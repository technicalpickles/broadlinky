import argparse
import sys

from . import Broadlinky

def discover(broadlinky, args):
    broadlinky = Broadlinky()
    while True:
        broadlinky.learn_device_packet(args.device)


def send(broadlinky, args):
    device = broadlinky.devices[args.device]
    device.send_command(args.namespace, args.command)


def server(broadlinky, args):
    from .app import build_app
    app = build_app()
    app.run()


def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='broadlinky')
    subparsers = parser.add_subparsers(dest='command', help='command help')

    discover_parser = subparsers.add_parser('discover', help='discover device commands')
    discover_parser.add_argument('device')
    discover_parser.set_defaults(func=discover)

    send_parser = subparsers.add_parser('send', help='send a device command')
    send_parser.add_argument('device')
    send_parser.add_argument('namespace')
    send_parser.add_argument('state')
    send_parser.set_defaults(func=send)

    server_parser = subparsers.add_parser('server', help='start webserver')
    server_parser.set_defaults(func=server)

    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)


def main():
    """Do IR and RF stuff."""

    args = parse_args()
    broadlinky = Broadlinky()
    args.func(broadlinky, args)


if __name__ == "__main__":
    main()
