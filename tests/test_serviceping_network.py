#!/usr/bin/env python
# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.
"""
test serviceping network scan
"""
from __future__ import print_function
from serviceping.network import scan, ScanFailed, ping, PingResponse
import unittest


# Any methods of the class below that begin with "test" will be executed
# when the the class is run (by calling unittest.main()
class TestServicepingScan(unittest.TestCase):

    def test_serviceping_scan_invalid_hostname(self):
        with self.assertRaises(ScanFailed):
            scan('pythonpython.python')

    def test_serviceping_scan_no_max_size(self):
        result = scan('localhost', port=65500, max_size=None)
        self.assertEqual(result['state'], 'closed')
        self.assertEqual(result['host'], 'localhost')
        self.assertEqual(result['port'], 65500)

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

    def test_serviceping_ping_closed(self):
        result = ping('localhost', port=65500)
        self.assertIsInstance(result, PingResponse)
        self.assertIsInstance(result, PingResponse)
        self.assertFalse(result.responding)
        self.assertEqual(result.state, 'closed')
        self.assertEqual(result.host, 'localhost')
        self.assertEqual(result.port, 65500)

    def test_serviceping_ping_open_http(self):
        result = ping('yahoo.com', port=80)
        self.assertIsInstance(result, PingResponse)
        self.assertTrue(result.responding)
        self.assertEqual(result.state, 'open')
        self.assertEqual(result.host, 'yahoo.com')
        self.assertEqual(result.port, 80)

    def test_serviceping_ping_open_https(self):
        result = ping('yahoo.com', port=443, https=True)
        self.assertIsInstance(result, PingResponse)
        self.assertTrue(result.responding)
        self.assertEqual(result.state, 'open')
        self.assertEqual(result.host, 'yahoo.com')
        self.assertEqual(result.port, 443)

    def test_serviceping_ping_open_https_url(self):
        result = ping(
            'yahoo.com', port=443, https=True, url='https://yahoo.com/'
        )
        self.assertIsInstance(result, PingResponse)
        self.assertTrue(result.responding)
        self.assertEqual(result.state, 'open')
        self.assertEqual(result.host, 'yahoo.com')
        self.assertEqual(result.port, 443)
        self.assertIn(result.code, [200, 301])

    def test_serviceping_pingresponse__str__(self):
        result = ping('localhost', 65500)
        self.assertIn('ip=localhost(127.0.0.1):port=65500:responding=False:data_mismatch=False:timeout=False:ssl_version=:duration=', str(result))


if __name__ == '__main__':
    unittest.main()
