#!/usr/bin/env python

from distutils.core import setup


PROJECT = "storytracker"
VERSION = '0.1'
AUTHOR = "GammaSQ"
AUTHOR_EMAIL = "doesnt.work@gmxat"
DESC = "A program to track a storyline of a book or RPG"

setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    #long_description=open('README.rst').read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    include_package_data=True,
    packages=["engine", "menue"],
    install_requires=[
        
    ],
)
