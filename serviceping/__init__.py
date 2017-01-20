# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.
"""
TCP Network Service Ping Utilities
"""
import json
import os
from .serviceping import calc_deviation, StatsList
from .network import scan


__metadata_file__ = os.path.join(
    os.path.dirname(__file__),
    'package_metadata.json'
)

if os.path.exists(__metadata_file__):  # pragma: no cover
    with open(__metadata_file__) as _file_handle:
        __package_metadata__ = json.load(_file_handle)
else:
    __package_metadata__ = {
        'version': '0.0.0'
    }

__version__ = str(__package_metadata__.get('version', '0.0.0'))
__git_version__ = str(__package_metadata__.get('git_version', ''))
__ci_version__ = str(__package_metadata__.get('ci_version', ''))
__ci_build_number__ = str(__package_metadata__.get('ci_build_number', ''))
__git_branch__ = str(__package_metadata__.get('git_branch', ''))
__git_origin__ = str(__package_metadata__.get('git_origin', ''))
__git_hash__ = str(__package_metadata__.get('git_hash', ''))
__git_base_url__ = 'https://github.com/yahoo/serviceping'
if __git_origin__.endswith('.git'):  # pragma: no cover
    __git_base_url__ = __git_origin__[:-4].strip('/')
__source_url__ = __git_base_url__ + '/tree/' + __git_hash__
