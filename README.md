# Gettext-Helpers

*Copyright © 2009–2012 Pierre Raybaut/CEA*

*Copyright © 2011- Gettext-Helpers Contributors*

Licensed under the terms of the [GNU General Public License Version 3](
https://www.gnu.org/licenses/gpl.html).


## Overview

Gettext-Helpers is originally based on a module and set of scripts from the
[GUIdata project](https://github.com/PierreRaybaut/guidata) by
[Pierre Raybaut](https://github.com/PierreRaybaut),
the original creator of [Spyder](https://www.spyder-ide.org/),
the Scientific Python Development Environment, and later adopted for use
internally with building the translations for that
[project](https://github.com/spyder-ide/spyder) by current Spyder maintainer
[Carlos Cordoba](https://github.com/ccordoba12) and others,
with additional improvements added during that time.

Finally, it was spun out into its own project for modularity and flexibility.
However, its primary purpose remains to build the Spyder translation files.


## Installation

Currently, you can just ``git clone`` the repository and call the scripts and
functions locally on your project of choice, though you may want to put it on
your ``PATH``/``PYTHONPATH`` first.

You will also need to install the Firefox selenium driver!

### With pip

```bash
pip install selenium polib
python setup.py develop
```

### With conda
```bash
conda install selenium polib -c spyder-ide
python setup.py develop
```


## Usage

Go to the root of the repository you want to update:

### To scan files and generate a *.pot file:

```bash
spyder-gettext scan <PATH_TO_ROOT_MODULE>
```

### To create or update new language stubs:

```bash
spyder-gettext scan <PATH_TO_ROOT_MODULE> --target-lang es
```

### To translate untranslated strings:

```bash
spyder-gettext translate <PATH_TO_ROOT_MODULE> --target-lang es
```

## Contributing

Everyone is welcome to help with Gettext-Helpers.
Please read our
[contributing instructions](
https://github.com/spyder-ide/gettext-helpers/blob/master/CONTRIBUTING.md)
to get started!


## Credits

The original files were licensed under the terms of the CeCILL license 2.0;
this derivative is released under the GNU General Public License 3.0
(or any later version) for greater license compatibility and clarity,
to reduce pointless license proliferation, and to use an OSI-approved license.
For older versions of the files originally covered by the CeCILL,
the applicable license is the one listed in the header at the top of the files.

All current files are released under the GNU GPL version 3,
although they may be based on or near-identical to MIT (Expat) licensed
versions found elsewhere in the Spyder project, and thus can be used under
those permissive terms as well if so desired.


## About the Spyder IDE

Spyder is a powerful scientific environment written in Python, for Python,
and designed by and for scientists, engineers and data analysts. It offers a
unique combination of the advanced editing, analysis, debugging, and profiling
functionality of a comprehensive development tool with the data exploration,
interactive execution, deep inspection, and beautiful visualization
capabilities of a scientific package.

Beyond its many built-in features, its abilities can be extended even further
via its plugin system and API. Furthermore, Spyder can also be used as a PyQt5
extension library, allowing you to build upon its functionality and embed
its components, such as the interactive console, in your own software.

For more general information about Spyder and to stay up to date on the
latest Spyder news and information, please check out [our website](
https://www.spyder-ide.org/).



## More information

[Spyder Website](https://www.spyder-ide.org/)

[Download Spyder (with Anaconda)](https://www.anaconda.com/download/)

[Spyder Github](https://github.com/spyder-ide/spyder)

[Support Spyder on OpenCollective](https://opencollective.com/spyder/)
