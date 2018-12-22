import unittest
"""Testcase for cssutils imports"""


class CSSutilsImportTestCase(unittest.TestCase):
    def test_import_all(self):
        "from cssutils import *"
        import cssutils
        from cssutils import __all__ as aimp

        exp = {
            'CSSParser': cssutils.CSSParser,  # noqa
            'CSSSerializer': cssutils.CSSSerializer,  # noqa
            'css': cssutils.css,
            'stylesheets': cssutils.stylesheets,
        }
        self.assertEqual(len(aimp), len(exp))
        self.assertEqual(set(aimp), set(exp))


if __name__ == '__main__':
    import unittest
    unittest.main()
