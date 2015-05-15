serviceping
***********

This utility provides a script with a "ping" like
interface to ping tcp port services.


Build Status
============

.. image:: https://travis-ci.org/yahoo/serviceping.svg
    :target: https://travis-ci.org/yahoo/serviceping

.. image:: https://coveralls.io/repos/yahoo/serviceping/badge.svg
  :target: https://coveralls.io/r/yahoo/serviceping

.. image:: https://img.shields.io/pypi/dm/serviceping.svg
    :target: https://pypi.python.org/pypi/serviceping/
    
.. image:: https://img.shields.io/pypi/v/serviceping.svg
   :target: https://pypi.python.org/pypi/serviceping

.. image:: https://img.shields.io/pypi/l/serviceping.svg
    :target: https://pypi.python.org/pypi/serviceping/


Installation
============

To install serviceping, simply:

.. code-block::

    $ pip install serviceping

or using easy_install:

.. code-block::

    $ easy_install serviceping

or from source:

.. code-block::

    $ python setup.py install


Usage
=====

.. code-block::

    Usage: serviceping [options] url | host[:port] | ip[:port]

    Options:
      -h, --help   show this help message and exit
      -c COUNT     Number of pings to send
      -i INTERVAL  Ping interval
      -d


Examples
========

The serviceping tool uses a syntax that mirrors that of the ping commmand.


Ping port 80 (http) on www.yahoo.com
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here we ping www.yahoo.com via http (port 80).
It is easy to see that that address has multiple hosts responding and the
latency of each request.

.. code-block::

    $ serviceping www.yahoo.com
    SERVICEPING www.yahoo.com:80 (98.139.180.149:80).
    from www.yahoo.com:80 (98.139.183.24:80): time=2.46 ms
    from www.yahoo.com:80 (98.139.180.149:80): time=2.43 ms
    --- www.yahoo.com ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1704.0ms
    rtt min/avg/max/dev = 2.43/2.44/2.46/4.00 ms
    $

Same thing using ssl
~~~~~~~~~~~~~~~~~~~~

Service ping can also connect to other ports such as the ssl port (443).

.. code-block::

    $ serviceping www.yahoo.com:443
    SERVICEPING www.yahoo.com:443 (98.139.183.24:443).
    from www.yahoo.com:443 (98.139.180.149:443): time=2.89 ms
    from www.yahoo.com:443 (98.139.180.149:443): time=2.81 ms
    --- www.yahoo.com ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1744.0ms
    rtt min/avg/max/dev = 2.81/2.85/2.89/6.08 ms
    $

Pinging a URL instead of the port
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Portping also allows specifying a URL.  If a URL is specified it will also
perform an http get request and show the response.

This is useful to see when there are hosts doing unexpected things in a dns
rotation or behind a reverse proxy or vip.

In this example we specify a url of http://cnn.com/

This shows that there are two hosts responding to this request and that they
are returning different amounts of data in their responses.

.. code-block::

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


Pinging a URL with timings
~~~~~~~~~~~~~~~~~~~~~~~~~~

The detailed timing flag adds timings for each step of each request.

This is useful for determining what is causing latency issues or errors.

Here we are doing the previous example with detailed timings.

In the results we can see a few new things.

It is clear that the host with address 157.166.226.25 is taking significantly longer to establish the tcp connection and handle the http get request.

.. code-block::

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

License
=======

Code licensed under the Apache license. See LICENSE.txt
file for terms.
