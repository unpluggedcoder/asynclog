## asynclog

`asynclog` provide the asynchronous way for python logging. Leave the logging I/O(especially the network I/O when we want to logging to a network endpoint) to the asynchronous thread or asynchronous task provided by [celery](http://www.celeryproject.org/) .

#### Install

```shell
python setup.py install
```

#### Usage

* Using thread

```python
import logging
import time

from asynclog import AsyncLogDispatcher


def write_log(msg):
    # Do write stuff, such as write log msg into network.
    # ...
    time.sleep(0.5)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = AsyncLogDispatcher(write_log)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info('Test Log')
```

* Using Celery

```python
from celery import shared_task

@shared_task
def write_task(msg):
    # Write log in Network IO
    print(msg)
    
celery_handler = AsyncLogDispatcher(write_task, use_thread=False, use_celery=True)
celery_handler.setLevel(logging.INFO)
logger.addHandler(celery_handler)

logger.info('Test Log')
```

####Test

```shell
python -m unittest
....
----------------------------------------------------------------------
Ran 4 tests in 0.003s

OK
```



