#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cssutils setup

use EasyInstall or install with
    >python setup.py install
"""
__docformat__ = 'restructuredtext'
__author__ = 'Christof Hoeke with contributions by Walter Doerwald and lots of other people'
__date__ = '$LastChangedDate::                            $:'

import re
import sys
import os

from setuptools import find_packages, setup
from setuptools.command.test import test

# extract the version without importing the module
VERSION = re.search(r"^VERSION\s+=\s+'(.+?)'", open('src/cssutils/version.py', 'rb').read().decode('utf-8'))
long_description = '\n' + open('README.md', 'rb').read().decode('utf-8') + '\n'  # + read('CHANGELOG.txt')


class Test(test):

    user_options = [
        ('which-test=', 'w', "Specify which test to run as either"
            " the test method name (without the leading test_)"
            " or a module name with a trailing period"),
    ]

    def initialize_options(self):
        self.which_test = None

    def finalize_options(self):
        pass

    def run(self):
        import importlib
        orig = sys.path[:]
        try:
            sys.path.insert(0, os.getcwd())
            m = importlib.import_module('run_tests')
            which_test = (self.which_test,) if self.which_test else ()
            m.run_tests(which_test)
        finally:
            sys.path = orig


setup(
    name='cssutils',
    version=VERSION,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'csscapture = cssutils.scripts.csscapture:main',
            'csscombine = cssutils.scripts.csscombine:main',
            'cssparse = cssutils.scripts.cssparse:main'
        ]
    },
    description='A CSS Cascading Style Sheets library for Python',
    long_description=long_description,
    cmdclass={'test': Test},
    author='Christof Hoeke',
    author_email='c@cthedot.de',
    url='http://cthedot.de/cssutils/',
    download_url='https://bitbucket.org/cthedot/cssutils/downloads',
    license='LGPL 2.1 or later, see also http://cthedot.de/cssutils/',
    keywords='CSS, Cascading Style Sheets, CSSParser, DOM Level 2 Stylesheets, DOM Level 2 CSS',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
