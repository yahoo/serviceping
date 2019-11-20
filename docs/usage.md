Serviceping provides a command line interface that operates like the 
[ping](https://linux.die.net/man/8/ping) command  but instead of using icmp packets to check 
for a response from a host.  It can perform a  tcp network connection to a port on a host or 
a http or https get request to check a url on a host.

Since tcp and http requests require multiple operations.  Each request performs all of
the operations end to end for each request.  The serviceping command adds a 
`-d` flag that will show timings for the different stages the ping request.

!!! note "The serviceping command line usage information""

    ```
    usage: serviceping [-h] [-c COUNT] [-i INTERVAL] [-d] destination [destination ...]
    positional arguments:
      destination Destination host or URL
    
    optional arguments:
      -h, --help   show this help message and exit
      -c COUNT     Number of pings to send
      -i INTERVAL  Ping interval
      -d           Show timings for the entire connection
    ```
