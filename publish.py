#!/usr/bin/env python
# License: LGPLv3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>

import glob
import os
import re
import shlex
import shutil
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('src/css_parser/__init__.py', 'rb') as f:
    VERSION = f.read().decode('utf-8')
m = re.search(r"^__version__ = '(.+?)'", VERSION, flags=re.MULTILINE)
assert m is not None
VERSION = m.group(1)


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
    for rem in ['dist', 'build']:
        os.path.exists(rem) and shutil.rmtree(rem)
    run('python', '-m', 'build')


def tag_release():
    run(f'git tag -s "v{VERSION}" -m "version-{VERSION}"')
    run(f'git push origin "v{VERSION}"')


def upload_release():
    files = list(glob.glob('dist/*'))
    run('twine', 'upload', '--config-file',
        os.path.join(os.environ['PENV'], 'pypi'), *files)


myinput = input


def has_executable(exe):
    for path in os.environ['PATH'].split(os.pathsep):
        if os.access(os.path.join(path, exe), os.X_OK):
            return True
    return False


def main():
    if not has_executable('twine'):
        raise SystemExit('Need to install twine to upload to PyPI')
    if myinput(f'Publish version {red(VERSION)} [y/n]? ') != 'y':
        raise SystemExit(1)
    build_release()
    if myinput(red('Upload') + ' release [y/n]? ') != 'y':
        raise SystemExit(1)
    tag_release()
    upload_release()


if __name__ == '__main__':
    main()
