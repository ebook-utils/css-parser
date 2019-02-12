#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: LGPLv3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>

import ast
import re
import sys
import os

from setuptools import find_packages, setup
from setuptools.command.test import test

# extract the version without importing the module
VERSION = open('src/css_parser/version.py', 'rb').read().decode('utf-8')
VERSION = '.'.join(map(str, ast.literal_eval(re.search(r'^version\s+=\s+(.+)', VERSION, flags=re.M).group(1))))
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
    name='css-parser',
    version=VERSION,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    description='A CSS Cascading Style Sheets library for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    cmdclass={'test': Test},
    author='Various People',
    author_email='redacted@anonymous.net',
    url='https://github.com/ebook-utils/css-parser',
    license='LGPL 3.0 or later',
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
