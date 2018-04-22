## asynclog
[![Build Status](https://travis-ci.org/unpluggedcoder/asynclog.svg?branch=master)](https://travis-ci.org/unpluggedcoder/asynclog) [![Coverage Status](https://coveralls.io/repos/github/unpluggedcoder/asynclog/badge.svg?branch=master)](https://coveralls.io/github/unpluggedcoder/asynclog?branch=master)

`asynclog` provide the asynchronous way for python logging. Leave the logging I/O(especially the network I/O when we want to logging to a network endpoint) to the asynchronous thread or asynchronous task provided by [celery](http://www.celeryproject.org/) .

#### Requirements

* Python 3.5+

#### Install

```shell
pip install asynclog
```

#### Usage

* Config from dict

```python
log_cfg = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s \n %(levelname)s \n %(message)s'
        },
    },
    'handlers': {
        'async_handler': {
            'level': 'INFO',
            'formatter': 'simple',
            'class': 'asynclog.AsyncLogDispatcher',
            'func': '[Dot_Path_To_Your_Func]',
        }
    },
    'loggers': {
        'asynclogger': {
            'handlers': ['async_handler', ],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(log_cfg)
logger = logging.getLogger('asynclogger')
logger.info('Test asynclog')
```

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

#### Test

```shell
python3 -m unittest
......
----------------------------------------------------------------------
Ran 6 tests in 0.007s

OK
```



