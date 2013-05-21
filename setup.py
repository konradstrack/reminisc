import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "reminisc",
    version = "0.0.1-SNAPSHOT",
    author = "Konrad Strack",
    author_email = "konrad@strack.pl",
    description = (""),
    license = "BSD",
    packages=['reminisc', 'tests'],
    long_description=read('README'),
)