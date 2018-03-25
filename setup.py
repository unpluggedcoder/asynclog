from setuptools import setup
from asynclog import __version__


setup(
    name='asynclog',
    version=__version__,
    description='Asynchronous log for python logging.',
    license='MIT',
    author='unpluggedcoder',
    author_email='unpluggedcoder@outlook.com',
    url='https://github.com/unpluggedcoder/asynclog',
    packages=['asynclog'],
    package_data={
        'asynclog': ['README.md', ]
    },
    keywords='logging asynchronous',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
    ],
)
