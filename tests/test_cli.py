from datetime import datetime, timedelta
import sys
from serviceping.cli import exit_statistics, main
from unittest import TestCase


class TestCLI(TestCase):

    def setUp(self):
        self._orig_argv = sys.argv

    def tearDown(self):
        sys.argv = self._orig_argv

    def test__exit_statistics(self):
        start_time = datetime.now()
        exit_statistics(
            hostname='localhost', start_time=start_time,
            count_sent=1, count_received=1,
            min_time=timedelta(seconds=.1), avg_time=1.0,
            max_time=timedelta(seconds=2.0), deviation=1.2
        )

    def test__main(self):
        sys.argv = ['serviceping', '-c', '2', 'yahoo.com']
        main()

    def test__main__interval(self):
        sys.argv = ['serviceping', '-c', '2', '-i', '2', 'yahoo.com']
        main()

    def test__main__port(self):
        sys.argv = ['serviceping', '-c', '2', 'yahoo.com:80']
        main()


    def test__main__url(self):
        sys.argv = ['serviceping', '-c', '1', 'http://yahoo.com/']
        main()

    def test__main__url__timings(self):
        sys.argv = ['serviceping', '-c', '1', '-d', '1', 'http://yahoo.com/']
        main()

    def test__main__https__url__timings(self):
        sys.argv = ['serviceping', '-c', '1', '-d', '1', 'https://yahoo.com/']
        main()

    def test__main__https__url__timings__port(self):
        sys.argv = ['serviceping', '-c', '1', '-d', '1', 'https://yahoo.com:4443/index.html']
        main()
