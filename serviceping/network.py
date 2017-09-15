"""
Network port scan functions
"""
from __future__ import print_function
import socket
import ssl
import struct
import sys
import time
from collections import OrderedDict


class ScanFailed(Exception):
    """
    The scan operation encountered a failure
    """
    pass


def scan(host, port=80, url=None, https=False, timeout=1):
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

    starts['all'] = starts['dns'] = time.time()

    # DNS Lookup
    try:
        host = socket.gethostbyname(host)
        ends['dns'] = time.time()
    except socket.gaierror:
        raise ScanFailed('DNS Lookup failed')

    # TCP Connect
    starts['connect'] = time.time()
    network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    network_socket.settimeout(timeout)
    result_connection = network_socket.connect_ex((host, port))
    ends['connect'] = time.time()

    # SSL
    if https:
        starts['ssl'] = time.time()
        network_socket = ssl.wrap_socket(network_socket)
        ends['ssl'] = time.time()

    # Get request
    if result_connection == 0 and url:
        starts['request'] = time.time()
        network_socket.send(
            "GET {0} HTTP/1.0\r\nHost: {1}\r\n\r\n".format(
                url, host
            ).encode('ascii'))
        data = network_socket.recv(1500).decode('ascii')
        result['length'] = len(data)
        try:
            result['code'] = int(data.split('\n')[0].split()[1])
        except IndexError:
            pass
        ends['request'] = time.time()
    network_socket.close()

    # Calculate durations
    ends['all'] = time.time()
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
    port = 0
    responding = False
    data_mismatch = False
    timeout = False
    start = 0.0
    end = 0.0
    duration = None

    def __init__(self, host=None, port=6666):
        self.host = host
        self.port = int(port)
        self.start_timer()

    def start_timer(self):
        self.start = time.time()
        self.end = None

    def stop_timer(self):
        self.end = time.time()

    def __str__(self):
        return ':'.join([self.host, str(self.port), str(self.responding), str(self.data_mismatch), str(self.timeout), str(self.duration)])

    @property
    def duration(self):
        """
        Get The duration based on the timer, or None no timing has been done
        """
        if not self.end:
            return None
        return self.end - self.start


def ping_udp(host, port=6666, size=100, timeout=1):
    """
    Send a single udp ping

    Parameters
    ----------
    host : str
        Host or ip address to ping

    port : int, optional
        Port to ping, default=6666

    size: int, optional
        Number of bytes to send in the ping, default=100

    timeout : float
        Timeout for network operations, default=1, set to 0 for no timeout

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
    # Create a udp socket with a timeout, if a timeout is specified
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', 6667,))
    if timeout:
        udp_socket.settimeout(timeout)

    # Resolve the hostname
    try:
        host = socket.gethostbyname(host)
    except socket.gaierror:
        pass

    # Data for the packet to send
    packet_data = b'x' * size

    # Time a ping
    ping_result = PingResponse(host=host, port=port)

    # Send the ping
    udp_socket.sendto(packet_data, (host, port))

    # Wait for the response'
    try:
        received_data, server = udp_socket.recvfrom(size)
        ping_result.responding = True
        ping_result.data_mismatch = received_data == packet_data
        print('server:', server)
        print('received:', received_data)
    except socket.timeout:
        ping_result.responding = False
        ping_result.timeout = True
    ping_result.stop_timer()
    return ping_result


if __name__ == '__main__':
    host = 'localhost'
    if len(sys.argv) > 1:
        host = sys.argv[-1]
    print(ping_udp('8.8.8.8', 53))
