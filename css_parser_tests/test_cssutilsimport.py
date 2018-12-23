from __future__ import absolute_import
from __future__ import unicode_literals
import unittest
"""Testcase for css_parser imports"""


class CSSutilsImportTestCase(unittest.TestCase):
    def test_import_all(self):
        "from css_parser import *"
        import css_parser
        from css_parser import __all__ as aimp

        exp = {
            'CSSParser': css_parser.CSSParser,  # noqa
            'CSSSerializer': css_parser.CSSSerializer,  # noqa
            'css': css_parser.css,
            'stylesheets': css_parser.stylesheets,
        }
        self.assertEqual(len(aimp), len(exp))
        self.assertEqual(set(aimp), set(exp))


if __name__ == '__main__':
    import unittest
    unittest.main()
