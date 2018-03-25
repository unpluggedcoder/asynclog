import logging
import unittest
from unittest import mock
from functools import wraps

from asynclog.handler import AsyncLogHandler

has_celery = False
app = None

try:
    import celery
    from celery import shared_task
    app = celery.Celery('tasks', broker='redis://localhost:6379/0')
    has_celery = True
except ImportError:
    def shared_task(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


records = []


def write_func(record):
    global records
    records.append(record)


@shared_task
def write_task(record):
    # Write log in Network IO
    print(record)


class TestAsyncLog(unittest.TestCase):
    ''' TestCase for AsyncLogHandler class
    '''

    def setUp(self):
        global records
        records = []

    def test_create_asynclog_with_error_params(self):
        with self.assertRaises(ValueError) as ex:
            AsyncLogHandler(write_func, use_thread=True, use_celery=True)
        self.assertEqual(ex.exception.args[0],
                         'Can not both use thread and celery.')

        with self.assertRaises(ValueError) as ex:
            AsyncLogHandler(write_func, use_thread=False, use_celery=False)
        self.assertEqual(
            ex.exception.args[0],
            'None of approach are given, set either use_thread or '
            'use_celery to True.')

        with self.assertRaises(ValueError) as ex:
            wrong_type = ('wrong', 'type')
            AsyncLogHandler(wrong_type, use_thread=True)
        self.assertEqual(
            ex.exception.args[0],
            'func must be a callable function while use_thread is True.')

        with self.assertRaises(ValueError) as ex:
            AsyncLogHandler(write_func, use_thread=False, use_celery=True)
        self.assertEqual(
            ex.exception.args[0],
            'Makesure Celery is available while use_celery is True.')

        with self.assertRaises(ValueError) as ex:
            AsyncLogHandler(
                write_func,
                use_thread=True,
                use_celery=False,
                thread_worker='2')
        self.assertEqual(ex.exception.args[0],
                         'Integer expected for thread_worker argument.')

    @mock.patch('tests.test_handler.write_task')
    def test_can_create_asynclog_with_right_params(self, write_mock):
        instance = AsyncLogHandler(
            write_func, use_thread=True, use_celery=False)
        self.assertIsNotNone(instance._thread_executor)
        self.assertIsNotNone(instance.func)

        write_mock.delay = mock.MagicMock()
        instance = AsyncLogHandler(
            write_task, use_thread=False, use_celery=True)
        self.assertIsNone(instance._thread_executor)
        self.assertIsNotNone(instance.func)

    def test_can_work_with_thread(self):
        logger = logging.getLogger()
        handler = AsyncLogHandler(write_func, use_thread=True)
        handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.info('Debug log')
        logger.info('Info log')
        logger.info('Warning log')
        handler.close()
        self.assertEqual(len(records), 3)

    @mock.patch('tests.test_handler.write_task')
    def test_can_work_with_celery(self, write_mock):
        msgs = []

        def side_effect(msg):
            msgs.append(msg)
        write_mock.delay = mock.MagicMock(side_effect=side_effect)
        logger = logging.getLogger()
        handler = AsyncLogHandler(
            write_task, use_celery=True, use_thread=False)
        handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        logger.info('Debug log')
        logger.info('Info log')
        logger.info('Warning log')
        handler.close()
        write_mock.delay.assert_called()
        write_mock.delay.assert_has_calls([
            mock.call('Debug log'), mock.call('Info log'),
            mock.call('Warning log')
        ])
        self.assertEqual(len(msgs), 3)


if __name__ == '__main__':
    unittest.main()
