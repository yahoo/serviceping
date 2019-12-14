# serviceping

[![Build Status](https://cd.screwdriver.cd/pipelines/2881/badge?cache=false)](https://cd.screwdriver.cd/pipelines/2881)
[![Coverage](https://codecov.io/gh/yahoo/serviceping/branch/master/graph/badge.svg?cache=false)](https://codecov.io/gh/yahoo/serviceping)
[![Version](https://img.shields.io/pypi/v/serviceping.svg)](https://pypi.python.org/pypi/serviceping/)
[![Downloads](https://pepy.tech/badge/serviceping)](https://pepy.tech/project/serviceping)
[![Supported Python Versions](https://img.shields.io/badge/python-3.6,3.7,3.8-blue.svg)](https://pypi.python.org/pypi/serviceping/)
[![License](https://img.shields.io/pypi/l/serviceping.svg)](https://pypi.python.org/pypi/serviceping/)
[![Documentation](https://img.shields.io/badge/Documentation-latest-blue.svg)](https://yahoo.github.io/serviceping/)

A utility with a "ping" like interface to ping tcp port services.

## Table of Contents

- [Background](#background)
- [Install](https://yahoo.github.io/serviceping/install/)
- [Usage](#usage)
- [Examples](https://yahoo.github.io/serviceping/examples/)
- [License](#license)

## Background

This utility was written to simplify troubleshooting network issues related to talking to network services

## Usage

Serviceping provides a command line interface that operates like the [ping]() command 
but instead of using icmp packets to check for a response from a host.  It can perform a 
tcp network connection to a port on a host or a http or https get request to check a url 
on a host.

Since tcp and http requests require multiple operations.  Each request performs all of
the operations end to end for the request.  The serviceping command adds a 
`-d` flag that will show timings for the different stages the ping request.

```
usage: serviceping [-h] [-c COUNT] [-i INTERVAL] [-W TIMEOUT] [-d] destination [destination ...]
positional arguments:
  destination Destination host or URL

optional arguments:
  -h, --help   show this help message and exit
  -c COUNT     Number of pings to send
  -i INTERVAL  Ping interval
  -d           Show timings for the entire connection
  -W TIMEOUT   Time to wait for a response, in seconds. The option affects only timeout in absence of any responses  
```

## Examples

The serviceping tool uses a syntax that mirrors that of the ping commmand.


### Ping port 80 (http) on www.yahoo.com

By pinging www.yahoo.com via http (port 80), we can clearly see the 
multiple hosts responding and the latency of each request.

```console
$ serviceping www.yahoo.com
SERVICEPING www.yahoo.com:80 (98.139.180.149:80).
from www.yahoo.com:80 (98.139.183.24:80): time=2.46 ms
from www.yahoo.com:80 (98.139.180.149:80): time=2.43 ms
--- www.yahoo.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1704.0ms
rtt min/avg/max/dev = 2.43/2.44/2.46/4.00 ms
$
```

### Ping port 4443 (https) on www.yahoo.com

Serviceping can also connect to other ports such as the ssl port (443).

```console
$ serviceping www.yahoo.com:443
SERVICEPING www.yahoo.com:443 (98.139.183.24:443).
from www.yahoo.com:443 (98.139.180.149:443): time=2.89 ms
from www.yahoo.com:443 (98.139.180.149:443): time=2.81 ms
--- www.yahoo.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1744.0ms
rtt min/avg/max/dev = 2.81/2.85/2.89/6.08 ms
$
```

### Pinging a URL instead of the port

The serviceping command can also specify send ping requests to a url.  If a URL is specified, it will 
perform an http get request and show the response, which is useful 
when hosts are doing unexpected things in a dns
rotation or behind a reverse proxy or vip.

In this example we specify a url of http://cnn.com/

```console
$ serviceping http://cnn.com/
SERVICEPING cnn.com:80 (157.166.255.18:80).
1500 bytes from cnn.com:80 (157.166.255.19:80):response=200 time=87.14 ms
1448 bytes from cnn.com:80 (157.166.226.25:80):response=200 time=64.82 ms
1500 bytes from cnn.com:80 (157.166.255.19:80):response=200 time=62.98 ms
1500 bytes from cnn.com:80 (157.166.255.19:80):response=200 time=78.30 ms
--- cnn.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 4372.0ms
rtt min/avg/max/dev = 62.98/73.31/87.14/56.00 ms
$
```

The output shows that two hosts are responding to this request, and that they are returning different amounts of data in their responses.

### Pinging a URL with timings

The detailed timing flag adds timings for each step of each request, 
which is useful for determining the causes of latency issues or errors.

Here we are doing the previous example with detailed timings.

```console
$ serviceping -d http://cnn.com/
SERVICEPING cnn.com:80 (157.166.255.19:80).
1386 bytes from cnn.com:80 (157.166.255.19:80):response=200 dns=0.21ms connect=68.36ms request=130.02ms all=198.73ms
1386 bytes from cnn.com:80 (157.166.226.25:80):response=200 dns=0.30ms connect=66.72ms request=101.07ms all=168.20ms
1500 bytes from cnn.com:80 (157.166.255.18:80):response=200 dns=0.30ms connect=123.94ms request=203.08ms all=327.43ms
1386 bytes from cnn.com:80 (157.166.226.26:80):response=200 dns=0.28ms connect=68.32ms request=87.94ms all=156.69ms
--- cnn.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 5009.0ms
rtt min/avg/max/dev = 156.69/212.76/327.43/138.24 ms
$
```

Clearly, the host with address 157.166.255.18 is taking significantly longer 
to establish the tcp connection and handle the http request.

### Pinging a SSL URL with timings

When pinging a ssl URL serviceping adds the ssl version information in the response.

```console
$ serviceping -d https://www.cnn.com/
SERVICEPING www.cnn.com:443 (151.101.25.67:443).
1371 bytes from www.cnn.com:443 (151.101.25.67:443):ssl=TLSv1.2:response=200 dns=0.58ms connect=10.22ms ssl=97.84ms request=12.07ms all=121.17ms 
1371 bytes from www.cnn.com:443 (151.101.25.67:443):ssl=TLSv1.2:response=200 dns=0.59ms connect=11.87ms ssl=95.93ms request=10.98ms all=119.76ms 
1371 bytes from www.cnn.com:443 (151.101.25.67:443):ssl=TLSv1.2:response=200 dns=0.56ms connect=11.14ms ssl=95.81ms request=12.49ms all=120.42ms 
1371 bytes from www.cnn.com:443 (151.101.25.67:443):ssl=TLSv1.2:response=200 dns=0.60ms connect=10.76ms ssl=179.81ms request=10.72ms all=202.28ms 
--- www.cnn.com ping statistics ---
4 packets transmitted, 4 received, 0.0% packet loss, time 3910.0370000000003ms
rtt min/avg/max/dev = 119.76/140.91/202.28/101.14 ms
$
```

## License

This project is licensed under the terms of the [Apache 2.0](LICENSE-Apache-2.0) open source license. Please refer to [LICENSE](LICENSE) for the full terms.
