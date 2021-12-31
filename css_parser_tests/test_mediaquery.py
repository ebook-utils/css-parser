# -*- coding: iso-8859-1 -*-
"""Testcases for css_parser.stylesheets.MediaQuery"""

from __future__ import absolute_import
from __future__ import unicode_literals
import xml.dom
import logging
from . import basetest
import css_parser.stylesheets


class MediaQueryTestCase(basetest.BaseTestCase):

    def setUp(self):
        super(MediaQueryTestCase, self).setUp()
        self.r = css_parser.stylesheets.MediaQuery()

    def test_mediaText(self):
        "MediaQuery.mediaText"
        tests = {
            'all': None,
            'braille': None,
            'embossed': None,
            'handheld': None,
            'print': None,
            'projection': None,
            'screen': None,
            'speech': None,
            'tty': None,
            'tv': None,
            'ALL': None,
            'a\\ll': None,
            'not tv': None,
            'n\\ot t\\v': None,
            'only tv': None,
            '\\only \\tv': None,
            'PRINT': None,
            'NOT PRINT': None,
            'ONLY PRINT': None,
            'tv and (color)': None,
            'not tv and (color)': None,
            'only tv and (color)': None,
            'print and(color)': 'print and (color)',
            'aural': None  # xml.dom.SyntaxErr in cssutils
        }
        self.do_equal_r(tests, att='mediaText')

        tests = {
            '': xml.dom.SyntaxErr,
            'two values': xml.dom.SyntaxErr,
            'or even three': xml.dom.SyntaxErr,
            '3d': xml.dom.SyntaxErr,  # a dimension
        }
        self.do_raise_r(tests, att='_setMediaText')

    def test_mediaType(self):
        "MediaQuery.mediaType"
        mq = css_parser.stylesheets.MediaQuery()

        self.assertEqual('', mq.mediaText)

        for mt in css_parser.stylesheets.MediaQuery.MEDIA_TYPES:
            mq.mediaType = mt
            self.assertEqual(mq.mediaType, mt)
            mq.mediaType = mt.upper()
            self.assertEqual(mq.mediaType, mt.upper())

        mt = '3D-UNKOwn-MEDIAtype0123'
        #mq.mediaType = mt
        self.assertEqual(self.captureLog(logging.WARNING, mq._setMediaType, mt),
                         'WARNING    MediaQuery: Unknown media type: "3D-UNKOwn-MEDIAtype0123".\n')
        #self.assertRaises(xml.dom.InvalidCharacterErr, mq._setMediaType, mt)

    def test_comments(self):
        "MediaQuery.mediaText comments"
        tests = {
            'all': None,
            'print': None,
            'not print': None,
            'only print': None,
            'print and (color)': None,
            'print and (color) and (width)': None,
            'print and (color: 2)': None,
            'print and (min-width: 100px)': None,
            'print and (min-width: 100px) and (color: red)': None,
            'not print and (min-width: 100px)': None,
            'only print and (min-width: 100px)': None,
            '/*1*/ tv /*2*/': None,
            '/*0*/ only /*1*/ tv /*2*/': None,
            '/*0* /not /*1*/ tv /*2*/': None,
            '/*x*/ only /*x*/ print /*x*/ and /*x*/ (/*x*/ min-width /*x*/: /*x*/ 100px /*x*/)': None,
            'print and/*1*/(color)': 'print and /*1*/ (color)'
        }
        self.do_equal_r(tests, att='mediaText')

    def test_reprANDstr(self):
        "MediaQuery.__repr__(), .__str__()"
        mediaText = 'tv and (color)'
        s = css_parser.stylesheets.MediaQuery(mediaText=mediaText)
        self.assertIn(mediaText, str(s))
        s2 = eval(repr(s))
        self.assertEqual(mediaText, s2.mediaText)
        self.assertIsInstance(s2, s.__class__)


if __name__ == '__main__':
    import unittest
    unittest.main()
