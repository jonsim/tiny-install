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
    - [Example config file](#example-config-file)
  - [Remaining work](#remaining-work)


# tiny-install

A micro installer, designed to be very small, light weight and configurable.
Designed for the installation of small, simple projects.

tiny-install is little more than a glorified script which copies files about, as
described in a project's configuration file. It does not handle dependency
installation or checking, versioning or updating.

&copy; Copyright 2017 Jonathan Simmonds


## Dependencies

&ge; Python 2.3 (if using < 2.7 place [argparse.py](https://pypi.python.org/pypi/argparse)
alongside `install`).


## License

All files are licensed under the MIT license.


# Documentation

## Installing a project

Projects should make it clear that they can be installed with tiny-install.
Then, assuming `install` is on the `PATH`, simply run any of:

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

`install` will accept the following command line options:

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


### Config file syntax

Config files have a basic INI-style syntax. Sections are given in
`[square-brackets]`, followed by `key = value` or `key: value` pairs (which may
*not* be indented). Comments may use `#` or `;` (only the latter may be used for
inline comments). Refer to the documentation for the
[ConfigParser](https://docs.python.org/2/library/configparser.html) library (a
builtin used for the parsing) for further information.

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
| `override_root`   | True if the user can override the root installation directory.            | False                  |
| *all other keys*  | All other key-value pairs in this section are pulled verbatim and stored. As with `root`, these keys can then be accessed as `%(key-name)s` in all other values. Unlike `root` these are not user overrideable. This is useful to reduce replication of parts of paths etc. | N/A (undefined) |


#### Module sections

The name of these sections denotes the name of the module. Names must be unique.
The only restricted names are `$PROJECT$` and `DEFAULT`.

| Available key     | Description                                                                                 | Default if absent |
|-------------------|---------------------------------------------------------------------------------------------|-------------------|
| `name`			| The module's name. This only need be provided if for some reason it cannot be represented in the section name (i.e. it is a restricted name or contains special characters). | *Section name* |
| `optional_module` | True if the user may opt out of installing this module.                                     | False             |
| `default_module`  | True if this module should be installed by default (ignored if the module is not optional). | True              |
| `source`          | Path, relative to the config file, to the item comprising the module. This may be a file or a directory (in which case it is copied recursively). | N/A (must be provided) |
| `target`          | Absolute path to the target of this item. The installation will rename to the basename, so must include the name of the destination. The path should be absolute. For this reason use of `%(root)s` is desireable. | `%(root)s/%(source)s` |
| `override_target` | True if the user can override the target destination.                                       | False             |

All keys *within a section* are accessible *within the scope of that section* via the `%(key-name)s` syntax - e.g. `%(name)s`, `%(source)s`. These will have their default value if they are not otherwise specified (so you need not define `name` to have it correctly interpolated).


### Example config file

The `examples` directory in this repository contains several examples of varying
complexity which interested parties are encouraged to explore. A simple one of
these is replicated below:

```ini
[$PROJECT$]
name = best project
description = some long winded and really quite verbose description. Maybe its
              too verbose for a description but then again maybe
              its not.
root = ~
override_root = yes
version = 1.1

[testing]
source = test/test.txt
target = %(root)s/%(name)s/interesting filename.%(version)s.txt
override_target = yes

[vimrc]
optional_module = no
default_module = yes
source = vim/.vimrc
target = %(root)s/.vimrc
override_target = no

[gitconfig]
optional_module = yes
default_module = yes
source = git/.gitconfig
target = %(root)s/.gitconfig
override_target = no

[vscode]
optional_module = yes
source = vscode
target = %(root)s/.vscode
override_target = yes
```


## Remaining work

* File copying
* Uninstallation
* Symbolic links
* Write out module install locations
* Consider updating
* Consider dependency checking
