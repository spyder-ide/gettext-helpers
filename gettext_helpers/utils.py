# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2009-2012 Pierre Raybaut/CEA (CeCILL License Version 2)
# Copyright (c) 2015- Gettext-Helpers Contributors (see AUTHORS.txt)
#
# This file is part of Gettext-Helpers.
# <https://github.com/spyder-ide/gettext-helpers>
#
# Gettext-Helpers is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gettext-Helpers is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gettext-Helpers.  If not, see <https://www.gnu.org/licenses/>.
#
# See LICENSE.txt in the gettext-helpers repository root for the full text.
# Also, see NOTICE.txt in the same location for more detailed legal history:
# <https://github.com/spyder-ide/gettext-helpers/blob/master/NOTICE.txt>
# -----------------------------------------------------------------------------
"""Gettext utilities."""

# Future imports for Python 2
from __future__ import print_function, unicode_literals

# Standard library imports
import sys
import os
import os.path as osp
import subprocess

# Adjust bundled executables (See: vendor)
_EXT = '.exe' if os.name == 'nt' else ''
PYGETTEXT_EXEC = 'pygettext' + _EXT
MSGFMT_EXEC = 'msgfmt' + _EXT
MSGMERGE_EXEC = 'msgmerge'
LC_MESSAGES = 'LC_MESSAGES'
MO_EXT = '.mo'
PO_EXT = '.po'
POT_EXT = '.pot'


def _get_locale_path(path):
    """Retunr locale full path based on path."""
    return osp.join(path, 'locale')


def get_files(path, extensions=('.py', '.pyw')):
    """Get all files in path ending in extension."""
    fpaths = []
    for dirname, _dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(extensions):
                fpaths.append(osp.join(dirname, filename))
    return fpaths


def get_languages(path):
    """Return any existing language translations on path locale."""
    dirnames = []
    locale_path = _get_locale_path(path)
    for _dirname, dirnames, _filenames in os.walk(locale_path):
        break  # We just want the list of first level directories
    return dirnames


def scan_path(path, module=None, languages=None):
    """Scan path for translations and generate '*.pot' and '*.po' files."""
    files = get_files(path)
    scan_files(files, path, module=module, languages=languages)


def scan_files(files, path, module=None, languages=None):
    """Scan files for translations and generate '*.pot' and '*.po' files."""
    locale_path = _get_locale_path(path)

    if not osp.isdir(locale_path):
        os.makedirs(locale_path)

    if module is None:
        module = osp.basename(path)

    potfile = module + POT_EXT
    subprocess.call(
        [
            PYGETTEXT_EXEC,
            '-o',
            potfile,  # Name of .pot file
            # '-D',   # Extract docstrings
            '-p',
            locale_path,  # Destination
        ] + files
    )
    potpath = osp.join(locale_path, potfile)
    print('Updating pot file: "{}"\n'.format(potpath))

    if languages is None:
        languages = get_languages(path)

    if languages is []:
        return

    for lang in languages:
        pofilepath = osp.join(locale_path, lang, LC_MESSAGES,
                              module + PO_EXT)
        potfilepath = osp.join(locale_path, potfile)
        print('Updating po file "{}"\n'.format(pofilepath))

        if not osp.exists(osp.join(locale_path, lang, LC_MESSAGES)):
            os.makedirs(osp.join(locale_path, lang, LC_MESSAGES))

        if not osp.exists(pofilepath):
            with open(potfilepath, 'r') as fh:
                data = fh.read()

            with open(pofilepath, 'w') as fh:
                fh.write('# -*- coding: utf-8 -*-\n')
                data = data.replace('charset=CHARSET', 'charset=utf-8')
                data = data.replace('Content-Transfer-Encoding: ENCODING',
                                    'Content-Transfer-Encoding: utf-8')
                fh.write(data)
        else:
            print('Merge...')
            try:
                subprocess.call(
                    [
                        MSGMERGE_EXEC,
                        '-o',
                        pofilepath,
                        pofilepath,
                        potfilepath,
                    ]
                )
            except Exception as e:
                print(e)


def compile_path(path, module=None):
    """Compile '.po' files to '.mo' files."""
    if module is None:
        module = osp.dirname(path)

    locale_path = _get_locale_path(path)
    for lang in get_languages(path):
        pofilepath = osp.join(locale_path, lang, LC_MESSAGES,
                              module + PO_EXT)
        mofilepath = osp.join(locale_path, lang, LC_MESSAGES,
                              module + MO_EXT)
        cmd = [
            MSGFMT_EXEC,
            '-o',
            mofilepath,
            pofilepath,
        ]
        try:
            subprocess.call(cmd)
        except Exception as e:
            print(e)
