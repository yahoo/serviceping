"""
Network port scan functions
"""
from __future__ import print_function
import datetime
import socket
import ssl
import struct
import sys
from collections import OrderedDict


class ScanFailed(Exception):
    """
    The scan operation encountered a failure
    """
    pass


def scan(host, port=80, url=None, https=False, timeout=1, max_size=65535):
    """
    Scan a network port

    Parameters
    ----------
    host : str
        Host or ip address to scan

    port : int, optional
        Port to scan, default=80

    url : str, optional
        URL to perform get request to on the host and port specified

    https : bool, optional
        Perform ssl connection on the socket, default=False

    timeout : float
        Timeout for network operations, default=1

    Returns
    -------
    dict
        Result dictionary that contains the following keys:
            host - The host or IP address that was scanned
            port - The port number that was scanned
            state - The state of the port, will be either "open" or "closed"
            durations - An ordered dictionary with floating point value of the
            time elapsed for each connection operation

    Raises
    ------
    ScanFailed - The scan operation failed
    """
    starts = OrderedDict()
    ends = OrderedDict()
    port = int(port)
    result = dict(
        host=host, port=port, state='closed', durations=OrderedDict()
    )
    if url:
        timeout = 1
        result['code'] = None

    starts['all'] = starts['dns'] = datetime.datetime.now()

    # DNS Lookup
    try:
        hostip = socket.gethostbyname(host)
        result['ip'] = hostip
        ends['dns'] = datetime.datetime.now()
    except socket.gaierror:
        raise ScanFailed('DNS Lookup failed')

    # TCP Connect
    starts['connect'] = datetime.datetime.now()
    network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    network_socket.settimeout(timeout)
    result_connection = network_socket.connect_ex((hostip, port))
    ends['connect'] = datetime.datetime.now()

    # SSL
    if https:
        starts['ssl'] = datetime.datetime.now()
        network_socket = ssl.wrap_socket(network_socket)
        ends['ssl'] = datetime.datetime.now()

    # Get request
    if result_connection == 0 and url:
        starts['request'] = datetime.datetime.now()
        network_socket.send(
            "GET {0} HTTP/1.0\r\nHost: {1}\r\n\r\n".format(
                url, host
            ).encode('ascii'))
        if max_size:
            data = network_socket.recv(max_size)
        else:
            data = network_socket.recv()
        result['length'] = len(data)
        data = data.decode('ascii', errors='ignore')
        result['response'] = (data)
        try:
            result['code'] = int(data.split('\n')[0].split()[1])
        except IndexError:
            pass
        ends['request'] = datetime.datetime.now()
    network_socket.close()

    # Calculate durations
    ends['all'] = datetime.datetime.now()
    for duration in starts.keys():
        if duration in ends.keys():
            result['durations'][duration] = ends[duration] - starts[duration]
    if result_connection == 0:
        result['state'] = 'open'
    return result


class PingResponse(object):
    """
    Ping response object

    Atributes
    ---------
    host : str
        Destination host or IP address

    port : int
        Destination port

    responding : bool
        True if ping response was received

    data_mismatch : bool
        True if the recieved packet did not match the sent packet

    timeout : bool
        True if ping timed out

    start : float
        Time started

    end : float
        Time ended

    duration: float
        The duration of the ping operation
    """
    host = None
    ip = None
    port = 0
    responding = False
    data_mismatch = False
    timeout = False
    start = 0.0
    end = 0.0
    duration = None
    response = None

    def __init__(self, host=None, port=6666):
        self.host = host
        self.port = int(port)
        self.start_timer()

    def start_timer(self):
        self.start = datetime.datetime.now()
        self.end = None

    def stop_timer(self):
        self.end = datetime.datetime.now()

    def __str__(self):
        return 'ip=%s(%s):port=%s:responding=%s:data_mismatch=%s:timeout=%s:duration=%s' % (
            self.host, self.ip, str(self.port), str(self.responding), str(self.data_mismatch), str(self.timeout), str(self.duration)
        )

    @property
    def duration(self):
        """
        Get The duration based on the timer, or None no timing has been done
        """
        if not self.end:
            return None
        return self.end - self.start


def ping(host, port=80, url=None, https=False, timeout=1, max_size=65535):
    """
    Ping a host

    Parameters
    ----------
    host: str
        The host or ip address to ping

    port: int, optional
        The port to ping, default=80

    url: str, optional
        URL to ping, will do a host/port ping if not provided

    https: bool, optional
        Connect via ssl, default=False

    timeout: int, optional
        Number of seconds to wait for a response before timing out, default=1 second

    max_size: int, optional
        The max size of response that can be retrieved.  This should be a power of 2
        default=65535.

    Returns
    -------
    PingResponse:
        The ping response object
    """
    result = scan(host=host, port=port, url=url, https=https, timeout=timeout, max_size=max_size)
    result_obj = PingResponse(host=host, port=port)
    result_obj.durations = result.get('durations', None)
    result_obj.code = result.get('code', None)
    result_obj.state = result.get('state', 'unknown')
    result_obj.length = result.get('length', 0)
    result_obj.ip = result.get('ip', None)
    result_obj.response = result.get('response', None)
    if result_obj.state in ['open']:
        result_obj.responding = True
    if result_obj.durations:
        result_obj.start = datetime.datetime.now()
        result_obj.end = result_obj.start + result_obj.durations.get('all', datetime.timedelta(0))
    return result_obj


if __name__ == '__main__':
    host = 'localhost'
    if len(sys.argv) > 1:
        host = sys.argv[-1]
    print(ping(host, 8888))
