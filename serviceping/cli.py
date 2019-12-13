# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.

"""
Command line utility providing a ping like interface for pinging tcp/ssl
services.
"""
import datetime
import socket
import sys
import time
from urllib.parse import urlparse

from .commandline import parse_arguments
from .serviceping import calc_deviation
from .network import scan, ping


TIMEOUT = 10  # Set a reasonable timeout value


def exit_statistics(hostname, start_time, count_sent, count_received, min_time, avg_time, max_time, deviation):
    """
    Print ping exit statistics
    """
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    duration_sec = float(duration.seconds * 1000)
    duration_ms = float(duration.microseconds / 1000)
    duration = duration_sec + duration_ms
    package_loss = 100 - ((float(count_received) / float(count_sent)) * 100)
    print(f'\b\b--- {hostname} ping statistics ---')
    try:
        print(f'{count_sent} packets transmitted, {count_received} received, {package_loss}% packet loss, time {duration}ms')
    except ZeroDivisionError:  # pragma: no cover
        print(f'{count_sent} packets transmitted, {count_received} received, 100% packet loss, time {duration}ms')
    print(
        'rtt min/avg/max/dev = %.2f/%.2f/%.2f/%.2f ms' % (
            min_time.seconds*1000 + float(min_time.microseconds)/1000,
            float(avg_time) / 1000,
            max_time.seconds*1000 + float(max_time.microseconds)/1000,
            float(deviation)
        )
    )


def main():
    (options, command_args) = parse_arguments()

    rc = 1
    https = False
    if command_args[0].startswith('http:') or command_args[0].startswith('https:'):
        urlp = urlparse(command_args[0])
        hostname = urlp.hostname
        port = urlp.port
        if command_args[0].startswith('https:'):
            https = True
        if not port:
            if urlp.scheme in ['https']:
                port = 443
            else:
                port = 80
        url = urlp.path
    else:
        args = command_args[0].split(':')
        hostname = args[0]
        try:
            port = int(args[1])
        except IndexError:
            port = 80
        try:
            url = args[2]
        except IndexError:
            url = None
    count_sent = count_received = 0
    max_time = min_time = datetime.timedelta(0)
    avg_time = 0
    deviation = 0
    start_time = datetime.datetime.now()
    times = []
    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        print('serviceping: unknown host %s' % hostname, file=sys.stderr)
        return 1
    print('SERVICEPING %s:%d (%s:%d).' % (hostname, port, ip, port))
    while True:
        try:
            ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            print('serviceping: unknown host %s' % hostname, file=sys.stderr)
            return 1

        try:
            ping_response = ping(host=hostname, port=port, url=url, https=https, sequence=count_sent, timeout=options.timeout)
            count_sent += 1
            if ping_response.responding:
                count_received += 1
                if ping_response.durations['all'] > max_time:
                    max_time = ping_response.durations['all']
                if min_time == datetime.timedelta(0) or ping_response.durations['all'] < min_time:
                    min_time = ping_response.durations['all']
                times.append(ping_response.durations['all'].seconds * 1000 + float(ping_response.durations['all'].microseconds))
                avg_time = sum(times) / float(len(times))
                deviation = calc_deviation(times, avg_time)
                if len(times) > 100:
                    times = times[-100:]
                code_string = ''
                if ping_response.ssl_version:
                    code_string += f'ssl={ping_response.ssl_version}'
                if url:
                    if code_string:
                        code_string += ':'
                    code_string += 'response=%s' % ping_response.code
                if options.timings:
                    print(
                        '%sfrom %s:%s (%s:%s):%s' % (
                            '%d bytes ' % ping_response.length if ping_response.length else '',
                            hostname, port, ip, port, code_string),
                        end=" "
                    )
                    for d in ['dns', 'connect', 'ssl', 'request', 'all']:
                        if d in ping_response.durations.keys():
                            print('%s=%.2fms' % (
                                d,
                                ping_response.durations[d].seconds * 1000
                                + float(ping_response.durations[d].microseconds) / 1000
                            ), end=" ")
                else:
                    print(
                        '%sfrom %s:%s (%s:%s):%s time=%.2f ms' % (
                            '%d bytes ' % ping_response.length if ping_response.length else '',
                            hostname, port, ip, port, code_string,
                            float(
                                ping_response.durations['all'].seconds * 1000
                                + ping_response.durations['all'].microseconds
                            ) / 1000
                        ),
                        end=" ")
                print()
                rc = 0
            else:
                if ping_response.error and ping_response.error_message:
                    print(f'{ping_response.error_message} for seq {ping_response.sequence}')
                rc = 1
            if options.count and options.count == count_sent:
                exit_statistics(hostname, start_time, count_sent, count_received, min_time, avg_time, max_time, deviation)
                return rc
            time.sleep(options.interval)
        except KeyboardInterrupt:  # pragma: no cover
            exit_statistics(hostname, start_time, count_sent, count_received, min_time, avg_time, max_time, deviation)
            return rc


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
