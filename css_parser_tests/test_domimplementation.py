"""Testcases for css_parser.css.DOMImplementation"""

from __future__ import absolute_import
from __future__ import unicode_literals
import xml.dom
import xml.dom.minidom
import unittest
import css_parser


class DOMImplementationTestCase(unittest.TestCase):

    def setUp(self):
        self.domimpl = css_parser.DOMImplementationCSS()

    def test_createCSSStyleSheet(self):
        "DOMImplementationCSS.createCSSStyleSheet()"
        title, media = 'Test Title', css_parser.stylesheets.MediaList('all')
        sheet = self.domimpl.createCSSStyleSheet(title, media)
        self.assertEqual(True, isinstance(sheet, css_parser.css.CSSStyleSheet))
        self.assertEqual(title, sheet.title)
        self.assertEqual(media, sheet.media)

    def test_createDocument(self):
        "DOMImplementationCSS.createDocument()"
        doc = self.domimpl.createDocument(None, None, None)
        self.assertIsInstance(doc, xml.dom.minidom.Document)

    def test_createDocumentType(self):
        "DOMImplementationCSS.createDocumentType()"
        doctype = self.domimpl.createDocumentType('foo', 'bar', 'raboof')
        self.assertIsInstance(doctype, xml.dom.minidom.DocumentType)

    def test_hasFeature(self):
        "DOMImplementationCSS.hasFeature()"
        tests = [
            ('css', '1.0'),
            ('css', '2.0'),
            ('stylesheets', '1.0'),
            ('stylesheets', '2.0')
        ]
        for name, version in tests:
            self.assertEqual(True, self.domimpl.hasFeature(name, version))


if __name__ == '__main__':
    unittest.main()
