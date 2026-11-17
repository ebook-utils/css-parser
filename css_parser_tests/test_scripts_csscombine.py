"""Testcases for css_parser.scripts.csscombine"""

import css_parser
from css_parser.script import csscombine

from . import basetest


class CSSCombine(basetest.BaseTestCase):

    C = '@namespace s2"uri";s2|sheet-1{top:1px}s2|sheet-2{top:2px}proxy{top:3px}'

    def setUp(self):
        self._saved = css_parser.log.raiseExceptions

    def tearDown(self):
        css_parser.log.raiseExceptions = self._saved

    def test_combine(self):
        "scripts.csscombine()"

        # path, SHOULD be keyword argument!
        csspath = basetest.get_sheet_filename('csscombine-proxy.css')
        combined = csscombine(csspath)
        self.assertEqual(combined, self.C.encode())
        combined = csscombine(path=csspath, targetencoding='ascii')
        self.assertEqual(combined, ('@charset "ascii";' + self.C).encode())

        # url
        cssurl = css_parser.helper.path2url(csspath)
        combined = csscombine(url=cssurl)
        self.assertEqual(combined, self.C.encode())
        combined = csscombine(url=cssurl, targetencoding='ascii')
        self.assertEqual(combined, ('@charset "ascii";' + self.C).encode())

        # cssText
        # TODO: really need binary or can handle str too?
        with open(csspath, mode="rb") as f:
            cssText = f.read()
        combined = csscombine(cssText=cssText, href=cssurl)
        self.assertEqual(combined, self.C.encode())
        combined = csscombine(cssText=cssText, href=cssurl,
                              targetencoding='ascii')
        self.assertEqual(combined, ('@charset "ascii";' + self.C).encode())

    def test_combine_resolveVariables(self):
        "scripts.csscombine(minify=..., resolveVariables=...)"
        # no actual imports but checking if minify and resolveVariables work
        cssText = '''
        @variables {
            c: #0f0;
        }
        a {
            color: var(c);
        }
        '''
        # default minify
        self.assertEqual(csscombine(cssText=cssText,
                                    resolveVariables=False),
                         b'@variables{c:#0f0}a{color:var(c)}')
        self.assertEqual(csscombine(cssText=cssText),
                         b'a{color:#0f0}')

        # no minify
        self.assertEqual(csscombine(cssText=cssText,
                                    minify=False,
                                    resolveVariables=False),
                         b'@variables {\n    c: #0f0\n    }\na {\n    color: var(c)\n    }')
        self.assertEqual(csscombine(cssText=cssText, minify=False),
                         b'a {\n    color: #0f0\n    }')


if __name__ == '__main__':
    import unittest
    unittest.main()
