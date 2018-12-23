"""Testcases for css_parser.stylesheets.StyleSheet"""
from __future__ import absolute_import
from __future__ import unicode_literals
__version__ = '$Id: test_csspagerule.py 1869 2009-10-17 19:37:40Z cthedot $'

import xml.dom
from . import basetest
import css_parser


class StyleSheetTestCase(basetest.BaseTestCase):

    def test_init(self):
        "StyleSheet.__init__()"
        s = css_parser.stylesheets.StyleSheet()

        self.assertEqual(s.type, 'text/css')
        self.assertEqual(s.href, None)
        self.assertEqual(s.media, None)
        self.assertEqual(s.title, '')
        self.assertEqual(s.ownerNode, None)
        self.assertEqual(s.parentStyleSheet, None)
        self.assertEqual(s.alternate, False)
        self.assertEqual(s.disabled, False)

        s = css_parser.stylesheets.StyleSheet(type='unknown',
                                            href='test.css',
                                            media=None,
                                            title='title',
                                            ownerNode=None,
                                            parentStyleSheet=None,
                                            alternate=True,
                                            disabled=True)

        self.assertEqual(s.type, 'unknown')
        self.assertEqual(s.href, 'test.css')
        self.assertEqual(s.media, None)
        self.assertEqual(s.title, 'title')
        self.assertEqual(s.ownerNode, None)
        self.assertEqual(s.parentStyleSheet, None)
        self.assertEqual(s.alternate, True)
        self.assertEqual(s.disabled, True)


if __name__ == '__main__':
    import unittest
    unittest.main()
