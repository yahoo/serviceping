
### Ping port 80 (http) on www.yahoo.com

By pinging www.yahoo.com via http (port 80), we can clearly see the  multiple hosts responding and the 
latency of each request.

!!! example "serviceping www.yahoo.com port 80"

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

### Ping port 443 (https) on www.yahoo.com

Serviceping can also connect to other ports such as the ssl port (443).

!!! example "serviceping www.yahoo.com port 443 (ssl)"

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

The serviceping command can also send requests to a a web url.  

If a URL is specified, it will perform an http or https get request and show the response, which is 
useful  when hosts are doing unexpected things in a dns rotation or behind a reverse proxy 
or vip.

In the example below we can see that the the responses are coming from multiple IP addresses.

!!! example "serviceping http://cnn.com/"

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

The output shows that two hosts are responding to this request, and that they are 
returning different amounts of data in their responses.

### Pinging a URL with timings

The detailed timing flag adds timings for each step of each request,  which is useful for determining the 
causes of latency issues or errors.

Here we are doing the previous example with detailed timings.

!!! example "serviceping http://cnn.com/ with timings"

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

The host with address 157.166.255.18 is taking significantly longer to establish the tcp connection and 
handle the http request.


### Pinging a SSL url

When pinging a ssl URL serviceping adds the ssl version information in the response.

!!! example "serviceping https://www.cnn.com/ with timings"

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

In the above example, we can see that all the responses where using TLSv1.2.
