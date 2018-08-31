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
from __future__ import print_function

# Standard library imports
import sys
import os
import os.path as osp
import subprocess


# Find pygettext.py source on a windows install
if os.name == 'nt':
    pygettext = ['python',
                 osp.join(sys.prefix, "Tools", "i18n", "pygettext.py")]
    msgfmt = ['python', osp.join(sys.prefix, "Tools", "i18n", "msgfmt.py")]
else:
    pygettext = ['pygettext']
    msgfmt = ['msgfmt']


def get_files(modname):
    if not osp.isdir(modname):
        return [modname]

    files = []
    for dirname, _dirnames, filenames in os.walk(modname):
        files += [osp.join(dirname, f)
                  for f in filenames
                  if f.endswith(".py") or f.endswith(".pyw")]
    for dirname, _dirnames, filenames in os.walk("tests"):
        files += [osp.join(dirname, f)
                  for f in filenames
                  if f.endswith(".py") or f.endswith(".pyw")]
    return files


def get_lang(modname):
    localedir = osp.join(modname, "locale")
    for _dirname, dirnames, _filenames in os.walk(localedir):
        break  # We just want the list of first level directories
    return dirnames


def do_rescan(modname):
    files = get_files(modname)
    dirname = modname
    do_rescan_files(files, modname, dirname)


def do_rescan_files(files, modname, dirname):
    localedir = osp.join(dirname, "locale")
    potfile = modname + ".pot"
    subprocess.call(pygettext
                    + ["-o", potfile,  # Nom du fichier pot
                       # "-D",   # Extract docstrings
                       "-p", localedir]  # Dest
                    + files)

    for lang in get_lang(dirname):
        pofilepath = osp.join(localedir, lang, "LC_MESSAGES", modname+".po")
        potfilepath = osp.join(localedir, potfile)
        print("Updating...", pofilepath)

        if not osp.exists(osp.join(localedir, lang, "LC_MESSAGES")):
            os.mkdir(osp.join(localedir, lang, "LC_MESSAGES"))
        if not osp.exists(pofilepath):
            outf = open(pofilepath, "w")
            outf.write("# -*- coding: utf-8 -*-\n")
            data = open(potfilepath).read()
            data = data.replace("charset=CHARSET", "charset=utf-8")
            data = data.replace("Content-Transfer-Encoding: ENCODING",
                                "Content-Transfer-Encoding: utf-8")
            outf.write(data)
        else:
            print("Merge...")
            subprocess.call(["msgmerge", "-o",
                             pofilepath, pofilepath, potfilepath])


def do_compile(modname, dirname=None):
    if dirname is None:
        dirname = modname
    localedir = osp.join(dirname, "locale")
    for lang in get_lang(dirname):
        pofilepath = osp.join(localedir, lang, "LC_MESSAGES", modname + ".po")
        mofilepath = osp.join(localedir, lang, "LC_MESSAGES", modname + ".mo")
        cmd = msgfmt + ['-o', mofilepath, pofilepath]
        subprocess.call(cmd)


def main(modname):
    if len(sys.argv) < 2:
        cmd = "help"
    else:
        cmd = sys.argv[1]
    # lang = get_lang(modname)

    if cmd == "help_gettext":
        subprocess.call(pygettext + ["--help"])
    elif cmd == "help_msgfmt":
        subprocess.call(msgfmt + ["--help"])
    elif cmd == "scan":
        print("Updating pot files...")
        do_rescan(modname)
    elif cmd == "compile":
        print("Builtin .mo files...")
        do_compile(modname)
    else:
        help_text = (
            """
            Gettxt-Helpers

            Available commands:

                help : This message
                help_gettext : pygettext --help
                help_msgfmt : msgfmt --help
                scan : Rescan .py files and update existing .po files
                compile : Recompile .po files

                Pour fonctionner ce programme doit être lancé depuis
                la racine du module
                Traductions disponibles:

            """
            )

        print(help_text)
        for dir_name in get_lang(modname):
            print(dir_name)
