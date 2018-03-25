# MIT License

# Copyright (c) 2018 Unplugged Coder

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
from concurrent import futures


class AsyncLogDispatcher(logging.Handler):
    ''' A dispatcher class which process logging in an asynchronous way.

    It doesn't do any log procedure actually. Instead, it just provide the
    asynchonrous way to do the logging. That's why it named as Dispatcher.
    It's useful when logging to a network endpoint.
    '''
    def __init__(self, func, use_thread=True, use_celery=False,
                 thread_worker=None, *args, **kwargs):
        '''Choose the way how async logging perform.

        :param use_thread: Set to use the asynchronous provided by
            ThreadPoolExecutor. True by default.
        :param use_celery: Set if Celery is available, False by default.
        :param thread_worker: Max workers of ThreadPoolExecutor. If it is None
            or not given, it will default to the number of processors on
            the machine.
        '''
        if use_thread and use_celery:
            raise ValueError('Can not both use thread and celery.')
        elif not use_thread and not use_celery:
            raise ValueError(
                'None of approach are given, set either use_thread or '
                'use_celery to True.')

        if use_thread and not callable(func):
            raise ValueError(
                'func must be a callable function while use_thread is True.')
        elif use_celery and not hasattr(func, 'delay'):
            raise ValueError(
                'Makesure Celery is available while use_celery is True.')

        if thread_worker and not isinstance(thread_worker, int):
            raise ValueError('Integer expected for thread_worker argument.')

        self.func = func
        self.use_thread = use_thread
        self.use_celery = use_celery
        if use_thread:
            self._thread_executor = futures.ThreadPoolExecutor(
                max_workers=thread_worker)
        else:
            self._thread_executor = None
        super(AsyncLogDispatcher, self).__init__(*args, **kwargs)

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

    def emit(self, record):
        msg = self.format(record)
        if self.use_thread and self._thread_executor:
            self._thread_executor.submit(self.func, msg)
        elif self.use_celery:
            self.func.delay(msg)
