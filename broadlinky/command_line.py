import argparse
import sys

from . import Broadlinky

def learn(broadlinky, args):
    broadlinky = Broadlinky()
    device = broadlinky.get_device(args.device)

    while True:
        state_value_packet = broadlinky.learn()
        if state_value_packet is not None:
            replay = input("Learned a thing. Replay it to confirm functioning? ")
            if replay == 'yes':
                broadlinky.send_data(state_value_packet)

                value_name = input("What do you want to save it as (Blank resumes learning) ")
                if value_name != '':
                    device.remember_state_value_packet(args.state, value_name, state_value_packet)

def send(broadlinky, args):
    device = broadlinky.devices[args.device]
    device.set_state(args.state, args.value)


def server(broadlinky, args):
    from .mqtt import run
    run(broadlinky)

    from .app import build_app
    app = build_app()
    app.run()


def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='broadlinky')
    subparsers = parser.add_subparsers(dest='subcommand', help='command help')

    learn_parser = subparsers.add_parser('learn', help='learn device commands')
    learn_parser.add_argument('device')
    learn_parser.add_argument('state')
    learn_parser.set_defaults(func=learn)

    send_parser = subparsers.add_parser('send', help='send a device command')
    send_parser.add_argument('device')
    send_parser.add_argument('state')
    send_parser.add_argument('value')
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
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit()
