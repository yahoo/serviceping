#!/usr/bin/env python
# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.
"""
test serviceping network scan
"""
from __future__ import print_function
from serviceping.network import scan, ScanFailed
import unittest


# Any methods of the class below that begin with "test" will be executed
# when the the class is run (by calling unittest.main()
class TestServicepingScan(unittest.TestCase):

    def test_serviceping_scan_closed(self):
        result = scan('localhost', port=65500)
        self.assertEqual(result['state'], 'closed')
        self.assertEqual(result['host'], 'localhost')
        self.assertEqual(result['port'], 65500)

    def test_serviceping_scan_open_http(self):
        result = scan('yahoo.com', port=80)
        self.assertEqual(result['state'], 'open')
        self.assertEqual(result['host'], 'yahoo.com')
        self.assertEqual(result['port'], 80)

    def test_serviceping_scan_open_https(self):
        result = scan('yahoo.com', port=443, https=True)
        self.assertEqual(result['state'], 'open')
        self.assertEqual(result['host'], 'yahoo.com')
        self.assertEqual(result['port'], 443)

    def test_serviceping_scan_open_https_url(self):
        result = scan(
            'yahoo.com', port=443, https=True, url='https://yahoo.com/'
        )
        self.assertEqual(result['state'], 'open')
        self.assertEqual(result['host'], 'yahoo.com')
        self.assertEqual(result['port'], 443)
        self.assertIn(result['code'], [200, 301])


if __name__ == '__main__':
    unittest.main()
