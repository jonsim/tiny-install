# Table of Contents

- [tiny-install](#tiny-install)
  - [Dependencies](#dependencies)
  - [License](#license)
- [Documentation](#documentation)
  - [Installing a project](#installing-a-project)
  - [Creating an installable project](#creating-an-installable-project)
    - [Config file syntax](#config-file-syntax)
      - [The `$PROJECT$` section](#the-project-section)
      - [Module sections](#module-sections)
- [Example](#example)
  - [Project structure](#project-structure)
  - [Config file](#config-file)
  - [Installation](#installation)
  - [Installed structure](#installed-structure)
- [Remaining work](#remaining-work)


# tiny-install

A micro installer, intended to be very small, light weight and configurable.
Designed for the installation of small, simple projects.

**NB: tiny-install is currently under development. See the
[Remaining work](#remaining-work) section for current status.**

tiny-install is little more than a glorified file-copying/linking script as
described in a project's
[configuration file](#https://github.com/jonsim/tiny-install#config-file-syntax).
It does not handle dependency installation or checking, versioning, updating
or uninstalling. These would all require a central database of installed
projects (short of fixed install locations).

&copy; Copyright 2017 Jonathan Simmonds


## Dependencies

&ge; Python 2.3 (if using < 2.7 place
[argparse.py](https://pypi.python.org/pypi/argparse) alongside `install`).


## License

All files are licensed under
[the MIT license](https://github.com/jonsim/tiny-install/blob/master/LICENSE).

Only the file `install` makes up the functional part of the project and may be
distributed alone providing the copyright &amp; license header in it remains
intact.


# Documentation

## Installing a project

If you have a project which can be installed with tiny-install, assuming
`install` is on the `PATH`, simply run one of:

* ```bash
   cd <some-project>
   install
   ```
* ```bash
   install <some-project>
   ```
* ```bash
   install some-project.zip
   ```
* ```bash
   install http://some-website.com/some-project.zip
   ```
* ```bash
   install git@github.com:jonsim/some-project.git
   ```

`install` accepts the following command line options:

| Option              | Effect                                                 |
|---------------------|--------------------------------------------------------|
| `-h`, `--help`      | Show the help text.                                    |
| `-y`, `--yes`       | Run non-interactively, using all default arguments.    |
| `-l`, `--links`     | Create symbolic links instead of copying files.        |
| `-u`, `--uninstall` | Uninstall an existing project installation.            |


## Creating an installable project

To enable tiny-install to install a project as above:
1. Add an install config file in the root folder of your project. This file may
   be called: `INSTALL.CFG`, `install.cfg`, `.INSTALL.CFG` or `.install.cfg`.
   For consistency the first version is preferred.
1. Describe in this file the various modules of the project and their
   installation locations. See the [Config file syntax](#config-file-syntax)
   section for information on this.
1. (Optionally) give your users some kind of hint on how to install. Choose the
   [install pattern](#installing-a-project) which most makes sense for your
   project. As tiny-install is licensed under
   [the MIT license](https://github.com/jonsim/tiny-install/blob/master/LICENSE)
   you are free to modify and/or distribute it with your application as you see
   fit providing the copyright &amp; license header in `install` remains intact.
   You may redirect users to this page or reproduce in part or in full this
   documentation on your project's page. You need not provide attribution for
   any part of this documentation reproduced, nor even at all.


### Config file syntax

Config files have a basic INI-style syntax. Sections are given in
`[square-brackets]`, followed by `key = value` or `key: value` pairs (which may
*not* be indented). Comments may use `#` or `;` (only the latter may be used for
inline comments). Refer to the documentation for the
[ConfigParser](https://docs.python.org/2/library/configparser.html) library (a
builtin used for the parsing) for further information.

All paths may contain a reference to the special `~` directory which will
evaluate to the (platform appropriate) user's home directory. All paths should
use UNIX style `/` separators.

Every config file must contain the special `$PROJECT$` section. All other
sections are *module* sections.


#### The `$PROJECT$` section

It is recommended, but not necessary, to make this the first section in the
file.

| Available key     | Description                                                               | Default if absent      |
|-------------------|---------------------------------------------------------------------------|------------------------|
| `name`            | The project's name. Displayed in installation text.                       | N/A (must be provided) |
| `description`     | A *brief* description of the project. Displayed in the installation text. | N/A (must be provided) |
| `root`            | The root installation directory. This is optional, its value can be accessed as `%(root)s` in all other values. Specifying this alone does nothing. This is actually a special-case of the *all other keys* section which allows user-overrides with the `override_root` key. | Empty string |
| `override_root`   | True if the user can override the root installation directory.            | `no`                   |
| *all other keys*  | All other key-value pairs in this section are pulled verbatim and stored. As with `root`, these keys can then be accessed as `%(key-name)s` in all other values. Unlike `root` these are not user overrideable. This is useful to reduce replication. The key names must not clash with [those permitted in module sections](#module-sections). | N/A (undefined) |


#### Module sections

The name of these sections denotes the name of the module. Names must be unique.
The only restricted names are `$PROJECT$` and `DEFAULT`.

| Available key     | Description                                                                                 | Default if absent |
|-------------------|---------------------------------------------------------------------------------------------|-------------------|
| `name`			| The module's name. This only need be provided if for some reason it cannot be represented in the section name (i.e. it is a restricted name or contains special characters). | *Section name* |
| `optional_module` | True if the user may opt out of installing this module.                                     | `no`              |
| `default_module`  | True if this module should be installed by default (ignored if the module is not optional). | `yes`             |
| `source`          | Path, relative to the config file, to the item comprising the module. This may be a file or a directory (in which case it is copied recursively). | `%(name)s` |
| `target`          | Absolute path to the target of this item. The installation will rename to the basename, so must include the name of the destination. As this path is absolute use of `%(root)s` is desireable. | `%(root)s/%(source)s` |
| `override_target` | True if the user can override the target destination.                                       | `no`              |

All keys *within a section* are accessible *within the scope of that section* via the `%(key-name)s` syntax - e.g. `%(name)s`, `%(source)s`. These will have their default value if they are not otherwise specified (so you need not define `name` to have it correctly interpolated).


# Example

The `examples` directory in this repository contains several examples of varying
complexity which those interested are encouraged to explore. The example in
`examples/simple` is replicated below:

### Project structure

```
examples/simple
+-- base-file.txt
+-- INSTALL.CFG
+-- module-1
|  `- file.txt
`-- module-2
   `- file.txt
```

### Config file

Contents of `INSTALL.CFG`:
```ini
[$PROJECT$]
name = simple example
description = A very simple example project
root = ~/simple-example
override_root = yes

[base]
source = base-file.txt
target = %(root)s/base.txt

[module-1]
target = %(root)s/first-module
override_target = yes

[module-2]
optional_module = yes
default_module = yes
source = module-2
target = %(root)s/second-module
override_target = yes
```

### Installation

Note that I override some values below during installation:
```
$ install examples/simple

simple example installer
------------------------

A very simple example project

Installation directory [default: ~/simple-example]: 
Installing to ~/simple-example

Installing base...
  Installed
Installing module-1...
  Install directory [default: ~/simple-example/first-module]: ~/simple-example/1
  Installed
Install module-2 [Y/n]? n
  Skipped

simple example installed

```

### Installed structure

Note the altered values are present in the installed structure:
```
/home/jon/simple-example
+-- base.txt
`-- 1
   `- file.txt
```


# Remaining work

* Provide more friendly error output
* Add further examples
* Zip file installation
* Git installation
* Write out module install locations
* Consider uninstallation (which would require keeping a record of installation)
* Consider updating (which would require keeping a record of installation)
* Consider dependency checking
