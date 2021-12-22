  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))


setup(
    name='clepsydra',
    description='Liquid scheduler for python',
    version='0.1a1',
    url='https://github.com/tishka17/clepsydra',
    author='A. Tikhonov',
    author_email='17@itishka.org',
    license='Apache2',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(include=['clepsydra', 'clepsydra.*']),
    install_requires=[
    ],
    extras_require={
    },
    package_data={
    },
    python_requires=">=3.8",
)
