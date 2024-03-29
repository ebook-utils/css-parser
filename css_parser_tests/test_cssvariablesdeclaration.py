"""Testcases for css_parser.css.cssvariablesdelaration.CSSVariablesDeclaration."""
from __future__ import absolute_import
from __future__ import unicode_literals
__version__ = '$Id: test_cssstyledeclaration.py 1869 2009-10-17 19:37:40Z cthedot $'

import xml.dom
from . import basetest
import css_parser


class CSSVariablesDeclarationTestCase(basetest.BaseTestCase):

    def setUp(self):
        self.r = css_parser.css.CSSVariablesDeclaration()
        css_parser.ser.prefs.useDefaults()

    def tearDown(self):
        css_parser.ser.prefs.useDefaults()

    def test_init(self):
        "CSSVariablesDeclaration.__init__()"
        v = css_parser.css.CSSVariablesDeclaration()
        self.assertEqual('', v.cssText)
        self.assertEqual(0, v.length)
        self.assertEqual(None, v.parentRule)

        v = css_parser.css.CSSVariablesDeclaration(cssText='x: 0')
        self.assertEqual('x: 0', v.cssText)
        self.assertEqual('0', v.getVariableValue('x'))

        rule = css_parser.css.CSSVariablesRule()
        v = css_parser.css.CSSVariablesDeclaration(cssText='x: 0',
                                                 parentRule=rule)
        self.assertEqual(rule, v.parentRule)

    def test__contains__(self):
        "CSSVariablesDeclaration.__contains__(name)"
        v = css_parser.css.CSSVariablesDeclaration(cssText='x: 0; y: 2')
        for test in ('x', 'y'):
            self.assertIn(test, v)
            self.assertIn(test.upper(), v)

        self.assertNotIn('z', v)

    def test_items(self):
        "CSSVariablesDeclaration[variableName]"
        v = css_parser.css.CSSVariablesDeclaration()

        value = '0'
        v['X'] = value
        self.assertEqual(value, v['X'])
        self.assertEqual(value, v.getVariableValue('X'))
        self.assertEqual(value, v['x'])
        self.assertEqual(value, v.getVariableValue('x'))

        self.assertEqual('', v['y'])
        self.assertEqual('', v.getVariableValue('y'))

        v['z'] = '1'
        self.assertEqual(2, v.length)

        items = []
        # unsorted!
        self.assertEqual(sorted(v), ['x', 'z'])

        del v['z']
        self.assertEqual(1, v.length)
        self.assertEqual(1, v.length)

        self.assertEqual('0', v.removeVariable('x'))
        self.assertEqual('', v.removeVariable('z'))
        self.assertEqual(0, v.length)

        v.cssText = 'x:0; y:1'
        keys = []
        # unsorted!
        for i in range(0, v.length):
            keys.append(v.item(i))
        self.assertEqual(sorted(keys), ['x', 'y'])

    def test_keys(self):
        "CSSVariablesDeclaration.keys()"
        v = css_parser.css.CSSVariablesDeclaration(cssText='x: 0; Y: 2')
        self.assertEqual(['x', 'y'], sorted(v.keys()))

    def test_cssText(self):
        "CSSVariablesDeclaration.cssText"
        # empty
        tests = {
            '': '',
            ' ': '',
            ' \t \n  ': '',
            'x: 1': None,
            'x: "a"': None,
            'x: rgb(1, 2, 3)': None,
            'x: 1px 2px 3px': None,

            'x:1': 'x: 1',
            'x:1;': 'x: 1',

            'x  :  1  ': 'x: 1',
            'x  :  1  ;  ': 'x: 1',

            'x:1;y:2': 'x: 1;\ny: 2',
            'x:1;y:2;': 'x: 1;\ny: 2',
            'x  :  1  ;  y  :  2  ': 'x: 1;\ny: 2',
            'x  :  1  ;  y  :  2  ;  ': 'x: 1;\ny: 2',

            '/*x*/': '/*x*/',
            'x555: 5': None,
            'xxx:1;yyy:2': 'xxx: 1;\nyyy: 2',
            'xxx : 1; yyy : 2': 'xxx: 1;\nyyy: 2',
            'x:1;x:2;X:2': 'x: 2',
            'same:1;SAME:2;': 'same: 2',
            '/**/x/**/:/**/1/**/;/**/y/**/:/**/2/**/':
                '/**/\n /**/\n /**/\n x: 1 /**/;\n/**/\n /**/\n /**/\n y: 2 /**/'
        }
        self.do_equal_r(tests)

    # TODO: Fix?
#    def test_cssText2(self):
#        "CSSVariablesDeclaration.cssText"
#        # exception
#        tests = {
#                 u'top': xml.dom.SyntaxErr,
#                 u'top:': xml.dom.SyntaxErr,
#                 u'top : ': xml.dom.SyntaxErr,
#                 u'top:;': xml.dom.SyntaxErr,
#                 u'top 0': xml.dom.SyntaxErr,
#                 u'top 0;': xml.dom.SyntaxErr,
#
#                 u':': xml.dom.SyntaxErr,
#                 u':0': xml.dom.SyntaxErr,
#                 u':0;': xml.dom.SyntaxErr,
#                 u':;': xml.dom.SyntaxErr,
#                 u': ;': xml.dom.SyntaxErr,
#
#                 u'0': xml.dom.SyntaxErr,
#                 u'0;': xml.dom.SyntaxErr,
#
#                 u';': xml.dom.SyntaxErr,
#            }
#        self.do_raise_r(tests)

    def test_xVariable(self):
        "CSSVariablesDeclaration.xVariable()"
        v = css_parser.css.CSSVariablesDeclaration()
        # unset
        self.assertEqual('', v.getVariableValue('x'))
        # set
        v.setVariable('x', '0')
        self.assertEqual('0', v.getVariableValue('x'))
        self.assertEqual('0', v.getVariableValue('X'))
        self.assertEqual('x: 0', v.cssText)
        v.setVariable('X', '0')
        self.assertEqual('0', v.getVariableValue('x'))
        self.assertEqual('0', v.getVariableValue('X'))
        self.assertEqual('x: 0', v.cssText)
        # remove
        self.assertEqual('0', v.removeVariable('x'))
        self.assertEqual('', v.removeVariable('x'))
        self.assertEqual('', v.getVariableValue('x'))
        self.assertEqual('', v.cssText)

    def test_imports(self):
        "CSSVariables imports"
        def fetcher(url):
            url = url.replace('\\', '/')
            url = url[url.rfind('/')+1:]
            return (None, {
                '3.css': '''
                    @variables {
                        over3-2-1-0: 3;
                        over3-2-1: 3;
                        over3-2: 3;
                        over3-2-0: 3;
                        over3-1: 3;
                        over3-1-0: 3;
                        over3-0: 3;
                        local3: 3;
                    }
                
                ''',
                '2.css': '''
                    @variables {
                        over3-2-1-0: 2;
                        over3-2-1: 2;
                        over3-2-0: 2;
                        over3-2: 2;
                        over2-1: 2;
                        over2-1-0: 2;
                        over2-0: 2;
                        local2: 2;
                    }
                
                ''',
                '1.css': '''
                    @import "3.css";
                    @import "2.css";
                    @variables {
                        over3-2-1-0: 1;
                        over3-2-1: 1;
                        over3-1: 1;
                        over3-1-0: 1;
                        over2-1: 1;
                        over2-1-0: 1;
                        over1-0: 1;
                        local1: 1;
                    }
                
                '''
            }[url])

        css = '''
            @import "1.css";
            @variables {
                over3-2-1-0: 0;
                over3-2-0: 0;
                over3-1-0: 0;
                over2-1-0: 0;
                over3-0: 0;
                over2-0: 0;
                over1-0: 0;
                local0: 0;
            }
            a {
                local0: var(local0);
                local1: var(local1);
                local2: var(local2);
                local3: var(local3);
                over1-0: var(over1-0);
                over2-0: var(over2-0);
                over3-0: var(over3-0);
                over2-1: var(over2-1);
                over3-1: var(over3-1);
                over3-2: var(over3-2);
                over2-1-0: var(over2-1-0);
                over3-2-0: var(over3-2-0);
                over3-2-1: var(over3-2-1);
                over3-2-1-0: var(over3-2-1-0);
            }
        '''
        p = css_parser.CSSParser(fetcher=fetcher)
        s = p.parseString(css)

        # only these in rule of this sheet
        self.assertEqual(s.cssRules[1].variables.length, 8)
        # but all vars in s available!
        self.assertEqual(s.variables.length, 15)
        self.assertEqual(['local0', 'local1', 'local2', 'local3',
                          'over1-0', 'over2-0', 'over2-1', 'over2-1-0',
                          'over3-0', 'over3-1', 'over3-1-0', 'over3-2',
                          'over3-2-0', 'over3-2-1', 'over3-2-1-0'],
                         sorted(s.variables.keys()))

        # test with variables rule
        css_parser.ser.prefs.resolveVariables = False
        self.assertEqual(s.cssText, '''@import "1.css";
@variables {
    over3-2-1-0: 0;
    over3-2-0: 0;
    over3-1-0: 0;
    over2-1-0: 0;
    over3-0: 0;
    over2-0: 0;
    over1-0: 0;
    local0: 0
    }
a {
    local0: var(local0);
    local1: var(local1);
    local2: var(local2);
    local3: var(local3);
    over1-0: var(over1-0);
    over2-0: var(over2-0);
    over3-0: var(over3-0);
    over2-1: var(over2-1);
    over3-1: var(over3-1);
    over3-2: var(over3-2);
    over2-1-0: var(over2-1-0);
    over3-2-0: var(over3-2-0);
    over3-2-1: var(over3-2-1);
    over3-2-1-0: var(over3-2-1-0)
    }'''.encode())

        # test with resolved vars
        css_parser.ser.prefs.resolveVariables = True
        self.assertEqual(s.cssText, '''@import "1.css";
a {
    local0: 0;
    local1: 1;
    local2: 2;
    local3: 3;
    over1-0: 0;
    over2-0: 0;
    over3-0: 0;
    over2-1: 1;
    over3-1: 1;
    over3-2: 2;
    over2-1-0: 0;
    over3-2-0: 0;
    over3-2-1: 1;
    over3-2-1-0: 0
    }'''.encode())

        s = css_parser.resolveImports(s)
        self.assertEqual(s.cssText, '''/* START @import "1.css" */
/* START @import "3.css" */
/* START @import "2.css" */
a {
    local0: 0;
    local1: 1;
    local2: 2;
    local3: 3;
    over1-0: 0;
    over2-0: 0;
    over3-0: 0;
    over2-1: 1;
    over3-1: 1;
    over3-2: 2;
    over2-1-0: 0;
    over3-2-0: 0;
    over3-2-1: 1;
    over3-2-1-0: 0
    }'''.encode())

    def test_parentRule(self):
        "CSSVariablesDeclaration.parentRule"
        s = css_parser.parseString('@variables { a:1}')
        r = s.cssRules[0]
        d = r.variables
        self.assertEqual(r, d.parentRule)

        d2 = css_parser.css.CSSVariablesDeclaration('b: 2')
        r.variables = d2
        self.assertEqual(r, d2.parentRule)

    def test_reprANDstr(self):
        "CSSVariablesDeclaration.__repr__(), .__str__()"
        s = css_parser.css.CSSVariablesDeclaration(cssText='a:1;b:2')

        self.assertIn('2', str(s)) # length

        s2 = eval(repr(s))
        self.assertIsInstance(s2, s.__class__)


if __name__ == '__main__':
    import unittest
    unittest.main()
