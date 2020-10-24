# -*- coding: utf-8 -*-
"""Testcases for css_parser.css.CSSCharsetRule"""
from __future__ import with_statement, unicode_literals

from __future__ import absolute_import
from . import basetest
import codecs
import css_parser
import os
import sys
import tempfile


class CSSutilsTestCase(basetest.BaseTestCase):
    def setUp(self):
        css_parser.ser.prefs.useDefaults()

    def tearDown(self):
        css_parser.ser.prefs.useDefaults()

    exp = '''@import "import/import2.css";
.import {
    /* ./import.css */
    background-image: url(images/example.gif)
    }'''

    def test_import_from_above(self):
        def fetch(url):
            self.assertEqual(url, '../test2.css')
            return None, ''

        p = css_parser.CSSParser(fetcher=fetch)
        s = p.parseString("@import url('../test2.css'); a { background-image: url(../test.jpg); }", href='test.css')
        self.assertEqual(
            s.cssRules[1].style.getPropertyCSSValue('background-image')[0].absoluteUri,
            '../test.jpg'
        )

        def fetch2(url):
            self.assertEqual(url, 'a/test2.css')
            return None, ''

        p = css_parser.CSSParser(fetcher=fetch2)
        s = p.parseString("@import url('../test2.css'); a { background-image: url(../test.jpg); }", href='a/b/test.css')
        self.assertEqual(
            s.cssRules[1].style.getPropertyCSSValue('background-image')[0].absoluteUri,
            'a/test.jpg'
        )

    def test_parseString(self):
        "css_parser.parseString()"
        s = css_parser.parseString(
            self.exp, media='handheld, screen', title='from string')
        self.assertTrue(isinstance(s, css_parser.css.CSSStyleSheet))
        self.assertEqual(None, s.href)
        self.assertEqual(self.exp.encode(), s.cssText)
        self.assertEqual('utf-8', s.encoding)
        self.assertEqual('handheld, screen', s.media.mediaText)
        self.assertEqual('from string', s.title)
        self.assertEqual(self.exp.encode(), s.cssText)

        ir = s.cssRules[0]
        self.assertEqual('import/import2.css', ir.href)
        irs = ir.styleSheet
        self.assertEqual(css_parser.css.CSSStyleSheet, type(irs))

        href = basetest.get_sheet_filename('import.css')
        href = css_parser.helper.path2url(href)
        s = css_parser.parseString(self.exp, href=href)
        self.assertEqual(href, s.href)

        ir = s.cssRules[0]
        self.assertEqual('import/import2.css', ir.href)
        irs = ir.styleSheet
        self.assertTrue(isinstance(irs, css_parser.css.CSSStyleSheet))
        self.assertEqual(
            irs.cssText,
            '@import "../import3.css";\n@import "import-impossible.css" print;\n.import2 {\n    /* sheets/import2.css */\n    background: url(http://example.com/images/example.gif);\n    background: url(//example.com/images/example.gif);\n    background: url(/images/example.gif);\n    background: url(images2/example.gif);\n    background: url(./images2/example.gif);\n    background: url(../images/example.gif);\n    background: url(./../images/example.gif)\n    }'  # noqa
            .encode())

        tests = {
            'a {color: red}': 'a {\n    color: red\n    }',
            'a {color: rgb(1,2,3)}': 'a {\n    color: rgb(1, 2, 3)\n    }'
        }
        self.do_equal_p(tests)

    def test_parseFile(self):
        "css_parser.parseFile()"
        # name if used with open, href used for @import resolving
        name = basetest.get_sheet_filename('import.css')
        href = css_parser.helper.path2url(name)
        s = css_parser.parseFile(
            name, href=href, media='screen', title='from file')
        self.assertTrue(isinstance(s, css_parser.css.CSSStyleSheet))
        if sys.platform.startswith('java'):
            # on Jython only file:
            self.assertTrue(s.href.startswith('file:'))
        else:
            # normally file:/// on win and file:/ on unix
            self.assertTrue(s.href.startswith('file:/'))
        self.assertTrue(s.href.endswith('/sheets/import.css'))
        self.assertEqual('utf-8', s.encoding)
        self.assertEqual('screen', s.media.mediaText)
        self.assertEqual('from file', s.title)
        self.assertEqual(self.exp.encode(), s.cssText)

        ir = s.cssRules[0]
        self.assertEqual('import/import2.css', ir.href)
        irs = ir.styleSheet
        self.assertTrue(isinstance(irs, css_parser.css.CSSStyleSheet))
        self.assertEqual(
            irs.cssText,
            '@import "../import3.css";\n@import "import-impossible.css" print;\n.import2 {\n    /* sheets/import2.css */\n    background: url(http://example.com/images/example.gif);\n    background: url(//example.com/images/example.gif);\n    background: url(/images/example.gif);\n    background: url(images2/example.gif);\n    background: url(./images2/example.gif);\n    background: url(../images/example.gif);\n    background: url(./../images/example.gif)\n    }'  # noqa
            .encode())

        # name is used for open and setting of href automatically
        # test needs to be relative to this test file!
        os.chdir(os.path.dirname(__file__))
        name = basetest.get_sheet_filename('import.css')

        s = css_parser.parseFile(name, media='screen', title='from file')
        self.assertTrue(isinstance(s, css_parser.css.CSSStyleSheet))
        if sys.platform.startswith('java'):
            # on Jython only file:
            self.assertTrue(s.href.startswith('file:'))
        else:
            # normally file:/// on win and file:/ on unix
            self.assertTrue(s.href.startswith('file:/'))
        self.assertTrue(s.href.endswith('/sheets/import.css'))
        self.assertEqual('utf-8', s.encoding)
        self.assertEqual('screen', s.media.mediaText)
        self.assertEqual('from file', s.title)
        self.assertEqual(self.exp.encode(), s.cssText)

        ir = s.cssRules[0]
        self.assertEqual('import/import2.css', ir.href)
        irs = ir.styleSheet
        self.assertTrue(isinstance(irs, css_parser.css.CSSStyleSheet))
        self.assertEqual(
            irs.cssText,
            '@import "../import3.css";\n@import "import-impossible.css" print;\n.import2 {\n    /* sheets/import2.css */\n    background: url(http://example.com/images/example.gif);\n    background: url(//example.com/images/example.gif);\n    background: url(/images/example.gif);\n    background: url(images2/example.gif);\n    background: url(./images2/example.gif);\n    background: url(../images/example.gif);\n    background: url(./../images/example.gif)\n    }'  # noqa
            .encode())

        # next test
        css = 'a:after { content: "羊蹄€\u2020" }'

        fd, name = tempfile.mkstemp('_css_parsertest.css')
        t = os.fdopen(fd, 'wb')
        t.write(css.encode('utf-8'))
        t.close()

        self.assertRaises(UnicodeDecodeError, css_parser.parseFile, name,
                          'ascii')

        # ???
        s = css_parser.parseFile(name, encoding='iso-8859-1')
        self.assertEqual(css_parser.css.CSSStyleSheet, type(s))
        self.assertEqual(s.cssRules[1].selectorText, 'a:after')

        s = css_parser.parseFile(name, encoding='utf-8')
        self.assertEqual(css_parser.css.CSSStyleSheet, type(s))
        self.assertEqual(s.cssRules[1].selectorText, 'a:after')

        css = '@charset "iso-8859-1"; a:after { content: "ä" }'
        t = codecs.open(name, 'w', 'iso-8859-1')
        t.write(css)
        t.close()

        self.assertRaises(UnicodeDecodeError, css_parser.parseFile, name,
                          'ascii')

        s = css_parser.parseFile(name, encoding='iso-8859-1')
        self.assertEqual(css_parser.css.CSSStyleSheet, type(s))
        self.assertEqual(s.cssRules[1].selectorText, 'a:after')

        self.assertRaises(UnicodeDecodeError, css_parser.parseFile, name,
                          'utf-8')

        # clean up
        try:
            os.remove(name)
        except EnvironmentError:
            pass

    def test_parseUrl(self):
        "css_parser.parseUrl()"
        href = basetest.get_sheet_filename('import.css')
        # href = u'file:' + urllib.pathname2url(href)
        href = css_parser.helper.path2url(href)
        # href = 'http://seewhatever.de/sheets/import.css'
        s = css_parser.parseUrl(href, media='tv, print', title='from url')
        self.assertTrue(isinstance(s, css_parser.css.CSSStyleSheet))
        self.assertEqual(href, s.href)
        self.assertEqual(self.exp.encode(), s.cssText)
        self.assertEqual('utf-8', s.encoding)
        self.assertEqual('tv, print', s.media.mediaText)
        self.assertEqual('from url', s.title)

        sr = s.cssRules[1]
        img = sr.style.getProperty('background-image').propertyValue[0].value
        self.assertEqual(img, 'images/example.gif')

        ir = s.cssRules[0]
        self.assertEqual('import/import2.css', ir.href)
        irs = ir.styleSheet
        self.assertEqual(
            irs.cssText,
            '@import "../import3.css";\n@import "import-impossible.css" print;\n.import2 {\n    /* sheets/import2.css */\n    background: url(http://example.com/images/example.gif);\n    background: url(//example.com/images/example.gif);\n    background: url(/images/example.gif);\n    background: url(images2/example.gif);\n    background: url(./images2/example.gif);\n    background: url(../images/example.gif);\n    background: url(./../images/example.gif)\n    }'  # noqa
            .encode())

        ir2 = irs.cssRules[0]
        self.assertEqual('../import3.css', ir2.href)
        irs2 = ir2.styleSheet
        self.assertEqual(
            irs2.cssText,
            '/* import3 */\n.import3 {\n    /* from ./import/../import3.css */\n    background: url(images/example3.gif);\n    background: url(./images/example3.gif);\n    background: url(import/images2/example2.gif);\n    background: url(./import/images2/example2.gif);\n    background: url(import/images2/../../images/example3.gif)\n    }'  # noqa
            .encode())

    def test_setCSSSerializer(self):
        "css_parser.setSerializer() and css_parser.ser"
        s = css_parser.parseString('a { left: 0 }')
        exp4 = '''a {
    left: 0
    }'''
        exp1 = '''a {
 left: 0
 }'''
        self.assertEqual(exp4.encode(), s.cssText)
        newser = css_parser.CSSSerializer(
            css_parser.serialize.Preferences(indent=' '))
        css_parser.setSerializer(newser)
        self.assertEqual(exp1.encode(), s.cssText)
        newser = css_parser.CSSSerializer(
            css_parser.serialize.Preferences(indent='    '))
        css_parser.ser = newser
        self.assertEqual(exp4.encode(), s.cssText)

    def test_parseStyle(self):
        "css_parser.parseStyle()"
        s = css_parser.parseStyle('x:0; y:red')
        self.assertEqual(type(s), css_parser.css.CSSStyleDeclaration)
        self.assertEqual(s.cssText, 'x: 0;\ny: red')

        s = css_parser.parseStyle('@import "x";')
        self.assertEqual(type(s), css_parser.css.CSSStyleDeclaration)
        self.assertEqual(s.cssText, '')

        tests = [('content: "ä"', 'iso-8859-1'), ('content: "€"', 'utf-8')]
        for v, e in tests:
            s = css_parser.parseStyle(v.encode(e), encoding=e)
            self.assertEqual(s.cssText, v)

        self.assertRaises(UnicodeDecodeError, css_parser.parseStyle,
                          'content: "ä"'.encode('utf-8'), 'ascii')

    def test_getUrls(self):
        "css_parser.getUrls()"
        css_parser.ser.prefs.keepAllProperties = True

        css = r'''
        @import "im1";
        @import url(im2);
        @import url( im3 );
        @import url( "im4" );
        @import url( 'im5' );
        a {
            background-image: url(a) !important;
            background-\image: url(b);
            background: url(c) no-repeat !important;
            /* issue #46 */
            src: local("xx"),
                 url("f.woff") format("woff"),
                 url("f.otf") format("opentype"),
                 url("f.svg#f") format("svg");
            }'''
        urls = set(css_parser.getUrls(css_parser.parseString(css)))
        self.assertEqual(
            urls,
            set([
                "im1", "im2", "im3", "im4", "im5", "a", "b", "c", 'f.woff',
                'f.svg#f', 'f.otf'
            ]))
        css_parser.ser.prefs.keepAllProperties = False

    def test_replaceUrls(self):
        "css_parser.replaceUrls()"
        css_parser.ser.prefs.keepAllProperties = True

        css = r'''
        @import "im1";
        @import url(im2);
        a {
            background-image: url(c) !important;
            background-\image: url(b);
            background: url(a) no-repeat !important;
            }'''
        s = css_parser.parseString(css)
        css_parser.replaceUrls(s, lambda old: "NEW" + old)
        self.assertEqual('@import "NEWim1";', s.cssRules[0].cssText)
        self.assertEqual('NEWim2', s.cssRules[1].href)
        self.assertEqual(
            '''background-image: url(NEWc) !important;
background-\\image: url(NEWb);
background: url(NEWa) no-repeat !important''', s.cssRules[2].style.cssText)

        css_parser.ser.prefs.keepAllProperties = False

        # CSSStyleDeclaration
        style = css_parser.parseStyle('''color: red;
                                        background-image:
                                            url(1.png),
                                            url('2.png')''')
        css_parser.replaceUrls(style, lambda url: 'prefix/' + url)
        self.assertEqual(
            style.cssText, '''color: red;
background-image: url(prefix/1.png), url(prefix/2.png)''')

    def test_resolveImports(self):
        "css_parser.resolveImports(sheet)"
        self._tempSer()
        css_parser.ser.prefs.useMinified()

        a = '@charset "iso-8859-1";@import"b.css";\xe4{color:green}'.encode(
            'iso-8859-1')
        b = '@charset "ascii";\\E4 {color:red}'.encode('ascii')

        # normal
        with self.patch_default_fetcher((None, b)):
            s = css_parser.parseString(a)

            # py3 TODO
            self.assertEqual(a, s.cssText)
            self.assertEqual(b, s.cssRules[1].styleSheet.cssText)

            c = css_parser.resolveImports(s)

            # py3 TODO
            self.assertEqual(
                '\xc3\xa4{color:red}\xc3\xa4{color:green}'.encode(
                    'iso-8859-1'), c.cssText)

            c.encoding = 'ascii'
            self.assertEqual(
                r'@charset "ascii";\E4 {color:red}\E4 {color:green}'.
                encode(), c.cssText)

        # b cannot be found
        with self.patch_default_fetcher((None, None)):
            s = css_parser.parseString(a)

            # py3 TODO
            self.assertEqual(a, s.cssText)
            self.assertEqual(css_parser.css.CSSStyleSheet, type(s.cssRules[1].styleSheet))
            c = css_parser.resolveImports(s)
            # py3 TODO
            self.assertEqual(
                '@import"b.css";\xc3\xa4{color:green}'.encode(
                    'iso-8859-1'), c.cssText)

        # @import with media
        a = '@import"b.css";@import"b.css" print, tv ;@import"b.css" all;'
        b = 'a {color: red}'
        with self.patch_default_fetcher((None, b)):
            s = css_parser.parseString(a)

            c = css_parser.resolveImports(s)

            self.assertEqual(
                'a{color:red}@media print,tv{a{color:red}}a{color:red}'.
                encode(), c.cssText)

        # cannot resolve with media => keep original
        a = '@import"b.css"print;'
        b = '@namespace "http://example.com";'
        with self.patch_default_fetcher((None, b)):
            s = css_parser.parseString(a)
            c = css_parser.resolveImports(s)
            self.assertEqual(a.encode(), c.cssText)

        # urls are adjusted too, layout:
        # a.css
        # c.css
        # img/img.gif
        # b/
        #     b.css
        #     subimg/subimg.gif
        a = '''
                @import"b/b.css";
                a {
                    x: url(/img/abs.gif);
                    y: url(img/img.gif);
                    z: url(b/subimg/subimg.gif);
                    }'''

        def fetcher(url):
            c = {
                'b.css':
                '''
                        @import"../c.css";
                        b {
                            x: url(/img/abs.gif);
                            y: url(../img/img.gif);
                            z: url(subimg/subimg.gif);
                            }''',
                'c.css':
                '''
                        c {
                            x: url(/img/abs.gif);
                            y: url(./img/img.gif);
                            z: url(./b/subimg/subimg.gif);
                            }'''
            }
            return 'utf-8', c[os.path.split(url)[1]]

        def do():
            with self.patch_default_fetcher(fetcher):
                s = css_parser.parseString(a)
                r = css_parser.resolveImports(s)
            return s, r

        s, r = do()

        css_parser.ser.prefs.useDefaults()
        css_parser.ser.prefs.keepComments = False
        self.assertEqual(
            '''c {
    x: url(/img/abs.gif);
    y: url(img/img.gif);
    z: url(b/subimg/subimg.gif)
    }
b {
    x: url(/img/abs.gif);
    y: url(img/img.gif);
    z: url(b/subimg/subimg.gif)
    }
a {
    x: url(/img/abs.gif);
    y: url(img/img.gif);
    z: url(b/subimg/subimg.gif)
    }'''.encode(), r.cssText)

    css_parser.ser.prefs.useDefaults()


if __name__ == '__main__':
    import unittest
    unittest.main()
