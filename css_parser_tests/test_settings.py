"""Testcases for css_parser.settings"""
from __future__ import absolute_import
from __future__ import unicode_literals
__version__ = '$Id: test_csscharsetrule.py 1356 2008-07-13 17:29:09Z cthedot $'

from . import test_cssrule
import css_parser
import css_parser.settings


class Settings(test_cssrule.CSSRuleTestCase):

    def test_set(self):
        "settings.set()"
        css_parser.ser.prefs.useMinified()
        text = 'a {filter: progid:DXImageTransform.Microsoft.BasicImage( rotation = 90 )}'

        self.assertEqual(css_parser.parseString(text).cssText, ''.encode())

        css_parser.settings.set('DXImageTransform.Microsoft', True)
        self.assertEqual(css_parser.parseString(text).cssText,
                         'a{filter:progid:DXImageTransform.Microsoft.BasicImage(rotation=90)}'.encode())

        css_parser.ser.prefs.useDefaults()


if __name__ == '__main__':
    import unittest
    unittest.main()
