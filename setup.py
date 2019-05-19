import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Nested tables columnprint',
    version='1.0.0',
    author='SamuelThewessen',
    author_email='sthewessen@gmail.com',
    description=('A multiple tables creation tool for printing'
                 ' multidimensional lists into nice column output'),
    license='MIT',
    keywords='columnprint table nestedtabel',
    url='http://github.com/Thewessen/NestedTables',
    packages='tables',
    long_discription=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: MIT License',
    ],
)
