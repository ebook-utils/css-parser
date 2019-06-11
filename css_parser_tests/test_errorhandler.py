"""Tests for parsing which does not raise Exceptions normally"""
from __future__ import absolute_import
from __future__ import unicode_literals
__version__ = '$Id: test_parse.py 1281 2008-06-04 21:12:29Z cthedot $'

import logging
import sys
import xml.dom
from . import basetest
import css_parser


class ErrorHandlerTestCase(basetest.BaseTestCase):

    def setUp(self):
        "replace default log and ignore its output"
        self._oldlog = css_parser.log._log
        self._saved = css_parser.log.raiseExceptions

        css_parser.log.raiseExceptions = False
        css_parser.log.setLog(logging.getLogger('IGNORED-CSSUTILS-TEST'))

    def tearDown(self):
        "reset default log"
        css_parser.log.setLog(self._oldlog)
        # for tests only
        css_parser.log.setLevel(logging.FATAL)
        css_parser.log.raiseExceptions = self._saved

    def test_calls(self):
        "css_parser.log.*"
        s = self._setHandler()
        css_parser.log.setLevel(logging.DEBUG)
        css_parser.log.debug('msg', neverraise=True)
        self.assertEqual(s.getvalue(), 'DEBUG    msg\n')

        s = self._setHandler()
        css_parser.log.setLevel(logging.INFO)
        css_parser.log.info('msg', neverraise=True)
        self.assertEqual(s.getvalue(), 'INFO    msg\n')

        s = self._setHandler()
        css_parser.log.setLevel(logging.WARNING)
        css_parser.log.warn('msg', neverraise=True)
        self.assertEqual(s.getvalue(), 'WARNING    msg\n')

        s = self._setHandler()
        css_parser.log.setLevel(logging.ERROR)
        css_parser.log.error('msg', neverraise=True)
        self.assertEqual(s.getvalue(), 'ERROR    msg\n')

        s = self._setHandler()
        css_parser.log.setLevel(logging.FATAL)
        css_parser.log.fatal('msg', neverraise=True)
        self.assertEqual(s.getvalue(), 'CRITICAL    msg\n')

        s = self._setHandler()
        css_parser.log.setLevel(logging.CRITICAL)
        css_parser.log.critical('msg', neverraise=True)
        self.assertEqual(s.getvalue(), 'CRITICAL    msg\n')

        s = self._setHandler()
        css_parser.log.setLevel(logging.CRITICAL)
        css_parser.log.error('msg', neverraise=True)
        self.assertEqual(s.getvalue(), '')

    def test_linecol(self):
        "css_parser.log line col"
        o = css_parser.log.raiseExceptions
        css_parser.log.raiseExceptions = True

        s = css_parser.css.CSSStyleSheet()
        try:
            s.cssText = '@import x;'
        except xml.dom.DOMException as e:
            self.assertEqual(str(e), 'CSSImportRule: Unexpected ident. [1:9: x]')
            self.assertEqual(e.line, 1)
            self.assertEqual(e.col, 9)
            if sys.platform.startswith('java'):
                self.assertEqual(e.msg, 'CSSImportRule: Unexpected ident. [1:9: x]')
            else:
                self.assertEqual(e.args, ('CSSImportRule: Unexpected ident. [1:9: x]',))

        css_parser.log.raiseExceptions = o

    def test_handlers(self):
        "css_parser.log"
        s = self._setHandler()

        css_parser.log.setLevel(logging.FATAL)
        self.assertEqual(css_parser.log.getEffectiveLevel(), logging.FATAL)

        css_parser.parseString('a { color: 1 }')
        self.assertEqual(s.getvalue(), '')

        css_parser.log.setLevel(logging.DEBUG)
        css_parser.parseString('a { color: 1 }')
        self.assertEqual(s.getvalue(),
                         'ERROR    Property: Invalid value for "CSS Level 2.1" property: 1 [1:5: color]\n')

        s = self._setHandler()

        css_parser.log.setLevel(logging.WARNING)
        css_parser.parseUrl('http://example.com')
        q = s.getvalue()[:38]
        if q.startswith('WARNING    URLError'):
            pass
        else:
            self.assertEqual(q, 'ERROR    Expected "text/css" mime type')

    def test_parsevalidation(self):
        style = 'color: 1'
        t = 'a { %s }' % style

        css_parser.log.setLevel(logging.DEBUG)

        # sheet
        s = self._setHandler()
        css_parser.parseString(t)
        self.assertNotEqual(len(s.getvalue()), 0)

        s = self._setHandler()
        css_parser.parseString(t, validate=False)
        self.assertEqual(s.getvalue(), '')

        # style
        s = self._setHandler()
        css_parser.parseStyle(style)
        self.assertNotEqual(len(s.getvalue()), 0)

        s = self._setHandler()
        css_parser.parseStyle(style, validate=True)
        self.assertNotEqual(len(s.getvalue()), 0)

        s = self._setHandler()
        css_parser.parseStyle(style, validate=False)
        self.assertEqual(s.getvalue(), '')


if __name__ == '__main__':
    import unittest
    unittest.main()
