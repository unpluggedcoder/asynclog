import unittest


from asynclog.handler import AsyncLog


class Handler:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.records = []

    def emit(self, record):
        self.records.append(record)

    def acquire(self):
        pass

    def release(self):
        pass


class AsyncLogHandler(AsyncLog, Handler):
    pass


class TestAsyncLog(unittest.TestCase):
    ''' TestCase for AsyncLog class
    '''
    def test_create_asynclog_with_error_params(self):
        with self.assertRaises(ValueError) as ex:
            AsyncLog(use_thread=True, use_celery=True)
        self.assertEqual(ex.exception.args[0],
                         'Can not both use thread and celery.')

        with self.assertRaises(ValueError) as ex:
            AsyncLog(use_thread=False, use_celery=False)
        self.assertEqual(
            ex.exception.args[0],
            'None of approach are given, set either use_thread or '
            'use_celery to True.'
        )

        with self.assertRaises(ValueError) as ex:
            AsyncLog(use_thread=True, use_celery=False, thread_worker='2')
        self.assertEqual(
            ex.exception.args[0],
            'Integer expected for thread_worker argument.'
        )

    def test_can_create_asynclog_with_right_params(self):
        instance = AsyncLog(use_thread=True, use_celery=False)
        self.assertIsNotNone(instance._thread_executor)
        instance = AsyncLog(use_thread=False, use_celery=True)

    def test_can_work_with_thread(self):
        handler = AsyncLogHandler(use_thread=True)
        handler.emit('Debug log')
        handler.emit('Info log')
        handler.emit('Warning log')
        handler.close()
        self.assertEqual(len(handler.records), 3)


if __name__ == '__main__':
    unittest.main()
