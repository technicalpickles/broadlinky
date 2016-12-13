import argparse
import sys

from . import Broadlinky

def learn(broadlinky, args):
    broadlinky = Broadlinky()
    device = broadlinky.get_device(args.device)

    while True:
        packet = broadlinky.learn()
        if packet is not None:
            replay = input("Learned a thing. Replay it to confirm functioning? ")
            if replay == 'yes':
                broadlinky.send_data(packet)

                command = input("What do you want to save it as (Blank resumes learning) ")
                if command != '':
                    device.remember_command(args.namespace, command, packet)

def send(broadlinky, args):
    device = broadlinky.devices[args.device]
    device.send_command(args.namespace, args.command)


def server(broadlinky, args):
    from .app import build_app
    app = build_app()
    app.run()


def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='broadlinky')
    subparsers = parser.add_subparsers(dest='subcommand', help='command help')

    learn_parser = subparsers.add_parser('learn', help='learn device commands')
    learn_parser.add_argument('device')
    learn_parser.add_argument('namespace')
    learn_parser.set_defaults(func=learn)

    send_parser = subparsers.add_parser('send', help='send a device command')
    send_parser.add_argument('device')
    send_parser.add_argument('namespace')
    send_parser.add_argument('command')
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
