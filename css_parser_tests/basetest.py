from __future__ import absolute_import, print_function, unicode_literals

import logging
import os
import re
import sys
import unittest
from contextlib import contextmanager
from io import StringIO

import css_parser

"""Base class for all tests"""


TEST_HOME = os.path.dirname(os.path.abspath(__file__))
PY2x = sys.version_info < (3, 0)


def msg3x(msg):
    """msg might contain unicode repr `u'...'` which in py3 is `u'...`
    needed by tests using ``assertRaisesMsg``"""
    if not PY2x and msg.find("u'"):
        msg = msg.replace("u'", "'")
    return msg


def get_resource_filename(resource_name):
    """Get the resource filename.
    """
    return os.path.join(TEST_HOME, *resource_name.split('/'))


def get_sheet_filename(sheet_name):
    """Get the filename for the given sheet."""
    # Extract all sheets since they might use @import
    sheet_dir = get_resource_filename('sheets')
    return os.path.join(sheet_dir, sheet_name)


class BaseTestCase(unittest.TestCase):

    def _tempSer(self):
        "Replace default ser with temp ser."
        self._ser = css_parser.ser
        css_parser.ser = css_parser.serialize.CSSSerializer()

    def _restoreSer(self):
        "Restore the default ser."
        css_parser.ser = self._ser

    @staticmethod
    def _setHandler():
        "sets log's new handler and returns StringIO instance to getvalue"
        s = StringIO()
        h = logging.StreamHandler(s)
        h.setFormatter(logging.Formatter('%(levelname)s    %(message)s'))
        # remove if present already
        css_parser.log.removeHandler(h)
        css_parser.log.addHandler(h)
        return s

    @staticmethod
    def captureLog(log_level, callable, *args, **kwargs):
        """returns the output of an ad hoc created log
        (which doesn't affect the standard one).
        Example usage:
        warning = self.captureLog(logging.WARNING,
                                   css_parser.stylesheets.MediaQuery,
                                   'unknown-media')
        self.assertEqual(warning, 'WARNING [...]')
        """
        old_log = css_parser.log._log
        old_level = css_parser.log.getEffectiveLevel()
        css_parser.log.setLog(logging.getLogger('CSS_PARSER-IGNORE'))
        css_parser.log.setLevel(log_level)
        s = BaseTestCase._setHandler()
        callable(*args, **kwargs)
        result = s.getvalue()
        css_parser.log.setLog(old_log)
        css_parser.log.setLevel(old_level)
        return result

    def setUp(self):
        # a raising parser!!!
        css_parser.log.raiseExceptions = True
        css_parser.log.setLevel(logging.FATAL)
        self.p = css_parser.CSSParser(raiseExceptions=True)

    @contextmanager
    def patch_default_fetcher(self, return_value):
        import css_parser.util as cu
        orig = cu._defaultFetcher

        def defaultFetcher(*a):
            return return_value
        if callable(return_value):
            cu._defaultFetcher = return_value
        else:
            cu._defaultFetcher = defaultFetcher
        try:
            yield
        finally:
            cu._defaultFetcher = orig

    def tearDown(self):
        if hasattr(self, '_ser'):
            self._restoreSer()

    def assertRaisesEx(self, exception, callable, *args, **kwargs):
        """
        from
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/307970
        """
        if "exc_args" in kwargs:
            exc_args = kwargs["exc_args"]
            del kwargs["exc_args"]
        else:
            exc_args = None
        if "exc_pattern" in kwargs:
            exc_pattern = kwargs["exc_pattern"]
            del kwargs["exc_pattern"]
        else:
            exc_pattern = None

        argv = [repr(a) for a in args]\
            + ["%s=%r" % (k, v) for k, v in kwargs.items()]
        callsig = "%s(%s)" % (callable.__name__, ", ".join(argv))

        try:
            callable(*args, **kwargs)
        except exception as exc:
            if exc_args is not None:
                self.failIf(exc.args != exc_args,
                            "%s raised %s with unexpected args: "
                            "expected=%r, actual=%r"
                            % (callsig, exc.__class__, exc_args, exc.args))
            if exc_pattern is not None:
                self.assertTrue(exc_pattern.search(str(exc)),
                                "%s raised %s, but the exception "
                                "does not match '%s': %r"
                                % (callsig, exc.__class__, exc_pattern.pattern,
                                   str(exc)))
        except Exception:
            exc_info = sys.exc_info()
            self.fail("%s raised an unexpected exception type: "
                      "expected=%s, actual=%s"
                      % (callsig, exception, exc_info[0]))
        else:
            self.fail("%s did not raise %s" % (callsig, exception))

    def assertRaisesMsg(self, excClass, msg, callableObj, *args, **kwargs):
        """
        Just like unittest.TestCase.assertRaises,
        but checks that the message is right too.

        Usage::

            self.assertRaisesMsg(
                MyException, "Exception message",
                my_function, (arg1, arg2)
                )

        from
        http://www.nedbatchelder.com/blog/200609.html#e20060905T064418
        """
        try:
            callableObj(*args, **kwargs)
        except excClass as exc:
            excMsg = str(exc)
            if not msg:
                # No message provided: any message is fine.
                return
            elif excMsg == msg:
                # Message provided, and we got the right message: passes.
                return
            else:
                # Message provided, and it didn't match: fail!
                raise self.failureException(
                    "Right exception, wrong message: got '%s' instead of '%s'" %
                    (excMsg, msg))
        else:
            if hasattr(excClass, '__name__'):
                excName = excClass.__name__
            else:
                excName = str(excClass)
            raise self.failureException(
                "Expected to raise %s, didn't get an exception at all" %
                excName
            )

    def do_equal_p(self, tests, att='cssText', debug=False, raising=True):
        """
        if raising self.p is used for parsing, else self.pf
        """
        p = css_parser.CSSParser(raiseExceptions=raising)
        # parses with self.p and checks att of result
        for test, expected in tests.items():
            if debug:
                print(('"%s"' % test))
            s = p.parseString(test)
            if expected is None:
                expected = test
            ans = s.__getattribute__(att)
            if isinstance(ans, bytes):
                ans = ans.decode('utf-8')
            self.assertEqual(expected, ans)

    def do_raise_p(self, tests, debug=False, raising=True):
        # parses with self.p and expects raise
        p = css_parser.CSSParser(raiseExceptions=raising)
        for test, expected in tests.items():
            if debug:
                print(('"%s"' % test))
            self.assertRaises(expected, p.parseString, test)

    def do_equal_r(self, tests, att='cssText', debug=False):
        # sets attribute att of self.r and asserts Equal
        for test, expected in tests.items():
            if debug:
                print(('"%s"' % test))
            self.r.__setattr__(att, test)
            if expected is None:
                expected = test
            self.assertEqual(expected, self.r.__getattribute__(att))

    def do_raise_r(self, tests, att='_setCssText', debug=False):
        # sets self.r and asserts raise
        for test, expected in tests.items():
            if debug:
                print(('"%s"' % test))
            self.assertRaises(expected, self.r.__getattribute__(att), test)

    def do_raise_r_list(self, tests, err, att='_setCssText', debug=False):
        # sets self.r and asserts raise
        for test in tests:
            if debug:
                print(('"%s"' % test))
            self.assertRaises(err, self.r.__getattribute__(att), test)


class GenerateTests(type):
    """Metaclass to handle a parametrized test.

    This works by generating many test methods from a single method.

    To generate the methods, you need the base method with the prefix
    "gen_test_", which takes the parameters. Then you define the attribute
    "cases" on this method with a list of cases. Each case is a tuple, which is
    unpacked when the test is called.

    Example::

        def gen_test_length(self, string, expected):
            self.assertEquals(len(string), expected)
        gen_test_length.cases = [
            ("a", 1),
            ("aa", 2),
        ]
    """
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        for aname, aobj in attrs.items():
            if not aname.startswith("gen_test_"):
                new_attrs[aname] = aobj
                continue

            # Strip off the gen_
            test_name = aname[4:]
            cases = aobj.cases
            for case_num, case in enumerate(cases):
                stringed_case = cls.make_case_repr(case)
                case_name = "%s_%s_%s" % (test_name, case_num, stringed_case)
                # Force the closure binding

                def make_wrapper(case=case, aobj=aobj):
                    def wrapper(self):
                        aobj(self, *case)
                    return wrapper
                wrapper = make_wrapper()
                wrapper.__name__ = str(case_name)
                wrapper.__doc__ = "%s(%s)" % (test_name,
                                              ", ".join(map(repr, case)))
                if aobj.__doc__ is not None:
                    wrapper.__doc__ += "\n\n" + aobj.__doc__
                new_attrs[case_name] = wrapper
        return type(name, bases, new_attrs)

    @classmethod
    def make_case_repr(cls, case):
        if isinstance(case, type('')):
            value = case
        else:
            try:
                iter(case)
            except TypeError:
                value = repr(case)
            else:
                value = '_'.join(cls.make_case_repr(x) for x in case)
        value = re.sub('[^A-Za-z_]', '_', value)
        value = re.sub('_{2,}', '_', value)
        return value
