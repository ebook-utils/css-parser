"""Testcases for css_parser.css.CSSValue and CSSPrimitiveValue."""
from __future__ import absolute_import
from __future__ import unicode_literals
__version__ = '$Id: test_cssvalue.py 1473 2008-09-15 21:15:54Z cthedot $'

# from decimal import Decimal # maybe for later tests?
import xml.dom
from . import basetest
import css_parser
import types


class XTestCase(basetest.BaseTestCase):

    def setUp(self):
        css_parser.ser.prefs.useDefaults()

    def tearDown(self):
        css_parser.ser.prefs.useDefaults()

    def test_prioriy(self):
        "Property.priority"
        s = css_parser.parseString('a { color: red }')
        self.assertEqual(s.cssText, 'a {\n    color: red\n    }'.encode())
#        self.assertEqual(u'', s.cssRules[0].style.getPropertyPriority('color'))
#
#        s = css_parser.parseString('a { color: red !important }')
#        self.assertEqual(u'a {\n    color: red !important\n    }', s.cssText)
#        self.assertEqual(u'important', s.cssRules[0].style.getPropertyPriority('color'))
#
#        css_parser.log.raiseExceptions = True
#        p = css_parser.css.Property(u'color', u'red', u'')
#        self.assertEqual(p.priority, u'')
#        p = css_parser.css.Property(u'color', u'red', u'!important')
#        self.assertEqual(p.priority, u'important')
#        self.assertRaisesMsg(xml.dom.SyntaxErr,
#                             u'',
#                             css_parser.css.Property, u'color', u'red', u'x')
#
#        css_parser.log.raiseExceptions = False
#        p = css_parser.css.Property(u'color', u'red', u'!x')
#        self.assertEqual(p.priority, u'x')
#        p = css_parser.css.Property(u'color', u'red', u'!x')
#        self.assertEqual(p.priority, u'x')
#        css_parser.log.raiseExceptions = True
#
#
#        # invalid but kept!
# css_parser.log.raiseExceptions = False
##        s = css_parser.parseString('a { color: red !x }')
##        self.assertEqual(u'a {\n    color: red !x\n    }', s.cssText)
##        self.assertEqual(u'x', s.cssRules[0].style.getPropertyPriority('color'))
#


if __name__ == '__main__':
    import unittest
    unittest.main()
