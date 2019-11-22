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


# Future imports for Python 2
from __future__ import print_function, unicode_literals

# Standard library imports
import sys
import os
import os.path as osp
import subprocess

# Adjust bundled executables (See: vendor)
_ext = '.exe' if os.name == 'nt' else ''
pygettext = ['pygettext' + _ext]
msgfmt = ['msgfmt' + _ext]


def get_files(path, modname=None):
    """"""
    if modname is None:
        modname = osp.basename(path)

    if not osp.isdir(path):
        return [modname]

    files = []
    for dirname, _dirnames, filenames in os.walk(path):
        files += [osp.join(dirname, f)
                  for f in filenames
                  if f.endswith(".py") or f.endswith(".pyw")]

    # for dirname, _dirnames, filenames in os.walk("tests"):
    #     files += [osp.join(dirname, f)
    #               for f in filenames
    #               if f.endswith(".py") or f.endswith(".pyw")]
    return files


def get_lang(path):
    """"""
    dirnames = []
    localedir = osp.join(path, "locale")
    for _dirname, dirnames, _filenames in os.walk(localedir):
        break  # We just want the list of first level directories
    return dirnames


def do_rescan(path, languages=None):
    """"""
    files = get_files(path)
    do_rescan_files(files, path, languages=languages)


def do_rescan_files(files, path, modname=None, languages=None):
    """"""
    localedir = osp.join(path, "locale")

    if not os.path.isdir(localedir):
        os.makedirs(localedir)

    if modname is None:
        modname = osp.basename(path)

    potfile = modname + ".pot"
    subprocess.call(pygettext
                    + ["-o", potfile,  # Name of .pot file
                       # "-D",   # Extract docstrings
                       "-p", localedir]  # Destination
                    + files)
    print('Updating pot file: "{}"'.format(potfile))

    if languages is None:
        languages = get_lang(path)

    if languages is []:
        return

    for lang in languages:
        pofilepath = osp.join(localedir, lang, "LC_MESSAGES", modname + ".po")
        potfilepath = osp.join(localedir, potfile)
        print("Updating...", pofilepath)

        if not osp.exists(osp.join(localedir, lang, "LC_MESSAGES")):
            os.makedirs(osp.join(localedir, lang, "LC_MESSAGES"))

        if not osp.exists(pofilepath):
            with open(pofilepath, "r") as fh2:
                data = fh2.read()

            with open(pofilepath, "w") as fh:
                fh.write("# -*- coding: utf-8 -*-\n")
                data = data.replace("charset=CHARSET", "charset=utf-8")
                data = data.replace("Content-Transfer-Encoding: ENCODING",
                                    "Content-Transfer-Encoding: utf-8")
                fh.write(data)
        else:
            print("Merge...")
            subprocess.call(["msgmerge", "-o",
                             pofilepath, pofilepath, potfilepath])


def do_compile(path, modname=None):
    """"""
    if modname is None:
        modname = osp.dirname(path)

    localedir = osp.join(path, "locale")
    for lang in get_lang(path):
        pofilepath = osp.join(localedir, lang, "LC_MESSAGES", modname + ".po")
        mofilepath = osp.join(localedir, lang, "LC_MESSAGES", modname + ".mo")
        cmd = msgfmt + ['-o', mofilepath, pofilepath]
        try:
            subprocess.call(cmd)
        except Exception as e:
            print(e)
