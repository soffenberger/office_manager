#!/usr/bin/python

from distutils.core import setup

files = ["images/*"]

setup(name='Office Manager',
    version='1.0',
    description='First Release of the Office Manager',
    author='Spencer Offenberger',
    author_email='soffenbe@asu.edu',
    url='https://www.python.org/sigs/distutils-sig/',
    packages = ['src'],
    #It says, package *needs* these files.
    package_data = {'package' : files },
    #'runner' is in the root.
    scripts = ["runner"],
    long_description = """Really long text here.""" 
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers = [] 
    )
