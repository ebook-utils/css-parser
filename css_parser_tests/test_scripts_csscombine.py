"""Testcases for css_parser.scripts.csscombine"""

from __future__ import absolute_import
from __future__ import unicode_literals
from css_parser.script import csscombine
from . import basetest
import css_parser
import os


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
        f = open(csspath, mode="rb")
        cssText = f.read()
        f.close()
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
                         '@variables{c:#0f0}a{color:var(c)}'.encode())
        self.assertEqual(csscombine(cssText=cssText),
                         'a{color:#0f0}'.encode())

        # no minify
        self.assertEqual(csscombine(cssText=cssText,
                                    minify=False,
                                    resolveVariables=False),
                         '@variables {\n    c: #0f0\n    }\na {\n    color: var(c)\n    }'.encode())
        self.assertEqual(csscombine(cssText=cssText, minify=False),
                         'a {\n    color: #0f0\n    }'.encode())


if __name__ == '__main__':
    import unittest
    unittest.main()
