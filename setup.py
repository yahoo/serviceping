#!/usr/bin/env python
# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.

import os
import json
from setuptools import setup


# Package Metadata filename
METADATA_FILENAME = 'serviceping/package_metadata.json'
BASEPATH = os.path.dirname(os.path.abspath(__file__))


# Create a dictionary of our arguments, this way this script can be imported
# without running setup() to allow external scripts to see the setup settings.
setup_arguments = {
    'name': 'serviceping',
    'version': '0.0.0',
    'author': 'Dwight Hubbard',
    'author_email': 'dhubbard@yahoo-inc.com',
    'url': 'http://github.com/yahoo/serviceping',
    'license': 'LICENSE.txt',
    'description': 'A ping like tool for network services',
    'classifiers': [
            'License :: OSI Approved :: Apache License',
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: BSD :: FreeBSD',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX :: SunOS/Solaris',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: System :: Systems Administration',
            'Topic :: Utilities',
    ],
    'package_data': {
        'serviceping': ['package_metadata.json']
    },
    'packages': ['serviceping'],
    'include_package_data': True,
}


class Git(object):
    """
    Simple wrapper class to the git command line tools
    """
    version_list = ['0', '7', '0']

    def __init__(self, version=None):
        if version:
            self.version_list = version.split('.')

    @property
    def version(self):
        """
        Generate a Unique version value from the git information
        :return:
        """
        git_rev = len(os.popen('git rev-list HEAD').readlines())
        if git_rev != 0:
            self.version_list[-1] = '%d' % git_rev
        version = '.'.join(self.version_list)
        return version

    @property
    def branch(self):
        """
        Get the current git branch
        :return:
        """
        return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()

    @property
    def hash(self):
        """
        Return the git hash for the current build
        :return:
        """
        return os.popen('git rev-parse HEAD').read().strip()

    @property
    def origin(self):
        """
        Return the fetch url for the git origin
        :return:
        """
        for item in os.popen('git remote -v'):
            split_item = item.strip().split()
            if split_item[0] == 'origin' and split_item[-1] == '(push)':
                return split_item[1]


def add_scripts_to_package():
    """
    Update the "scripts" parameter of the setup_arguments with any scripts
    found in the "scripts" directory.
    :return:
    """
    global setup_arguments

    if os.path.isdir('scripts'):
        setup_arguments['scripts'] = [
            os.path.join('scripts', f) for f in os.listdir('scripts')
        ]


def get_and_update_package_metadata():
    """
    Update the package metadata for this package if we are building the package.
    :return:metadata - Dictionary of metadata information
    """
    global setup_arguments
    global METADATA_FILENAME

    if not os.path.exists('.git') and os.path.exists(METADATA_FILENAME):
        with open(METADATA_FILENAME) as fh:
            metadata = json.load(fh)
    else:
        git = Git(version=setup_arguments['version'])
        metadata = {
            'version': git.version,
            'long_description': 'A ping like tool for network services',
            'git_hash': git.hash,
            'git_origin': git.origin,
            'git_branch': git.branch
        }
        for readme_file in ['README.rst', 'README.md', 'README.txt']:
            if os.path.exists(readme_file):
                with open(readme_file) as file_handle:
                    metadata['long_description'] = file_handle.read()
                break
        with open(METADATA_FILENAME, 'w') as fh:
            json.dump(metadata, fh)
    return metadata


if __name__ == '__main__':
    # We're being run from the command line so call setup with our arguments
    metadata = get_and_update_package_metadata()
    setup_arguments['version'] = metadata['version']
    setup_arguments['long_description'] = metadata['long_description']
    setup(**setup_arguments)
