# -*- coding: iso-8859-1 -*-
"""Testcases for css_parser.stylesheets.MediaList"""

from __future__ import absolute_import
from __future__ import unicode_literals
import xml.dom
import logging
from . import basetest
import css_parser.stylesheets



class MediaListTestCase(basetest.BaseTestCase):

    def setUp(self):
        super(MediaListTestCase, self).setUp()
        self.r = css_parser.stylesheets.MediaList()

    def test_set(self):
        "MediaList.mediaText 1"
        ml = css_parser.stylesheets.MediaList()

        self.assertEqual(0, ml.length)
        self.assertEqual('all', ml.mediaText)

        ml.mediaText = ' print   , screen '
        self.assertEqual(2, ml.length)
        self.assertEqual('print, screen', ml.mediaText)

        # self.assertRaisesMsg(xml.dom.InvalidModificationErr,
        #                     basetest.msg3x('''MediaList: Ignoring new medium css_parser.stylesheets.MediaQuery(mediaText=u'tv') as already specified "all" (set ``mediaText`` instead).'''),
        #                     ml._setMediaText, u' print , all  , tv ')
        #
        #self.assertEqual(u'all', ml.mediaText)
        #self.assertEqual(1, ml.length)

        self.assertEqual(self.captureLog(logging.WARNING, ml.appendMedium, 'test'),
                         'WARNING    MediaQuery: Unknown media type: "test".\n')

    def test_appendMedium(self):
        "MediaList.appendMedium() 1"
        ml = css_parser.stylesheets.MediaList()

        ml.appendMedium('print')
        self.assertEqual(1, ml.length)
        self.assertEqual('print', ml.mediaText)

        ml.appendMedium('screen')
        self.assertEqual(2, ml.length)
        self.assertEqual('print, screen', ml.mediaText)

        # automatic del and append!
        ml.appendMedium('print')
        self.assertEqual(2, ml.length)
        self.assertEqual('screen, print', ml.mediaText)

        # automatic del and append!
        ml.appendMedium('SCREEN')
        self.assertEqual(2, ml.length)
        self.assertEqual('print, SCREEN', ml.mediaText)

        # append invalid MediaQuery
        mq = css_parser.stylesheets.MediaQuery()
        ml.appendMedium(mq)
        self.assertEqual(2, ml.length)
        self.assertEqual('print, SCREEN', ml.mediaText)

        # append()
        mq = css_parser.stylesheets.MediaQuery('tv')
        ml.append(mq)
        self.assertEqual(3, ml.length)
        self.assertEqual('print, SCREEN, tv', ml.mediaText)

        # __setitem__
        self.assertRaises(IndexError, ml.__setitem__, 10, 'all')
        ml[0] = 'handheld'
        self.assertEqual(3, ml.length)
        self.assertEqual('handheld, SCREEN, tv', ml.mediaText)

    def test_appendAll(self):
        "MediaList.append() 2"
        ml = css_parser.stylesheets.MediaList()
        ml.appendMedium('print')
        ml.appendMedium('tv')
        self.assertEqual(2, ml.length)
        self.assertEqual('print, tv', ml.mediaText)

        ml.appendMedium('all')
        self.assertEqual(1, ml.length)
        self.assertEqual('all', ml.mediaText)

        self.assertRaisesMsg(xml.dom.InvalidModificationErr,
                             basetest.msg3x(
                                 '''MediaList: Ignoring new medium css_parser.stylesheets.MediaQuery(mediaText=u'tv') as already specified "all" (set ``mediaText`` instead).'''),
                             ml.appendMedium, 'tv')
        self.assertEqual(1, ml.length)
        self.assertEqual('all', ml.mediaText)

        self.assertRaises(xml.dom.InvalidModificationErr,
                          ml.appendMedium, 'test')

    def test_append2All(self):
        "MediaList all"
        ml = css_parser.stylesheets.MediaList()
        ml.appendMedium('all')
        self.assertRaisesMsg(xml.dom.InvalidModificationErr,
                             basetest.msg3x(
                                 '''MediaList: Ignoring new medium css_parser.stylesheets.MediaQuery(mediaText=u'print') as already specified "all" (set ``mediaText`` instead).'''),
                             ml.appendMedium, 'print')

        sheet = css_parser.parseString('@media all, print { /**/ }')
        self.assertEqual('@media all {\n    /**/\n    }'.encode(), sheet.cssText)

    def test_delete(self):
        "MediaList.deleteMedium()"
        ml = css_parser.stylesheets.MediaList()

        self.assertRaises(xml.dom.NotFoundErr, ml.deleteMedium, 'all')
        self.assertRaises(xml.dom.NotFoundErr, ml.deleteMedium, 'test')

        ml.appendMedium('print')
        ml.deleteMedium('print')
        ml.appendMedium('tV')
        ml.deleteMedium('Tv')
        self.assertEqual(0, ml.length)
        self.assertEqual('all', ml.mediaText)

    def test_item(self):
        "MediaList.item()"
        ml = css_parser.stylesheets.MediaList()
        ml.appendMedium('print')
        ml.appendMedium('screen')

        self.assertEqual('print', ml.item(0))
        self.assertEqual('screen', ml.item(1))
        self.assertEqual(None, ml.item(2))

    # REMOVED special case!
    # def test_handheld(self):
    #    "MediaList handheld"
    #    ml = css_parser.stylesheets.MediaList()

    #    ml.mediaText = u' handheld , all  '
    #    self.assertEqual(2, ml.length)
    #    self.assertEqual(u'handheld, all', ml.mediaText)

    #    self.assertRaisesMsg(xml.dom.InvalidModificationErr,
    #                         basetest.msg3x('''MediaList: Ignoring new medium css_parser.stylesheets.MediaQuery(mediaText=u'handheld') as already specified "all" (set ``mediaText`` instead).'''),
    #                         ml._setMediaText, u' handheld , all  , tv ')

    def test_mediaText(self):
        "MediaList.mediaText 2"
        tests = {
            'ALL': 'ALL',
            'Tv': 'Tv',
            'all': None,
            'all, handheld': 'all',
            'tv': None,
            'tv, handheld, print': None,
            'tv and (color), handheld and (width: 1px) and (color)': None,
            'print, amzn-mobi': None
        }
        self.do_equal_r(tests, att='mediaText')

        tests = {
            '': xml.dom.SyntaxErr,
            'a,b': xml.dom.SyntaxErr,
            'not': xml.dom.SyntaxErr,  # known but need media
            'only': xml.dom.SyntaxErr,  # known but need media
            'not tv,': xml.dom.SyntaxErr,  # known but need media
            'all;': xml.dom.SyntaxErr,
            'all, and(color)': xml.dom.SyntaxErr,
            'all,': xml.dom.SyntaxErr,
            'all, ': xml.dom.SyntaxErr,
            'all ,': xml.dom.SyntaxErr,
            'all, /*1*/': xml.dom.SyntaxErr,
            'all and (color),': xml.dom.SyntaxErr,
            'all tv, print': xml.dom.SyntaxErr,
        }
        self.do_raise_r(tests, att='_setMediaText')

    def test_comments(self):
        "MediaList.mediaText comments"
        tests = {
            '/*1*/ tv /*2*/, /*3*/ handheld /*4*/, print':
            '/*1*/ tv /*2*/ /*3*/, handheld /*4*/, print',
        }
        self.do_equal_r(tests, att='mediaText')

    def test_reprANDstr(self):
        "MediaList.__repr__(), .__str__()"
        mediaText = 'tv, print'

        s = css_parser.stylesheets.MediaList(mediaText=mediaText)

        self.assertIn(mediaText, str(s))

        s2 = eval(repr(s))
        self.assertIsInstance(s2, s.__class__)
        self.assertEqual(mediaText, s2.mediaText)


if __name__ == '__main__':
    import unittest
    unittest.main()
