# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.

import json
import os


_metadata_file = os.path.join(
    os.path.dirname(__file__),
    'package_metadata.json'
)

if os.path.exists(_metadata_file):  # pragma: no cover
    with open(_metadata_file) as _file_handle:
        _package_metadata = json.load(_file_handle)
else:
    _package_metadata = {
        'version': '0.0.0'
    }

__version__ = str(_package_metadata.get('version', '0.0.0'))
__git_version__ = str(_package_metadata.get('git_version', ''))
__ci_version__ = str(_package_metadata.get('ci_version', ''))
__ci_build_number__ = str(_package_metadata.get('ci_build_number', ''))
__git_branch__ = str(_package_metadata.get('git_branch', ''))
__git_origin__ = str(_package_metadata.get('git_origin', ''))
__git_hash__ = str(_package_metadata.get('git_hash', ''))
__git_base_url__ = 'https://github.com/yahoo/serviceping'
if __git_origin__.endswith('.git'):  # pragma: no cover
    __git_base_url__ = __git_origin__[:-4].strip('/')
__source_url__ = __git_base_url__ + '/tree/' + __git_hash__


from .serviceping import calc_deviation, StatsList