"""Testcases for css_parser.css.CSSRule"""

from __future__ import absolute_import
from __future__ import unicode_literals
import xml.dom
from . import basetest
import css_parser.css


class CSSRuleTestCase(basetest.BaseTestCase):
    """
    base class for all CSSRule subclass tests

    overwrite setUp with the appriopriate values, will be used in
    test_init and test_readonly
    overwrite all tests as you please, use::

        super(CLASSNAME, self).test_TESTNAME(params)

    to use the base class tests too
    """

    def setUp(self):
        """
        OVERWRITE!
        self.r is the rule
        self.rRO the readonly rule
        relf.r_type the type as defined in CSSRule
        """
        super(CSSRuleTestCase, self).setUp()

        self.sheet = css_parser.css.CSSStyleSheet()
        self.r = css_parser.css.CSSRule()
        self.rRO = css_parser.css.CSSRule()
        self.rRO._readonly = True  # must be set here!
        self.r_type = css_parser.css.CSSRule.UNKNOWN_RULE
        self.r_typeString = 'UNKNOWN_RULE'

    def tearDown(self):
        css_parser.ser.prefs.useDefaults()

    def test_init(self):
        "CSSRule.type and init"
        self.assertEqual(self.r_type, self.r.type)
        self.assertEqual(self.r_typeString, self.r.typeString)
        self.assertEqual('', self.r.cssText)
        self.assertEqual(None, self.r.parentRule)
        self.assertEqual(None, self.r.parentStyleSheet)

    def test_parentRule_parentStyleSheet_type(self):
        "CSSRule.parentRule .parentStyleSheet .type"
        rules = [
            ('@charset "ascii";', css_parser.css.CSSRule.CHARSET_RULE),
            ('@import "x";', css_parser.css.CSSRule.IMPORT_RULE),
            ('@namespace "x";', css_parser.css.CSSRule.NAMESPACE_RULE),
            ('@font-face { src: url(x) }', css_parser.css.CSSRule.FONT_FACE_RULE),
            ('''@media all {
                    @x;
                    a { color: red }
                    /* c  */
                }''', css_parser.css.CSSRule.MEDIA_RULE),
            ('@page :left { color: red }', css_parser.css.CSSRule.PAGE_RULE),
            ('@unknown;', css_parser.css.CSSRule.UNKNOWN_RULE),
            ('b { left: 0 }', css_parser.css.CSSRule.STYLE_RULE),
            ('/*1*/', css_parser.css.CSSRule.COMMENT)  # must be last for add test
        ]
        mrt = [css_parser.css.CSSRule.UNKNOWN_RULE,
               css_parser.css.CSSRule.STYLE_RULE,
               css_parser.css.CSSRule.COMMENT]

        def test(s):
            for i, rule in enumerate(s):
                self.assertEqual(rule.parentRule, None)
                self.assertEqual(rule.parentStyleSheet, s)
                #self.assertEqual(rule.type, rules[i][1])
                if rule.MEDIA_RULE == rule.type:
                    for j, r in enumerate(rule):
                        self.assertEqual(r.parentRule, rule)
                        self.assertEqual(r.parentStyleSheet, s)
                        self.assertEqual(r.type, mrt[j])

                if i == 0:  # check encoding
                    self.assertEqual('ascii', s.encoding)
                elif i == 2:  # check namespaces
                    self.assertEqual('x', s.namespaces[''])

        cssText = ''.join(r[0] for r in rules)
        # parsing
        s = css_parser.parseString(cssText)
        test(s)
        # sheet.cssText
        s = css_parser.css.CSSStyleSheet()
        s.cssText = cssText
        test(s)
        # sheet.add CSS
        s = css_parser.css.CSSStyleSheet()
        for css, type_ in rules:
            s.add(css)
        test(s)
        # sheet.insertRule CSS
        s = css_parser.css.CSSStyleSheet()
        for css, type_ in rules:
            s.insertRule(css)
        test(s)

        types = [css_parser.css.CSSCharsetRule,
                 css_parser.css.CSSImportRule,
                 css_parser.css.CSSNamespaceRule,
                 css_parser.css.CSSFontFaceRule,
                 css_parser.css.CSSMediaRule,
                 css_parser.css.CSSPageRule,
                 css_parser.css.CSSUnknownRule,
                 css_parser.css.CSSStyleRule,
                 css_parser.css.CSSComment]
        # sheet.add CSSRule
        s = css_parser.css.CSSStyleSheet()
        for i, (css, type_) in enumerate(rules):
            rule = types[i]()
            rule.cssText = css
            s.add(rule)
        test(s)
        # sheet.insertRule CSSRule
        s = css_parser.css.CSSStyleSheet()
        for i, (css, type_) in enumerate(rules):
            rule = types[i]()
            rule.cssText = css
            s.insertRule(rule)
        test(s)

    def test_CSSMediaRule_cssRules_parentRule_parentStyleSheet_type(self):
        "CSSMediaRule.cssRules.parentRule .parentStyleSheet .type"
        rules = [
            ('b { left: 0 }', css_parser.css.CSSRule.STYLE_RULE),
            ('/*1*/', css_parser.css.CSSRule.COMMENT),
            ('@x;', css_parser.css.CSSRule.UNKNOWN_RULE)
        ]

        def test(s):
            mr = s.cssRules[0]
            for i, rule in enumerate(mr):
                self.assertEqual(rule.parentRule, mr)
                self.assertEqual(rule.parentStyleSheet, s)
                self.assertEqual(rule.parentStyleSheet, mr.parentStyleSheet)
                self.assertEqual(rule.type, rules[i][1])

        cssText = '@media all { %s }' % ''.join(r[0] for r in rules)
        # parsing
        s = css_parser.parseString(cssText)
        test(s)
        # sheet.cssText
        s = css_parser.css.CSSStyleSheet()
        s.cssText = cssText
        test(s)

        def getMediaSheet():
            s = css_parser.css.CSSStyleSheet()
            s.cssText = '@media all {}'
            return s, s.cssRules[0]
        # sheet.add CSS
        s, mr = getMediaSheet()
        for css, type_ in rules:
            mr.add(css)
        test(s)
        # sheet.insertRule CSS
        s, mr = getMediaSheet()
        for css, type_ in rules:
            mr.insertRule(css)
        test(s)

        types = [css_parser.css.CSSStyleRule,
                 css_parser.css.CSSComment,
                 css_parser.css.CSSUnknownRule]
        # sheet.add CSSRule
        s, mr = getMediaSheet()
        for i, (css, type_) in enumerate(rules):
            rule = types[i]()
            rule.cssText = css
            mr.add(rule)
        test(s)
        # sheet.insertRule CSSRule
        s, mr = getMediaSheet()
        for i, (css, type_) in enumerate(rules):
            rule = types[i]()
            rule.cssText = css
            mr.insertRule(rule)
        test(s)

    def test_readonly(self):
        "CSSRule readonly"
        self.rRO = css_parser.css.CSSRule()
        self.rRO._readonly = True
        self.assertEqual(True, self.rRO._readonly)
        self.assertEqual('', self.rRO.cssText)
        self.assertRaises(xml.dom.NoModificationAllowedErr,
                          self.rRO._setCssText, 'x')
        self.assertEqual('', self.rRO.cssText)

    def _test_InvalidModificationErr(self, startwithspace):
        """
        CSSRule.cssText InvalidModificationErr

        called by subclasses

        startwithspace

        for test starting with this not the test but " test" is tested
        e.g. " @page {}"
        exception is the style rule test
        """
        tests = ('',
                 '/* comment */',
                 '@charset "utf-8";',
                 '@font-face {}',
                 '@import url(x);',
                 '@media all {}',
                 '@namespace "x";'
                 '@page {}',
                 '@unknown;',
                 '@variables;',
                 # TODO:
                 #u'@top-left {}'
                 'a style rule {}'
                 )
        for test in tests:
            if startwithspace in ('a style rule', ) and test in (
                    '/* comment */', 'a style rule {}'):
                continue

            if test.startswith(startwithspace):
                test = ' %s' % test

            self.assertRaises(xml.dom.InvalidModificationErr,
                              self.r._setCssText, test)

        # check that type is readonly
        self.assertRaises(AttributeError, self.r.__setattr__, 'parentRule', None)
        self.assertRaises(AttributeError, self.r.__setattr__, 'parentStyleSheet', None)
        self.assertRaises(AttributeError, self.r.__setattr__, 'type', 1)
        self.assertRaises(AttributeError, self.r.__setattr__, 'typeString', "")


if __name__ == '__main__':
    import unittest
    unittest.main()
