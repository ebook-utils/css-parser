#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: LGPLv3 Copyright: 2017, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import absolute_import, division, print_function, unicode_literals

import importlib
import os
import sys
import unittest

self_path = os.path.abspath(__file__)
base = os.path.dirname(self_path)


def itertests(suite):
    stack = [suite]
    while stack:
        suite = stack.pop()
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                stack.append(test)
                continue
            if test.__class__.__name__ == 'ModuleImportFailure':
                raise Exception('Failed to import a test module: %s' % test)
            yield test


def filter_tests(suite, test_ok):
    ans = unittest.TestSuite()
    added = set()
    for test in itertests(suite):
        if test_ok(test) and test not in added:
            ans.addTest(test)
            added.add(test)
    return ans


def filter_tests_by_name(suite, name):
    if not name.startswith('test_'):
        name = 'test_' + name
    if name.endswith('_'):
        def q(test):
            return test._testMethodName.startswith(name)
    else:
        def q(test):
            return test._testMethodName == name

    return filter_tests(suite, q)


def filter_tests_by_module(suite, *names):
    names = frozenset(names)

    def q(test):
        m = test.__class__.__module__.rpartition('.')[-1]
        return m in names

    return filter_tests(suite, q)


def find_tests():
    suites = []
    for f in os.listdir(os.path.join(base, 'css_parser_tests')):
        n, ext = os.path.splitext(f)
        if ext == '.py' and n.startswith('test_'):
            m = importlib.import_module('css_parser_tests.' + n)
            suite = unittest.defaultTestLoader.loadTestsFromModule(m)
            suites.append(suite)
    return unittest.TestSuite(suites)


def run_tests(test_names=()):
    sys.path = [base, os.path.join(base, 'src')] + sys.path
    tests = find_tests()
    suites = []
    for name in test_names:
        if name.endswith('.'):
            module_name = name[:-1]
            if not module_name.startswith('test_'):
                module_name = 'test_' + module_name
            suites.append(filter_tests_by_module(tests, module_name))
        else:
            suites.append(filter_tests_by_name(tests, name))
    tests = unittest.TestSuite(suites) if suites else tests

    r = unittest.TextTestRunner
    result = r().run(tests)

    if not result.wasSuccessful():
        raise SystemExit(1)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='''\
Run the specified tests, or all tests if none are specified. Tests
can be specified as either the test method name (without the leading test_)
or a module name with a trailing period.
''')
    parser.add_argument(
        'test_name',
        nargs='*',
        help=(
            'Test name (either a method name or a module name with a trailing period)'
            '. Note that if the name ends with a trailing underscore all tests methods'
            ' whose names start with the specified name are run.'
        )
    )
    args = parser.parse_args()
    run_tests(args.test_name)


if __name__ == '__main__':
    main()
