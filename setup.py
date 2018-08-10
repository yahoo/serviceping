#!/usr/bin/env python
# Copyright (c) 2013-2018, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.
import setuptools
import sys


# Create a dictionary of our arguments, this way this script can be imported
# without running setup() to allow external scripts to see the setup settings.
def setuptools_version_supported():
    major, minor, patch = setuptools.__version__.split('.')
    if int(major) > 31:
        return True
    return False


if not setuptools_version_supported():
    print('Setuptools version 32.0.0 or higher is needed to install this package')
    sys.exit(1)


setuptools.setup(
    license='Apache',
    classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: BSD :: FreeBSD',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX :: SunOS/Solaris',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: System :: Systems Administration',
            'Topic :: Utilities',
    ],
    python_requires=">=3.6",
)

