#!/usr/bin/env python
import os
import codecs

from setuptools import setup, find_packages

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
here = lambda *x: os.path.join(PACKAGE_ROOT, *x)


with codecs.open(here('README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='eusurvey',
    version='0.1.2',
    description='EU Survey bridge.',
    long_description=long_description,
    author='Mozilla',
    license='MPL 2.0',
    url='',
    include_package_data=True,
    package_data={
        'eusurvey': []
    },
    scripts=[
        'eusurvey/bin/survey.py',
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: OS',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=[],
)
