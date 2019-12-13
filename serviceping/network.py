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
    def __init__(self, *args, **kwargs):
        try:
            self.result = kwargs.pop('result')
        except KeyError:
            result = {}
        super().__init__(*args, **kwargs)


def scan(host, port=80, url=None, https=False, timeout=1.0, max_size=65535):
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
        host=host, port=port, state='closed', durations=OrderedDict(), ssl_version=''
    )
    if url:
        result['code'] = None

    starts['all'] = starts['dns'] = datetime.datetime.now()

    # DNS Lookup
    try:
        hostip = socket.gethostbyname(host)
        result['ip'] = hostip
        ends['dns'] = datetime.datetime.now()
    except socket.gaierror:
        raise ScanFailed('DNS Lookup failed', result=result)

    # TCP Connect
    starts['connect'] = datetime.datetime.now()
    network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    network_socket.settimeout(timeout)
    result_connection = network_socket.connect_ex((hostip, port))
    ends['connect'] = datetime.datetime.now()

    # SSL
    if https:
        starts['ssl'] = datetime.datetime.now()
        try:
            network_socket = ssl.wrap_socket(network_socket)  # nosec
        except socket.timeout:
            raise ScanFailed(f'SSL socket timeout ({timeout} seconds)', result=result)
        ends['ssl'] = datetime.datetime.now()
        result['ssl_version'] = network_socket.version()

    # Get request
    if result_connection == 0 and url:
        starts['request'] = datetime.datetime.now()
        network_socket.send(
            "GET {0} HTTP/1.0\r\nHost: {1}\r\n\r\n".format(
                url, host
            ).encode('ascii'))
        if max_size:
            try:
                data = network_socket.recv(max_size)
            except socket.timeout:
                raise ScanFailed(f'TCP socket timeout ({timeout} seconds)', result=result)
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
    def __init__(
            self, host=None, port=0, ip=None, responding=False, data_mismatch=False, timeout=False, code=None,
            state=None, length=0, start=None, end=None, error=False, error_message=None, durations=None, response=None,
            sequence=0, ssl_version=''
    ):
        self.host = host
        self.port = int(port)
        self.ip = ip
        self.responding = responding
        self.data_mismatch = data_mismatch
        self.timeout = timeout
        self.code = code
        self.state = state
        self.length = length
        self.durations = durations
        self.sequence = sequence
        self.ssl_version = ssl_version
        if start:
            self.start = start
        else:
            self.start = datetime.datetime.now()
        self.end = end
        self.error = error
        self.error_message = error_message
        self.response = response
        self.start_timer()

    def start_timer(self):
        self.start = datetime.datetime.now()
        self.end = None

    def stop_timer(self):
        self.end = datetime.datetime.now()

    def __repr__(self):
        return f'PingResponse(host={self.host!r}, port={self.port!r}, ip={self.ip!r}, sequence={self.sequence!r}, ' \
               f'responding={self.responding!r}, data_mismatch={self.data_mismatch!r}, timeout={self.timeout!r}, ' \
               f'code={self.code!r}, state={self.state!r}, length={self.length!r}, start={self.start!r}, ' \
               f'end={self.end!r}, error={self.error!r}, error_message={self.error_message!r}, ' \
               f'durations={self.durations!r}, ssl_version={self.ssl_version!r}, response={self.response!r})'

    def __str__(self):
        return f'ip={self.host}({self.ip}):port={self.port}:responding={self.responding}' \
               f'{":error="+str(self.error)+":error_message="+repr(self.error_message) if self.error else ""}' \
               f':data_mismatch={self.data_mismatch}' \
               f':timeout={self.timeout}:ssl_version={self.ssl_version}:duration={self.duration}'

    @property
    def duration(self):
        """
        Get The duration based on the timer, or None no timing has been done
        """
        if not self.end:
            return None
        return self.end - self.start


def ping(host, port=80, url=None, https=False, timeout=1.0, max_size=65535, sequence=0):
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

    timeout: float, optional
        Number of seconds to wait for a response before timing out, default=1 second

    max_size: int, optional
        The max size of response that can be retrieved.  This should be a power of 2
        default=65535.

    sequence: int, optional
        Sequence number for the ping request

    Returns
    -------
    PingResponse:
        The ping response object
    """
    try:
        result = scan(host=host, port=port, url=url, https=https, timeout=timeout, max_size=max_size)
    except ScanFailed as failure:
        result = failure.result
        result['error'] = True
        result['error_message'] = str(failure)
    result_obj = PingResponse(
        host=host, port=port, ip=result.get('ip', None), sequence=sequence,
        durations=result.get('durations', None),
        code=result.get('code', None),
        state=result.get('state', 'unknown'),
        length=result.get('length', 0),
        ssl_version=result.get('ssl_version', ''),
        response=result.get('response', None),
        error=result.get('error', False),
        error_message=result.get('error_message', None),
        responding=True if result.get('state', 'unknown') in ['open'] else False,
        start=datetime.datetime.now(),
        end=datetime.datetime.now() + result['durations'].get('all', datetime.timedelta(0)) if result.get('durations', None) else None
    )
    return result_obj


if __name__ == '__main__':
    host = 'localhost'
    if len(sys.argv) > 1:
        host = sys.argv[-1]
    print(ping(host, 8888))
