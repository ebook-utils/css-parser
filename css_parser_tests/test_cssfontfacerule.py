"""Testcases for css_parser.css.CSSFontFaceRule"""

from __future__ import absolute_import
from __future__ import unicode_literals
import xml.dom
from . import test_cssrule
import css_parser


class CSSFontFaceRuleTestCase(test_cssrule.CSSRuleTestCase):

    def setUp(self):
        super(CSSFontFaceRuleTestCase, self).setUp()
        self.r = css_parser.css.CSSFontFaceRule()
        self.rRO = css_parser.css.CSSFontFaceRule(readonly=True)
        self.r_type = css_parser.css.CSSFontFaceRule.FONT_FACE_RULE
        self.r_typeString = 'FONT_FACE_RULE'

    def test_init(self):
        "CSSFontFaceRule.__init__()"
        super(CSSFontFaceRuleTestCase, self).test_init()

        r = css_parser.css.CSSFontFaceRule()
        self.assertIsInstance(r.style, css_parser.css.CSSStyleDeclaration)
        self.assertEqual(r, r.style.parentRule)

        # until any properties
        self.assertEqual('', r.cssText)

        # only possible to set @... similar name
        self.assertRaises(xml.dom.InvalidModificationErr, self.r._setAtkeyword, 'x')

        def checkrefs(ff):
            self.assertEqual(ff, ff.style.parentRule)
            for p in ff.style:
                self.assertEqual(ff.style, p.parent)

        checkrefs(css_parser.css.CSSFontFaceRule(
            style=css_parser.css.CSSStyleDeclaration('font-family: x')))

        r = css_parser.css.CSSFontFaceRule()
        r.cssText = '@font-face { font-family: x }'
        checkrefs(r)

        r = css_parser.css.CSSFontFaceRule()
        r.style.setProperty('font-family', 'y')
        checkrefs(r)

        r = css_parser.css.CSSFontFaceRule()
        r.style['font-family'] = 'z'
        checkrefs(r)

        r = css_parser.css.CSSFontFaceRule()
        r.style.fontFamily = 'a'
        checkrefs(r)

    def test_cssText(self):
        "CSSFontFaceRule.cssText"
        tests = {
            '''@font-face {
    font-family: x;
    src: url(../fonts/LateefRegAAT.ttf) format("truetype-aat"), url(../fonts/LateefRegOT.ttf) format("opentype");
    font-style: italic;
    font-weight: 500;
    font-stretch: condensed;
    unicode-range: u+1-ff, u+111
    }''': None,
            '@font-face{font-family: x;}': '@font-face {\n    font-family: x\n    }',
            '@font-face  {  font-family: x;  }': '@font-face {\n    font-family: x\n    }',
            '@f\\ont\\-face{font-family : x;}': '@font-face {\n    font-family: x\n    }',
            # comments
            '@font-face/*1*//*2*/{font-family: x;}':
                '@font-face /*1*/ /*2*/ {\n    font-family: x\n    }',
            # WS
            '@font-face\n\t\f {\n\t\f font-family:x;\n\t\f }':
                '@font-face {\n    font-family: x\n    }',
        }
        self.do_equal_r(tests)
        self.do_equal_p(tests)

        tests = {
            '@font-face;': xml.dom.SyntaxErr,
            '@font-face }': xml.dom.SyntaxErr,
        }
        self.do_raise_p(tests)  # parse
        tests.update({
            '@font-face {': xml.dom.SyntaxErr,  # no }
            # trailing
            '@font-face {}1': xml.dom.SyntaxErr,
            '@font-face {}/**/': xml.dom.SyntaxErr,
            '@font-face {} ': xml.dom.SyntaxErr,
        })
        self.do_raise_r(tests)  # set cssText

    def test_style(self):
        "CSSFontFaceRule.style (and references)"
        r = css_parser.css.CSSFontFaceRule()
        s1 = r.style
        self.assertEqual(r, s1.parentRule)
        self.assertEqual('', s1.cssText)

        # set rule.cssText
        r.cssText = '@font-face { font-family: x1 }'
        self.assertNotEqual(r.style, s1)
        self.assertEqual(r, r.style.parentRule)
        self.assertEqual(r.cssText, '@font-face {\n    font-family: x1\n    }')
        self.assertEqual(r.style.cssText, 'font-family: x1')
        self.assertEqual(s1.cssText, '')
        s2 = r.style

        # set invalid rule.cssText
        try:
            r.cssText = '@font-face { $ }'
        except xml.dom.SyntaxErr as e:
            pass
        self.assertEqual(r.style, s2)
        self.assertEqual(r, s2.parentRule)
        self.assertEqual(r.cssText, '@font-face {\n    font-family: x1\n    }')
        self.assertEqual(s2.cssText, 'font-family: x1')
        self.assertEqual(r.style.cssText, 'font-family: x1')

        # set rule.style.cssText
        r.style.cssText = 'font-family: x2'
        self.assertEqual(r.style, s2)
        self.assertEqual(r, s2.parentRule)
        self.assertEqual(r.cssText, '@font-face {\n    font-family: x2\n    }')
        self.assertEqual(s2.cssText, 'font-family: x2')
        self.assertEqual(r.style.cssText, 'font-family: x2')

        # set new style object s2
        sn = css_parser.css.CSSStyleDeclaration('font-family: y1')
        r.style = sn
        self.assertEqual(r.style, sn)
        self.assertEqual(r, sn.parentRule)
        self.assertEqual(r.cssText, '@font-face {\n    font-family: y1\n    }')
        self.assertEqual(sn.cssText, 'font-family: y1')
        self.assertEqual(r.style.cssText, 'font-family: y1')
        self.assertEqual(s2.cssText, 'font-family: x2')  # old

        # set s2.cssText
        sn.cssText = 'font-family: y2'
        self.assertEqual(r.style, sn)
        self.assertEqual(r.cssText, '@font-face {\n    font-family: y2\n    }')
        self.assertEqual(r.style.cssText, 'font-family: y2')
        self.assertEqual(s2.cssText, 'font-family: x2')  # old

        # set invalid s2.cssText
        try:
            sn.cssText = '$'
        except xml.dom.SyntaxErr as e:
            pass
        self.assertEqual(r.style, sn)
        self.assertEqual(r.style.cssText, 'font-family: y2')
        self.assertEqual(r.cssText, '@font-face {\n    font-family: y2\n    }')

        # set r.style with text
        r.style = 'font-family: z'
        self.assertNotEqual(r.style, sn)
        self.assertEqual(r.cssText, '@font-face {\n    font-family: z\n    }')
        self.assertEqual(r.style.cssText, 'font-family: z')
        self.assertEqual(sn.cssText, 'font-family: y2')

    def test_properties(self):
        "CSSFontFaceRule.style properties"
        r = css_parser.css.CSSFontFaceRule()
        r.style.cssText = '''
        src: url(x)
        '''
        exp = '''@font-face {
    src: url(x)
    }'''
        self.assertEqual(exp, r.cssText)

        tests = {
            'font-family': [  # ('serif', True),
                #                            ('x', True),
                #                            ('"x"', True),
                ('x, y', False),
                ('"x", y', False),
                ('x, "y"', False),
                #                            ('"x", "y"', False)
            ]
        }
        for n, t in tests.items():
            for (v, valid) in t:
                r = css_parser.css.CSSFontFaceRule()
                r.style[n] = v
                self.assertEqual(r.style.getProperty(n).parent, r.style)
                self.assertEqual(r.style.getProperty(n).valid, valid)

    def test_incomplete(self):
        "CSSFontFaceRule (incomplete)"
        tests = {
            '@font-face{':
                '',  # no } and no content
            '@font-face { ':
                '',  # no } and no content
            '@font-face { font-family: x':
                '@font-face {\n    font-family: x\n    }',  # no }
        }
        self.do_equal_p(tests)  # parse

    def test_InvalidModificationErr(self):
        "CSSFontFaceRule.cssText InvalidModificationErr"
        self._test_InvalidModificationErr('@font-face')
        tests = {
            '@font-fac {}': xml.dom.InvalidModificationErr,
        }
        self.do_raise_r(tests)

    def test_valid(self):
        "CSSFontFaceRule.valid"
        r = css_parser.css.CSSFontFaceRule()
        self.assertEqual(False, r.valid)
        N = 'font-family: x; src: local(x);'
        tests = {
            True: (N,
                   N + 'font-style: italic; font-weight: bold',
                   ),
            False: ('',
                    'font-family: x, y; src: local(x);',
                    N + 'font-style: inherit',
                    N + 'invalid: 1')
        }
        for valid, testlist in tests.items():
            for test in testlist:
                r.style.cssText = test
                self.assertEqual(valid, r.valid)

    def test_reprANDstr(self):
        "CSSFontFaceRule.__repr__(), .__str__()"
        style = 'src: url(x)'
        s = css_parser.css.CSSFontFaceRule(style=style)

        self.assertIn(style, str(s))

        s2 = eval(repr(s))
        self.assertIsInstance(s2, s.__class__)
        self.assertEqual(style, s2.style.cssText)


if __name__ == '__main__':
    import unittest
    unittest.main()
