#!/usr/bin/env python3
"""Interface to send RF/IR commands."""
import argparse
from broadlinky import Broadlinky


def main():
    """Send device commands."""
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('device')
    parser.add_argument('command')
    args = parser.parse_args()

    broadlinky = Broadlinky()
    broadlinky.send_device_command(args.device, args.command)


if __name__ == "__main__":
    main()
