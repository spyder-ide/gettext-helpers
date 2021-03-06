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
"""
Translation utilities.
"""

# Standard library imports
import os.path as osp
import time

# Third party imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import polib

# Vars
_base_url = (
    'https://translate.google.com/#view=home'
    '&op=translate'
    '&sl={source_language}'
    '&tl={target_language}'
    '&text={text}')


def clean_lang_for_google(lang):
    """Convert language descriptor to a valid google translate language."""
    LANG = {
        'pt_BR': 'pt',
        'zh_CN': 'zh-CN',
    }
    if lang in LANG:
        lang = LANG.get(lang)
    return lang


def get_driver():
    """Search for available webdriver."""
    driver = None
    error = None
    try:
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        print('Using Firefox webdriver:')
    except Exception as error:
        try:
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(chrome_options=chrome_options)
            print('Using Chrome webdriver:')
        except Exception as error:
            pass

    if driver is None:
        print('Webdriver not found!')
        print(error)

    return driver


def translate_path(path, target_lang, source_lang='en', module=None):
    """Read all untranslated and fuzzy entries and translate them."""
    google_target_lang = clean_lang_for_google(target_lang)
    google_source_lang = clean_lang_for_google(source_lang)

    if module is None:
        module = osp.basename(path)
    pofile = osp.join(path, 'locale', target_lang, 'LC_MESSAGES',
                      module + '.po')

    if osp.isfile(pofile):
        print('Transalting file:')
        print(pofile)

        # Use polib to get all untranslated strings
        # Do not add column wrapping by using a large value!
        po = polib.pofile(pofile, wrapwidth=10000)
        texts = po.untranslated_entries() + po.fuzzy_entries()
        template = '/{}) Translating: '.format(len(texts))
        driver = get_driver()

        if driver is None:
            return

        for idx, entry in enumerate(texts):
            text = entry.msgid
            print('({}'.format(idx + 1) + template + repr(text))
            try:
                trans = translate_string(driver, text, google_target_lang,
                                         google_source_lang)
            except Exception as e:
                print(e)
                trans = ''
            entry.msgstr = trans

            # We save on each item to be able to continue on last item if the
            # process stops.
            po.save(pofile)

        try:
            driver.close()
        except Exception:
            pass
    else:
        print('"{}" file not found!'.format(pofile))


def translate_string(driver, text, target_lang, source_lang='en'):
    """Use google translate vie web driver to translate text."""
    url = _base_url.format(
        source_language=source_lang,
        target_language=target_lang,
        text=text,
    )
    driver.get(url)
    time.sleep(1)
    elem = driver.find_element_by_class_name("translation")
    trans_text = elem.text or ''
    return trans_text
