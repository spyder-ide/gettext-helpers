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
"""Crowdin utilities."""

# Standard library imports
import os


def create_crowdin_base_config(path, module=None):
    """"""
    message = """commit_message: '[ci skip] New %language% translation from Crowdin'
append_commit_message: false
files:
  - source: /{module}/locale/{module}.pot
    translation: /{module}/locale/%two_letters_code%/LC_MESSAGES/%file_name%.po
    languages_mapping:
      two_letters_code:
        pt-BR: pt_BR
        zh-CN: zh_CN
"""
    if module is None:
        module = os.path.basename(path)

    content = message.format(module=module)
    repo_root = os.getcwd()
    crowdin_fpath = os.path.join(repo_root, 'crowdin.yml')
    with open(crowdin_fpath, 'w') as fh:
      fh.write(content)

    return crowdin_fpath