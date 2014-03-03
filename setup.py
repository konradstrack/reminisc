from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import os
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="reminisc",
    version="0.1-SNAPSHOT",
    author="Konrad Strack",
    author_email="",
    description=(""),
    long_description=read_file('README'),
    license="BSD",
    url="https://github.com/konradstrack/reminisc",
    packages=find_packages(),

    install_requires=[
        'mongoengine==0.8.7'
    ],

    package_data={
    },

    tests_require=['pytest', 'pytest-cov'],
    cmdclass={'test': PyTest},
)