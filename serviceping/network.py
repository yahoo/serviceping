"""
Network port scan functions
"""
import socket
import ssl
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
