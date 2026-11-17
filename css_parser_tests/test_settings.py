"""Testcases for css_parser.settings"""
__version__ = '$Id: test_csscharsetrule.py 1356 2008-07-13 17:29:09Z cthedot $'

import css_parser
import css_parser.settings

from . import test_cssrule


class Settings(test_cssrule.CSSRuleTestCase):

    def test_set(self):
        "settings.set()"
        css_parser.ser.prefs.useMinified()
        text = 'a {filter: progid:DXImageTransform.Microsoft.BasicImage( rotation = 90 )}'

        self.assertEqual(css_parser.parseString(text).cssText, b'')

        css_parser.settings.set('DXImageTransform.Microsoft', True)
        self.assertEqual(css_parser.parseString(text).cssText,
                         b'a{filter:progid:DXImageTransform.Microsoft.BasicImage(rotation=90)}')

        css_parser.ser.prefs.useDefaults()


if __name__ == '__main__':
    import unittest
    unittest.main()
