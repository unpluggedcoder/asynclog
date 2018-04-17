from setuptools import setup, find_packages
from os import path
from codecs import open

from asynclog import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='asynclog',
    version=__version__,
    description='Asynchronous log for python logging.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='unpluggedcoder',
    author_email='unpluggedcoder@outlook.com',
    url='https://github.com/unpluggedcoder/asynclog',
    packages=find_packages(),
    package_data={'asynclog': [
        'README.md',
    ]},
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
    ], )
