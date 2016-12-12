#!/usr/bin/env python3
"""Interface to discover RF/IR packets and remember devices & commands."""
import argparse
from broadlinky import Broadlinky


def main():
    """Discover packets in a loop."""
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('device')
    args = parser.parse_args()

    broadlinky = Broadlinky()
    while True:
        broadlinky.learn_device_packet(args.device)

if __name__ == "__main__":
    main()
