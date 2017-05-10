#!/usr/bin/env python
# (c) Copyright 2017 Jonathan Simmonds
"""A micro installer, designed to be lightly configurable and very simple.
   Useful for installing small, very simple projects."""
import argparse
import ConfigParser
import textwrap
import sys
import os

SUPPORTED_NAMES = ['INSTALL.CFG', 'install.cfg', '.INSTALL.CFG', '.install.cfg']
PROJECT_SECTION = '$PROJECT$'
SOURCE_KEY = 'source'
TARGET_KEY = 'target'
OPTIONAL_KEY = 'optional'
DEFAULT_KEY = 'default'
OVERRIDE_KEY = 'override'

def _get_optional_str(config, section, option, fallback):
    return config.get(section, option) \
            if config.has_option(section, option) else fallback

def _get_optional_bool(config, section, option, fallback):
    return config.getboolean(section, option) \
            if config.has_option(section, option) else fallback

def main():
    """Main method."""
    # Handle command line.
    parser = argparse.ArgumentParser(description='A micro installer, designed '
                                     'to be lightly configurable and very '
                                     'simple. Useful for installing small, '
                                     'very simple projects.')
    parser.add_argument('project_dir',
                        type=str, metavar='PROJECT-DIR', nargs='?', default='.',
                        help='Project directory to install from. Defaults to '
                        'the current directory.')
    args = parser.parse_args()
    interactive = True

    # Parse the config file.
    config_files = [os.path.join(args.project_dir, n) for n in SUPPORTED_NAMES]
    config = ConfigParser.RawConfigParser()
    config.read(config_files)

    # Process the config file's header.
    project = config.get(PROJECT_SECTION, 'name')
    description = config.get(PROJECT_SECTION, 'description')
    root = _get_optional_str(config, PROJECT_SECTION, 'root', None)
    override = _get_optional_bool(config, PROJECT_SECTION, OVERRIDE_KEY, False)

    # Print the header.
    print "\nInstaller for %s\n%s\n" % (project, '-' * (14 + len(project)))
    print '%s\n' % (textwrap.fill(description))
    if root:
        if override:
            user = raw_input('Installation directory [default: %s]: ' % (root))
            if user:
                root = user
        print "Installing to %s\n" % (root)

    # Loop through the parsed file and install each component.
    for component in config.sections():
        if component == PROJECT_SECTION:
            continue
        # Extract fields from the section.
        source = _get_optional_str(config, component, SOURCE_KEY, component)\
            .replace(PROJECT_SECTION, root)
        target = config.get(component, TARGET_KEY)\
            .replace(PROJECT_SECTION, root)
        optional = _get_optional_bool(config, component, OPTIONAL_KEY, False)
        default = _get_optional_bool(config, component, DEFAULT_KEY, False)
        override = _get_optional_bool(config, component, OVERRIDE_KEY, False)
        # Collect user input if necessary.
        print "Installing %s..." % (component)
        if interactive and optional:
            user = raw_input('  Install %s [%s]: ' %
                             (component, 'Y/n' if default else 'N/y'))
            if (user and user not in ['y', 'Y', 'yes', 'Yes']) or \
               (not user and not default):
                continue
        if interactive and override:
            user = raw_input('  Install directory for %s [default: %s]: ' %
                             (component, target))
            if user:
                target = user
        #if os.path.exists(target):
        print '  %s installed from %s to %s' % (component, source, target)
    print '\n%s installed.' % (project)

# Entry point.
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print
        sys.exit(1)
