#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: LGPLv3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import ast
import glob
import os
import re
import shlex
import shutil
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

VERSION = open('src/css_parser/version.py', 'rb').read().decode('utf-8')
VERSION = '.'.join(map(str, ast.literal_eval(re.search(r'^version\s+=\s+(.+)', VERSION, flags=re.M).group(1))))


def red(text):
    return '\033[91;1m' + text + '\033[39;22m'


def green(text):
    return '\033[92;1m' + text + '\033[39;22m'


def run(*cmd):
    if len(cmd) == 1:
        cmd = shlex.split(cmd[0])
    print(green(' '.join(cmd)))
    ret = subprocess.Popen(cmd).wait()
    if ret != 0:
        raise SystemExit(ret)


def build_release():
    for rem in 'dist build'.split():
        os.path.exists(rem) and shutil.rmtree(rem)
    run('python3', 'setup.py', '-q', 'sdist', 'bdist_wheel')


def sign_release():
    for installer in glob.glob('dist/*'):
        run(os.environ['PENV'] + '/gpg-as-kovid', '--armor', '--detach-sig',
            installer)


def tag_release():
    run('git tag -s "v{0}" -m "version-{0}"'.format(VERSION))
    run('git push origin "v{0}"'.format(VERSION))


def upload_release():
    files = list(glob.glob('dist/*'))
    run('twine', 'upload', '--config-file',
        os.path.join(os.environ['PENV'], 'pypi'), *files)


try:
    myinput = raw_input
except NameError:
    myinput = input


def has_executable(exe):
    for path in os.environ['PATH'].split(os.pathsep):
        if os.access(os.path.join(path, exe), os.X_OK):
            return True
    return False


def main():
    if not has_executable('twine'):
        raise SystemExit('Need to install twine to upload to PyPI')
    if myinput('Publish version {} [y/n]? '.format(red(VERSION))) != 'y':
        raise SystemExit(1)
    build_release()
    sign_release()
    if myinput(red('Upload') + ' release [y/n]? ') != 'y':
        raise SystemExit(1)
    tag_release()
    upload_release()


if __name__ == '__main__':
    main()
