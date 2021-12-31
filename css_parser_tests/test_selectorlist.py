"""Testcases for css_parser.css.selectorlist.SelectorList."""

from __future__ import absolute_import
from __future__ import unicode_literals
import xml.dom
from . import basetest
import css_parser
from css_parser.css.selectorlist import SelectorList


class SelectorListTestCase(basetest.BaseTestCase):

    def setUp(self):
        basetest.BaseTestCase.setUp(self)
        self.r = SelectorList()

    def test_init(self):
        "SelectorList.__init__() and .length"
        s = SelectorList()
        self.assertEqual(0, s.length)

        s = SelectorList('a, b')
        self.assertEqual(2, s.length)
        self.assertEqual('a, b', s.selectorText)

        s = SelectorList(selectorText='a')
        self.assertEqual(1, s.length)
        self.assertEqual('a', s.selectorText)

        s = SelectorList(selectorText=('p|a', {'p': 'uri'}))  # n-dict
        self.assertEqual(1, s.length)
        self.assertEqual('p|a', s.selectorText)

        s = SelectorList(selectorText=('p|a', (('p', 'uri'),)))  # n-tuples
        self.assertEqual(1, s.length)
        self.assertEqual('p|a', s.selectorText)

    def test_parentRule(self):
        "Selector.parentRule"
        def check(style):
            self.assertEqual(style, style.selectorList.parentRule)
            for sel in style.selectorList:
                self.assertEqual(style.selectorList, sel.parent)

        style = css_parser.css.CSSStyleRule('a, b')
        check(style)

        # add new selector
        style.selectorList.append(css_parser.css.Selector('x'))
        check(style)

        # replace selectorList
        style.selectorList = css_parser.css.SelectorList('x')
        check(style)

        # replace selectorText
        style.selectorText = ('x, y')
        check(style)

    def test_appendSelector(self):
        "SelectorList.appendSelector() and .length"
        s = SelectorList()
        s.appendSelector('a')
        self.assertEqual(1, s.length)

        self.assertRaises(xml.dom.InvalidModificationErr,
                          s.appendSelector, 'b,')
        self.assertEqual(1, s.length)

        self.assertEqual('a', s.selectorText)

        s.append('b')
        self.assertEqual(2, s.length)
        self.assertEqual('a, b', s.selectorText)

        s.append('a')
        self.assertEqual(2, s.length)
        self.assertEqual('b, a', s.selectorText)

        # __setitem__
        self.assertRaises(IndexError, s.__setitem__, 4, 'x')
        s[1] = 'c'
        self.assertEqual(2, s.length)
        self.assertEqual('b, c', s.selectorText)
        # TODO: remove duplicates?
#        s[0] = 'c'
#        self.assertEqual(1, s.length)
#        self.assertEqual(u'c', s.selectorText)

        s = SelectorList()
        s.appendSelector(('p|a', {'p': 'uri', 'x': 'xxx'}))
        self.assertEqual('p|a', s.selectorText)
        # x gets lost as not used
        self.assertRaises(xml.dom.NamespaceErr, s.append, 'x|a')
        # not set at all
        self.assertRaises(xml.dom.NamespaceErr, s.append, 'y|a')
        # but p is retained
        s.append('p|b')
        self.assertEqual('p|a, p|b', s.selectorText)

    def test_selectorText(self):
        "SelectorList.selectorText"
        s = SelectorList()
        s.selectorText = 'a, b'
        self.assertEqual('a, b', s.selectorText)
        self.assertRaises(xml.dom.SyntaxErr, s._setSelectorText, ',')
        # not changed as invalid!
        self.assertEqual('a, b', s.selectorText)

        tests = {
            '*': None,
            '/*1*/*': None,
            '/*1*/*, a': None,
            'a, b': None,
            'a ,b': 'a, b',
            'a , b': 'a, b',
            'a, b, c': 'a, b, c',
            '#a, x#a, .b, x.b': '#a, x#a, .b, x.b',
            ('[p|a], p|*', (('p', 'uri'),)): '[p|a], p|*',
        }
        # do not parse as not complete
        self.do_equal_r(tests, att='selectorText')

        tests = {
            'x|*': xml.dom.NamespaceErr,
            '': xml.dom.SyntaxErr,
            ' ': xml.dom.SyntaxErr,
            ',': xml.dom.SyntaxErr,
            'a,': xml.dom.SyntaxErr,
            ',a': xml.dom.SyntaxErr,
            '/* 1 */,a': xml.dom.SyntaxErr,
        }
        # only set as not complete
        self.do_raise_r(tests, att='_setSelectorText')

    def test_reprANDstr(self):
        "SelectorList.__repr__(), .__str__()"
        sel = ('a, p|b', {'p': 'uri'})

        s = css_parser.css.SelectorList(selectorText=sel)

        self.assertIn(sel[0], str(s))

        s2 = eval(repr(s))
        self.assertIsInstance(s2, s.__class__)
        self.assertEqual(sel[0], s2.selectorText)


if __name__ == '__main__':
    import unittest
    unittest.main()
