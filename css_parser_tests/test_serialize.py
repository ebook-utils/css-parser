# -*- coding: utf-8 -*-
"""Testcases for css_parser.CSSSerializer"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import basetest
import css_parser


class PreferencesTestCase(basetest.BaseTestCase):
    """
    testcases for css_parser.serialize.Preferences
    """

    def setUp(self):
        css_parser.ser.prefs.useDefaults()

    def tearDown(self):
        css_parser.ser.prefs.useDefaults()

#    def testkeepUnkownAtRules(self):
#        "Preferences.keepUnkownAtRules"
#        # py >=2.6 only
#        # v = sys.version_info; if v[0]*10+v[1] >= 26:
#        from warnings import catch_warnings
#        with catch_warnings(record=True) as log:
#            x = css_parser.ser.prefs.keepUnkownAtRules
#
#        if log:
#            # unpack the only member of log
#            warning, = log
#            self.assertEqual(warning.category, DeprecationWarning)

    def test_resolveVariables(self):
        "Preferences.resolveVariables"
        self.assertEqual(css_parser.ser.prefs.resolveVariables, True)

        css_parser.ser.prefs.resolveVariables = False

        vars = '''
            @variables {
                c1: red;
                c2: #0f0;
                px: 1px 2px;
            }
        '''
        tests = {
            '''a {\n    color: var(c1)\n    }''':
            '''a {\n    color: red\n    }''',
            '''a {\n    color: var(c1)\n; color: var(  c2   )    }''':
            '''a {\n    color: red;\n    color: #0f0\n    }''',
            '''a {\n    margin: var(px)\n    }''':
            '''a {\n    margin: 1px 2px\n    }''',
            '''@media all {
                a {
                    margin: var(px) var(px);
                    color: var(c1);
                    left: var(unknown)
                    }
            }''':
            '''@media all {\n    a {\n        margin: 1px 2px 1px 2px;\n        color: red;\n        left: var(unknown)\n        }\n    }''',
        }
        css_parser.ser.prefs.resolveVariables = True

        for test, exp in tests.items():
            s = css_parser.parseString(vars + test)
            self.assertEqual(exp.encode(), s.cssText)

        css_parser.ser.prefs.resolveVariables = True

    def test_useDefaults(self):
        "Preferences.useDefaults()"
        css_parser.ser.prefs.useMinified()
        css_parser.ser.prefs.useDefaults()
        self.assertEqual(css_parser.ser.prefs.defaultAtKeyword, True)
        self.assertEqual(css_parser.ser.prefs.defaultPropertyName, True)
        self.assertEqual(css_parser.ser.prefs.defaultPropertyPriority, True)
        self.assertEqual(css_parser.ser.prefs.formatUnknownAtRules, True)
        self.assertEqual(css_parser.ser.prefs.importHrefFormat, None)
        self.assertEqual(css_parser.ser.prefs.indent, 4 * ' ')
        self.assertEqual(css_parser.ser.prefs.indentClosingBrace, True)
        self.assertEqual(css_parser.ser.prefs.keepAllProperties, True)
        self.assertEqual(css_parser.ser.prefs.keepComments, True)
        self.assertEqual(css_parser.ser.prefs.keepEmptyRules, False)
        self.assertEqual(css_parser.ser.prefs.keepUnknownAtRules, True)
        self.assertEqual(css_parser.ser.prefs.keepUsedNamespaceRulesOnly, False)
        self.assertEqual(css_parser.ser.prefs.lineNumbers, False)
        self.assertEqual(css_parser.ser.prefs.lineSeparator, '\n')
        self.assertEqual(css_parser.ser.prefs.linesAfterRules, 0 * css_parser.ser.prefs.lineSeparator)
        self.assertEqual(css_parser.ser.prefs.listItemSpacer, ' ')
        self.assertEqual(css_parser.ser.prefs.minimizeColorHash, True)
        self.assertEqual(css_parser.ser.prefs.omitLastSemicolon, True)
        self.assertEqual(css_parser.ser.prefs.omitLeadingZero, False)
        self.assertEqual(css_parser.ser.prefs.paranthesisSpacer, ' ')
        self.assertEqual(css_parser.ser.prefs.propertyNameSpacer, ' ')
        self.assertEqual(css_parser.ser.prefs.selectorCombinatorSpacer, ' ')
        self.assertEqual(css_parser.ser.prefs.spacer, ' ')
        self.assertEqual(css_parser.ser.prefs.validOnly, False)
        css = '''
    /*1*/
    @import url(x) tv , print;
    @namespace prefix "uri";
    @namespace unused "unused";
    @media all {}
    @media all {
        a {}
    }
    @media   all  {
    a { color: red; }
        }
    @page     { left: 0; }
    a {}
    prefix|x, a  +  b  >  c  ~  d  ,  b { top : 1px ;
        font-family : arial ,'some'
        }
    '''
        parsedcss = '''/*1*/
@import url(x) tv, print;
@namespace prefix "uri";
@namespace unused "unused";
@media all {
    a {
        color: red
        }
    }
@page {
    left: 0
    }
prefix|x, a + b > c ~ d, b {
    top: 1px;
    font-family: arial, "some"
    }'''
        s = css_parser.parseString(css)
        self.assertEqual(s.cssText, parsedcss.encode())

        tests = {
            '0.1 .1 0.1px .1px 0.1% .1% +0.1 +.1 +0.1px +.1px +0.1% +.1% -0.1 -.1 -0.1px -.1px -0.1% -.1%':
            '0.1 0.1 0.1px 0.1px 0.1% 0.1% +0.1 +0.1 +0.1px +0.1px +0.1% +0.1% -0.1 -0.1 -0.1px -0.1px -0.1% -0.1%'
        }
        css_parser.ser.prefs.useDefaults()
        for test, exp in tests.items():
            s = css_parser.parseString('a{x:%s}' % test)
            self.assertEqual(('a {\n    x: %s\n    }' % exp).encode(), s.cssText)

    def test_useMinified(self):
        "Preferences.useMinified()"
        css_parser.ser.prefs.useDefaults()
        css_parser.ser.prefs.useMinified()
        self.assertEqual(css_parser.ser.prefs.defaultAtKeyword, True)
        self.assertEqual(css_parser.ser.prefs.defaultPropertyName, True)
        self.assertEqual(css_parser.ser.prefs.importHrefFormat, 'string')
        self.assertEqual(css_parser.ser.prefs.indent, '')
        self.assertEqual(css_parser.ser.prefs.keepAllProperties, True)
        self.assertEqual(css_parser.ser.prefs.keepComments, False)
        self.assertEqual(css_parser.ser.prefs.keepEmptyRules, False)
        self.assertEqual(css_parser.ser.prefs.keepUnknownAtRules, False)
        self.assertEqual(css_parser.ser.prefs.keepUsedNamespaceRulesOnly, True)
        self.assertEqual(css_parser.ser.prefs.lineNumbers, False)
        self.assertEqual(css_parser.ser.prefs.lineSeparator, '')
        self.assertEqual(css_parser.ser.prefs.listItemSpacer, '')
        self.assertEqual(css_parser.ser.prefs.omitLastSemicolon, True)
        self.assertEqual(css_parser.ser.prefs.omitLeadingZero, True)
        self.assertEqual(css_parser.ser.prefs.paranthesisSpacer, '')
        self.assertEqual(css_parser.ser.prefs.propertyNameSpacer, '')
        self.assertEqual(css_parser.ser.prefs.selectorCombinatorSpacer, '')
        self.assertEqual(css_parser.ser.prefs.spacer, '')
        self.assertEqual(css_parser.ser.prefs.validOnly, False)

        css = '''
    /*1*/
    @import   url(x) tv , print;
    @namespace   prefix "uri";
    @namespace   unused "unused";
    @media  all {}
    @media  all {
        a {}
    }
    @media all "name" {
        a { color: red; }
    }
    @page:left {
    left: 0
    }
    a {}
    prefix|x, a + b > c ~ d , b { top : 1px ;
        font-family : arial ,  'some'
        }
    @x  x;
    '''
        s = css_parser.parseString(css)
        css_parser.ser.prefs.keepUnknownAtRules = True
        self.assertEqual(s.cssText,
                         '''@import"x"tv,print;@namespace prefix"uri";@media all"name"{a{color:red}}@page :left{left:0}prefix|x,a+b>c~d,b{top:1px;font-family:arial,"some"}@x x;'''.encode(
                         )
                         )
        css_parser.ser.prefs.keepUnknownAtRules = False
        self.assertEqual(s.cssText,
                         '''@import"x"tv,print;@namespace prefix"uri";@media all"name"{a{color:red}}@page :left{left:0}prefix|x,a+b>c~d,b{top:1px;font-family:arial,"some"}'''.encode(
                         )
                         )
        # Values
        valuetests = {
            '  a  a1  a-1  a-1a  ': 'a a1 a-1 a-1a',
            'a b 1 c 1em d -1em e': 'a b 1 c 1em d -1em e',
            '  1em  /  5  ': '1em/5',
            '1em/5': '1em/5',
            'a 0 a .0 a 0.0 a -0 a -.0 a -0.0 a +0 a +.0 a +0.0':
                'a 0 a 0 a 0 a 0 a 0 a 0 a 0 a 0 a 0',
            'a  0px  a  .0px  a  0.0px  a  -0px  a  -.0px  a  -0.0px  a  +0px  a  +.0px  a  +0.0px ':
                'a 0 a 0 a 0 a 0 a 0 a 0 a 0 a 0 a 0',
            'a  1  a  .1  a  1.0  a  0.1  a  -1  a  -.1  a  -1.0  a  -0.1  a  +1  a  +.1  a  +1.0':
                'a 1 a .1 a 1 a .1 a -1 a -.1 a -1 a -.1 a +1 a +.1 a +1',
            '  url(x)  f()': 'url(x) f()',
            '#112233': '#123',
            '#112234': '#112234',
            '#123': '#123',
            '#123 url() f()': '#123 url() f()',
            '1 +2 +3 -4': '1 +2 +3 -4',  # ?
            '0.1 .1 0.1px .1px 0.1% .1% +0.1 +.1 +0.1px +.1px +0.1% +.1% -0.1 -.1 -0.1px -.1px -0.1% -.1%':
            '.1 .1 .1px .1px .1% .1% +.1 +.1 +.1px +.1px +.1% +.1% -.1 -.1 -.1px -.1px -.1% -.1%'
        }
        for test, exp in valuetests.items():
            s = css_parser.parseString('a{x:%s}' % test)
            self.assertEqual(('a{x:%s}' % exp).encode(), s.cssText)

    def test_defaultAtKeyword(self):
        "Preferences.defaultAtKeyword"
        s = css_parser.parseString('@im\\port "x";')
        self.assertEqual('@import "x";'.encode(), s.cssText)
        css_parser.ser.prefs.defaultAtKeyword = True
        self.assertEqual('@import "x";'.encode(), s.cssText)
        css_parser.ser.prefs.defaultAtKeyword = False
        self.assertEqual('@im\\port "x";'.encode(), s.cssText)

    def test_defaultPropertyName(self):
        "Preferences.defaultPropertyName"
        css_parser.ser.prefs.keepAllProperties = False

        # does not actually work as once the name is set it is used also
        # if used with a backslash in it later...

        s = css_parser.parseString(r'a { c\olor: green; }')
        self.assertEqual('a {\n    color: green\n    }'.encode(), s.cssText)
        css_parser.ser.prefs.defaultPropertyName = True
        self.assertEqual('a {\n    color: green\n    }'.encode(), s.cssText)
        css_parser.ser.prefs.defaultPropertyName = False
        self.assertEqual('a {\n    c\\olor: green\n    }'.encode(), s.cssText)

        s = css_parser.parseString(r'a { color: red; c\olor: green; }')
        self.assertEqual('a {\n    c\\olor: green\n    }'.encode(), s.cssText)
        css_parser.ser.prefs.defaultPropertyName = False
        self.assertEqual('a {\n    c\\olor: green\n    }'.encode(), s.cssText)
        css_parser.ser.prefs.defaultPropertyName = True
        self.assertEqual('a {\n    color: green\n    }'.encode(), s.cssText)

    def test_defaultPropertyPriority(self):
        "Preferences.defaultPropertyPriority"
        css = 'a {\n    color: green !IM\\portant\n    }'
        s = css_parser.parseString(css)
        self.assertEqual(s.cssText, 'a {\n    color: green !important\n    }'.encode())
        css_parser.ser.prefs.defaultPropertyPriority = False
        self.assertEqual(s.cssText, css.encode())

    def test_formatUnknownAtRules(self):
        "Preferences.formatUnknownAtRules"
        css = '@meda screen and (max-width: 100px) { .someclass { color: blue } }'
        formatted = '''\
@meda screen and (max-width: 100px) {
    . someclass {
        color: blue
        }
    }'''
        s = css_parser.parseString(css)
        self.assertEqual(s.cssText, formatted.encode())
        css_parser.ser.prefs.formatUnknownAtRules = False
        self.assertEqual(s.cssText, css.encode())
        css = '@meda screen and (max-width: 100px) { /*comm*/ .someclass { color: blue /* comm */ } }'
        s = css_parser.parseString(css)
        self.assertEqual(s.cssText, css.encode())

    def test_importHrefFormat(self):
        "Preferences.importHrefFormat"
        r0 = css_parser.css.CSSImportRule()
        r0.cssText = '@import url("not");'
        r1 = css_parser.css.CSSImportRule()
        r1.cssText = '@import "str";'
        self.assertEqual('@import url(not);', r0.cssText)
        self.assertEqual('@import "str";', r1.cssText)

        css_parser.ser.prefs.importHrefFormat = 'string'
        self.assertEqual('@import "not";', r0.cssText)
        self.assertEqual('@import "str";', r1.cssText)

        css_parser.ser.prefs.importHrefFormat = 'uri'
        self.assertEqual('@import url(not);', r0.cssText)
        self.assertEqual('@import url(str);', r1.cssText)

        css_parser.ser.prefs.importHrefFormat = 'not defined'
        self.assertEqual('@import url(not);', r0.cssText)
        self.assertEqual('@import "str";', r1.cssText)

    def test_indent(self):
        "Preferences.ident"
        s = css_parser.parseString('a { left: 0 }')
        exp4 = '''a {
    left: 0
    }'''
        exp1 = '''a {
 left: 0
 }'''
        css_parser.ser.prefs.indent = ' '
        self.assertEqual(exp1.encode(), s.cssText)
        css_parser.ser.prefs.indent = 4 * ' '
        self.assertEqual(exp4.encode(), s.cssText)

    def test_indentClosingBrace(self):
        "Preferences.indentClosingBrace"
        s = css_parser.parseString('@media all {a {left: 0}}'
                                   'b { top: 0 }'
                                   '@page { @top-left { content: "some content" } margin: .5em }'
                                   '@font-face { font-family: examplefont; }')
        expT = '''\
@media all {
    a {
        left: 0
        }
    }
b {
    top: 0
    }
@page {
    margin: 0.5em;
    @top-left {
        content: "some content"
        }
    }
@font-face {
    font-family: examplefont
    }'''
        expF = '''\
@media all {
    a {
        left: 0
    }
}
b {
    top: 0
}
@page {
    margin: 0.5em;
    @top-left {
        content: "some content"
    }
}
@font-face {
    font-family: examplefont
}'''
        css_parser.ser.prefs.useDefaults()
        self.assertEqual(expT.encode(), s.cssText)
        css_parser.ser.prefs.indentClosingBrace = False
        self.assertEqual(expF.encode(), s.cssText)

    def test_keepAllProperties(self):
        "Preferences.keepAllProperties"
        css = r'''a {
            color: pink;
            color: red;
            c\olor: blue;
            c\olor: green;
            }'''
        s = css_parser.parseString(css)
        # keep only last
        css_parser.ser.prefs.keepAllProperties = False
        self.assertEqual('a {\n    color: green\n    }'.encode(), s.cssText)
        # keep all
        css_parser.ser.prefs.keepAllProperties = True
        self.assertEqual(
            'a {\n    color: pink;\n    color: red;\n    c\\olor: blue;\n    c\\olor: green\n    }'.encode(), s.cssText)

    def test_keepComments(self):
        "Preferences.keepComments"
        s = css_parser.parseString('/*1*/ a { /*2*/ }')
        css_parser.ser.prefs.keepComments = False
        self.assertEqual(''.encode(), s.cssText)
        css_parser.ser.prefs.keepEmptyRules = True
        self.assertEqual('a {}'.encode(), s.cssText)

    def test_keepEmptyRules(self):
        "Preferences.keepEmptyRules"
        # CSSStyleRule
        css = '''a {}
a {
    /*1*/
    }
a {
    color: red
    }'''
        s = css_parser.parseString(css)
        css_parser.ser.prefs.useDefaults()
        css_parser.ser.prefs.keepEmptyRules = True
        self.assertEqual(css.encode(), s.cssText)
        css_parser.ser.prefs.keepEmptyRules = False
        self.assertEqual('a {\n    /*1*/\n    }\na {\n    color: red\n    }'.encode(),
                         s.cssText)
        css_parser.ser.prefs.keepComments = False
        self.assertEqual('a {\n    color: red\n    }'.encode(), s.cssText)

        # CSSMediaRule
        css = '''@media tv {
    }
@media all {
    /*1*/
    }
@media print {
    a {}
    }
@media print {
    a {
        /*1*/
        }
    }
@media all {
    a {
        color: red
        }
    }'''
        s = css_parser.parseString(css)
        css_parser.ser.prefs.useDefaults()
        css_parser.ser.prefs.keepEmptyRules = True
        self.assertEqual(css.encode(), s.cssText)
        css_parser.ser.prefs.keepEmptyRules = False
        self.assertEqual('''@media all {
    /*1*/
    }
@media print {
    a {
        /*1*/
        }
    }
@media all {
    a {
        color: red
        }
    }'''.encode(), s.cssText)
        css_parser.ser.prefs.keepComments = False
        self.assertEqual('''@media all {
    a {
        color: red
        }
    }'''.encode(), s.cssText)

    def test_keepUnknownAtRules(self):
        "Preferences.keepUnknownAtRules"
        tests = {
            '''@three-dee {
              @background-lighting {
                azimuth: 30deg;
                elevation: 190deg;
              }
              h1 { color: red }
            }
            h1 { color: blue }''': ('''@three-dee {
    @background-lighting {
        azimuth: 30deg;
        elevation: 190deg;
        } h1 {
        color: red
        }
    }
h1 {
    color: blue
    }''', '''h1 {
    color: blue
    }''')
        }
        for test in tests:
            s = css_parser.parseString(test)
            expwith, expwithout = tests[test]
            css_parser.ser.prefs.keepUnknownAtRules = True
            self.assertEqual(s.cssText, expwith.encode())
            css_parser.ser.prefs.keepUnknownAtRules = False
            self.assertEqual(s.cssText, expwithout.encode())

    def test_keepUsedNamespaceRulesOnly(self):
        "Preferences.keepUsedNamespaceRulesOnly"
        tests = {
            # default == prefix => both are combined
            '@namespace p "u"; @namespace "u"; p|a, a {top: 0}':
                ('@namespace "u";\na, a {\n    top: 0\n    }',
                 '@namespace "u";\na, a {\n    top: 0\n    }'),
            '@namespace "u"; @namespace p "u"; p|a, a {top: 0}':
                ('@namespace p "u";\np|a, p|a {\n    top: 0\n    }',
                 '@namespace p "u";\np|a, p|a {\n    top: 0\n    }'),
            # default and prefix
            '@namespace p "u"; @namespace "d"; p|a, a {top: 0}':
                ('@namespace p "u";\n@namespace "d";\np|a, a {\n    top: 0\n    }',
                 '@namespace p "u";\n@namespace "d";\np|a, a {\n    top: 0\n    }'),
            # prefix only
            '@namespace p "u"; @namespace "d"; p|a {top: 0}':
                ('@namespace p "u";\n@namespace "d";\np|a {\n    top: 0\n    }',
                 '@namespace p "u";\np|a {\n    top: 0\n    }'),
            # default only
            '@namespace p "u"; @namespace "d"; a {top: 0}':
                ('@namespace p "u";\n@namespace "d";\na {\n    top: 0\n    }',
                 '@namespace "d";\na {\n    top: 0\n    }'),
            # prefix-ns only
            '@namespace p "u"; @namespace d "d"; p|a {top: 0}':
                ('@namespace p "u";\n@namespace d "d";\np|a {\n    top: 0\n    }',
                 '@namespace p "u";\np|a {\n    top: 0\n    }'),
        }
        for test in tests:
            s = css_parser.parseString(test)
            expwith, expwithout = tests[test]
            css_parser.ser.prefs.keepUsedNamespaceRulesOnly = False
            self.assertEqual(s.cssText, expwith.encode())
            css_parser.ser.prefs.keepUsedNamespaceRulesOnly = True
            self.assertEqual(s.cssText, expwithout.encode())

    def test_lineNumbers(self):
        "Preferences.lineNumbers"

        s = css_parser.parseString('a {top: 1; left: 2}')
        exp0 = '''a {
    top: 1;
    left: 2
    }'''
        exp1 = '''1: a {
2:     top: 1;
3:     left: 2
4:     }'''
        self.assertEqual(False, css_parser.ser.prefs.lineNumbers)
        self.assertEqual(exp0.encode(), s.cssText)
        css_parser.ser.prefs.lineNumbers = True
        self.assertEqual(True, css_parser.ser.prefs.lineNumbers)
        self.assertEqual(exp1.encode(), s.cssText)

    def test_lineSeparator(self):
        "Preferences.lineSeparator"
        s = css_parser.parseString('a { x:1;y:2}')
        self.assertEqual('a {\n    x: 1;\n    y: 2\n    }'.encode(), s.cssText)
        # cannot be indented as no split possible
        css_parser.ser.prefs.lineSeparator = ''
        self.assertEqual('a {x: 1;y: 2    }'.encode(), s.cssText)
        # no valid css but should work
        css_parser.ser.prefs.lineSeparator = 'XXX'
        self.assertEqual('a {XXX    x: 1;XXX    y: 2XXX    }'.encode(), s.cssText)

    def test_linesAfterRule(self):
        "Preferences.linesAfterRule"
        s = css_parser.parseString('div {color:red;} @media screen {.aclass {width: 200px}}')
        expected_default = '''\
div {
    color: red
    }
@media screen {
    .aclass {
        width: 200px
        }
    }'''
        self.assertEqual(expected_default.encode(), s.cssText)
        css_parser.ser.prefs.linesAfterRules = 1 * '\n'
        expected_changed = '''\
div {
    color: red
    }

@media screen {
    .aclass {
        width: 200px
        }
    }
'''
        self.assertEqual(expected_changed.encode(), s.cssText)

    def test_listItemSpacer(self):
        "Preferences.listItemSpacer"
        css_parser.ser.prefs.keepEmptyRules = True

        css = '''
        @import "x" print, tv;
a, b {}'''
        s = css_parser.parseString(css)
        self.assertEqual('@import "x" print, tv;\na, b {}'.encode(), s.cssText)
        css_parser.ser.prefs.listItemSpacer = ''
        self.assertEqual('@import "x" print,tv;\na,b {}'.encode(), s.cssText)

    def test_minimizeColorHash(self):
        "Preferences.minimizeColorHash"
        css = 'a { color: #ffffff }'
        s = css_parser.parseString(css)
        self.assertEqual('a {\n    color: #fff\n    }'.encode(), s.cssText)
        css_parser.ser.prefs.minimizeColorHash = False
        self.assertEqual('a {\n    color: #ffffff\n    }'.encode(), s.cssText)

    def test_omitLastSemicolon(self):
        "Preferences.omitLastSemicolon"
        css = 'a { x: 1; y: 2 }'
        s = css_parser.parseString(css)
        self.assertEqual('a {\n    x: 1;\n    y: 2\n    }'.encode(), s.cssText)
        css_parser.ser.prefs.omitLastSemicolon = False
        self.assertEqual('a {\n    x: 1;\n    y: 2;\n    }'.encode(), s.cssText)

    def test_normalizedVarNames(self):
        "Preferences.normalizedVarNames"
        css_parser.ser.prefs.resolveVariables = False

        css = '@variables { A: 1 }'
        s = css_parser.parseString(css)
        self.assertEqual('@variables {\n    a: 1\n    }'.encode(), s.cssText)
        css_parser.ser.prefs.normalizedVarNames = False
        self.assertEqual('@variables {\n    A: 1\n    }'.encode(), s.cssText)

        css_parser.ser.prefs.resolveVariables = True

    def test_paranthesisSpacer(self):
        "Preferences.paranthesisSpacer"
        css = 'a { x: 1; y: 2 }'
        s = css_parser.parseString(css)
        self.assertEqual('a {\n    x: 1;\n    y: 2\n    }'.encode(), s.cssText)
        css_parser.ser.prefs.paranthesisSpacer = ''
        self.assertEqual('a{\n    x: 1;\n    y: 2\n    }'.encode(), s.cssText)

    def test_propertyNameSpacer(self):
        "Preferences.propertyNameSpacer"
        css = 'a { x: 1; y: 2 }'
        s = css_parser.parseString(css)
        self.assertEqual('a {\n    x: 1;\n    y: 2\n    }'.encode(), s.cssText)
        css_parser.ser.prefs.propertyNameSpacer = ''
        self.assertEqual('a {\n    x:1;\n    y:2\n    }'.encode(), s.cssText)

    def test_selectorCombinatorSpacer(self):
        "Preferences.selectorCombinatorSpacer"
        s = css_parser.css.Selector(selectorText='a+b>c~d  e')
        self.assertEqual('a + b > c ~ d e', s.selectorText)
        css_parser.ser.prefs.selectorCombinatorSpacer = ''
        self.assertEqual('a+b>c~d e', s.selectorText)

    def test_spacer(self):
        css_parser.ser.prefs.spacer = ''
        tests = {
            '@font-face {a:1}': '@font-face {\n    a: 1\n    }',
            '@import  url( a );': '@import url(a);',
            '@media  all{a{color:red}}': '@media all {\n    a {\n        color: red\n        }\n    }',
            '@namespace "a";': '@namespace"a";',
            '@namespace a  "a";': '@namespace a"a";',
            '@page  :left {   a  :1  }': '@page :left {\n    a: 1\n    }',
            '@x  x;': '@x x;',
            '@import"x"tv': '@import"x"tv;'  # ?
        }
        for css, exp in tests.items():
            self.assertEqual(exp.encode(), css_parser.parseString(css).cssText)

    def test_validOnly(self):
        "Preferences.validOnly"
        # Property
        p = css_parser.css.Property('color', '1px')
        self.assertEqual(p.cssText, 'color: 1px')
        p.value = '1px'
        css_parser.ser.prefs.validOnly = True
        self.assertEqual(p.cssText, '')
        css_parser.ser.prefs.validOnly = False
        self.assertEqual(p.cssText, 'color: 1px')

        # CSSStyleDeclaration has no actual property valid
        # but is empty if containing invalid Properties only
        s = css_parser.css.CSSStyleDeclaration()
        s.cssText = 'left: x;top: x'
        self.assertEqual(s.cssText, 'left: x;\ntop: x')
        css_parser.ser.prefs.validOnly = True
        self.assertEqual(s.cssText, '')

        css_parser.ser.prefs.useDefaults()
        css_parser.ser.prefs.keepComments = False
        css_parser.ser.prefs.validOnly = True
        tests = {
            'h1 { color: red; rotation: 70minutes }': 'h1 {\n    color: red;\n    }',
            '''img { float: left }       /* correct CSS 2.1 */
img { float: left here }  /* "here" is not a value of 'float' */
img { background: "red" } /* keywords cannot be quoted */
img { border-width: 3 }   /* a unit must be specified for length values */''': 'img {\n    float: left\n    }'

        }
        self.do_equal_p(tests, raising=False)


class CSSSerializerTestCase(basetest.BaseTestCase):
    """
    testcases for css_parser.CSSSerializer
    """

    def setUp(self):
        css_parser.ser.prefs.useDefaults()

    def tearDown(self):
        css_parser.ser.prefs.useDefaults()

    def test_canonical(self):
        tests = {
            '''1''': '''1''',
            # => remove +
            '''+1''': '''+1''',
            # 0 => remove unit
            '''0''': '''0''',
            '''+0''': '''0''',
            '''-0''': '''0''',
            '''0.0''': '''0''',
            '''00.0''': '''0''',
            '''00.0px''': '''0''',
            '''00.0pc''': '''0''',
            '''00.0em''': '''0''',
            '''00.0ex''': '''0''',
            '''00.0cm''': '''0''',
            '''00.0mm''': '''0''',
            '''00.0in''': '''0''',
            # 0 => keep unit
            '''00.0%''': '''0%''',
            '''00.0ms''': '''0ms''',
            '''00.0s''': '''0s''',
            '''00.0khz''': '''0khz''',
            '''00.0hz''': '''0hz''',
            '''00.0khz''': '''0khz''',
            '''00.0deg''': '''0deg''',
            '''00.0rad''': '''0rad''',
            '''00.0grad''': '''0grad''',
            '''00.0xx''': '''0xx''',
            # 11.
            '''a, 'b"', serif''': r'''a, "b\"", serif''',
            # SHOULD: \[ => [ but keep!
            r"""url('h)i') '\[\]'""": r'''url("h)i") "\[\]"''',
            '''rgb(18, 52, 86)''': '''rgb(18, 52, 86)''',
            '''#123456''': '''#123456''',
            # SHOULD => #112233
            '''#112233''': '''#123''',
            # SHOULD => #000000
            #            u'rgba(000001, 0, 0, 1)': u'#000'
        }
        for test, exp in tests.items():
            v = css_parser.css.PropertyValue(test)
            self.assertEqual(exp, v.cssText)

    def test_CSSStyleSheet(self):
        "CSSSerializer.do_CSSStyleSheet"
        css = '/* κουρος */'
        sheet = css_parser.parseString(css)
        ans = sheet.cssText
        if isinstance(ans, bytes):
            ans = ans.decode('utf-8')
        self.assertEqual(css, ans)

        css = '@charset "utf-8";\n/* κουρος */'
        sheet = css_parser.parseString(css)
        ans = sheet.cssText
        if isinstance(ans, bytes):
            ans = ans.decode('utf-8')
        self.assertEqual(css, ans)
        sheet.cssRules[0].encoding = 'ascii'
        self.assertEqual('@charset "ascii";\n/* \\3BA \\3BF \\3C5 \\3C1 \\3BF \\3C2  */'.encode(),
                         sheet.cssText)

    def test_Property(self):
        "CSSSerializer.do_Property"

        name = "color"
        value = "red"
        priority = "!important"

        s = css_parser.css.property.Property(
            name=name, value=value, priority=priority)
        self.assertEqual('color: red !important',
                         css_parser.ser.do_Property(s))

        s = css_parser.css.property.Property(
            name=name, value=value)
        self.assertEqual('color: red',
                         css_parser.ser.do_Property(s))

    def test_escapestring(self):
        "CSSSerializer._escapestring"
        # '"\a\22\27"'
        css = r'''@import url("ABC\a");
@import "ABC\a";
@import 'ABC\a';
a[href='"\a\22\27"'] {
    a: "\a\d\c";
    b: "\a \d \c ";
    c: "\"";
    d: "\22";
    e: '\'';
    f: "\\";
    g: "2\\ 1\ 2\\";
    content: '\27';
    }'''
#        exp = ur'''@import url("ABC\a ");
# @import "ABC\a";
# @import "ABC\a";
# a[href="\"\a\22\27\""] {
#    a: "\a\d\c";
#    b: "\a \d \c ";
#    c: "\"";
#    d: "\22";
#    e: "'";
#    f: "\\";
#    g: "2\\ 1\ 2\\";
#    content: "\27"
#    }'''
        exp = r'''@import url("ABC\a ");
@import "ABC\a ";
@import "ABC\a ";
a[href="\"\a \"'\""] {
    a: "\a \d \c ";
    b: "\a \d \c ";
    c: "\"";
    d: "\"";
    e: "'";
    f: "\\";
    g: "2\\ 1\ 2\\";
    content: "'"
    }'''
        sheet = css_parser.parseString(css)
        self.assertEqual(sheet.cssText, exp.encode())


if __name__ == '__main__':
    import unittest
    unittest.main()
