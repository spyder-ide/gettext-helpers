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

# Standard library imports
import argparse
import os
import sys

# Local imports
from .constants import LANG_CODES
from .translate import translate_path
from .utils import compile_path, scan_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command',
        type=str,
        choices=['scan', 'compile', 'translate'],
        help='Command to run!',
    )
    parser.add_argument(
        'path',
        type=str,
        default=None,
        help='Path to main repository root module',
    )
    parser.add_argument(
        '-m',
        '--module',
        type=str,
        default=None,
        help='Module name to use for *.pot, *.po and *.mo files',
    )
    parser.add_argument(
        '-sl',
        '--source-lang',
        type=str,
        default='en',
        help='Source language code',
    )
    parser.add_argument(
        '-tl',
        '--target-lang',
        type=str,
        help='Target language code',
        default=None
    )
    sys.stdout.write('\n')
    args = parser.parse_args()

    # Check language is correct
    if args.target_lang and args.target_lang[:2].lower() not in LANG_CODES:
        sys.stdout.write(
            '\nInvalid target language code!\n\n'
            'Language codes must start with a 2 letter lowercase \n'
            'code as defined in the ISO: 639-2 standard.\n\n'
        )
        return

    if args.source_lang and args.source_lang[:2].lower() not in LANG_CODES:
        sys.stdout.write(
            '\nInvalid source language code!\n\n'
            'Language codes must start with a 2 letter lowercase \n'
            'code as defined in the ISO: 639-2 standard.\n\n'
        )
        return

    path = os.path.abspath(args.path)

    # Check path exists
    if args.command == 'scan':
        if args.target_lang is None:
            scan_path(path, module=args.module)
        else:
            scan_path(path, module=args.module, languages=[args.target_lang])
    elif args.command == 'compile':
        compile_path(path)
    elif args.command == 'translate':
        translate_path(path, target_lang=args.target_lang,
                       source_lang=args.source_lang, module=args.module)

    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
