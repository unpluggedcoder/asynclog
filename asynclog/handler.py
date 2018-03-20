from concurrent import futures
from functools import wraps

try:
    from celery import shared_task
except ImportError:
    def shared_task(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


def log_async(func):
    @shared_task
    def wrapper_task(*args, **kwargs):
        return func(*args, **kwargs)

    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0]
        if instance.use_thread:
            instance.submit(func, *args, **kwargs)
        elif instance.use_celery:
            return wrapper_task.delay(*args, **kwargs)
    return wrapper


class AsyncLog:
    '''
    A handler class which process logging in an asynchronous way.
    '''
    def __init__(self, use_thread=True, use_celery=False, thread_worker=None,
                 *args, **kwargs):
        '''Choose the way how async logging perform.

        :param use_thread: Set to use the asynchronous provided by
            ThreadPoolExecutor. True by default.
        :param use_celery: Set if Celery is available, False by default.
        :param thread_worker: Max workers of ThreadPoolExecutor.
        '''
        if use_thread and use_celery:
            raise ValueError('Can not both use thread and celery.')
        elif not use_thread and not use_celery:
            raise ValueError(
                'None of approach are given, set either use_thread or '
                'use_celery to True.')

        if thread_worker and not isinstance(thread_worker, int):
            raise ValueError('Integer expected for thread_worker argument.')

        self.use_thread = use_thread
        self.use_celery = use_celery
        if use_thread:
            self._thread_executor = futures.ThreadPoolExecutor(
                max_workers=thread_worker)
        else:
            self._thread_executor = None
        super(AsyncLog, self).__init__(*args, **kwargs)

    def close(self):
        '''
        Close ThreadPoolExecutor if needed.
        '''
        self.acquire()
        try:
            if self.use_thread and self._thread_executor:
                self._thread_executor.shutdown(wait=True)
        finally:
            self.release()

    def submit(self, func, *args, **kwargs):
        if self.use_thread and self._thread_executor:
            self._thread_executor.submit(func, *args, **kwargs)

    @log_async
    def emit(self, record):
        super(AsyncLog, self).emit(record)
