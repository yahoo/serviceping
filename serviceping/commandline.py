"""
Command Line Utility Functions
"""
import argparse


def parse_arguments():
    """
    Parse the command line arguments
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", dest="count", default=0, type=int,
        help="Number of pings to send"
    )
    parser.add_argument(
        "-i", dest="interval", default=1, type=float, help="Ping interval"
    )
    parser.add_argument(
        "-d", dest="timings", default=False, action="store_true",
        help="Show timings for the entire connection"
    )
    parser.add_argument(
        'destination', nargs='+', help='Destination host or URL'
    )
    args = parser.parse_args()
    return args, args.destination
