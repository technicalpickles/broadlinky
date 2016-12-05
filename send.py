import broadlink
from IPython import embed
import yaml
import argparse

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('thing')
parser.add_argument('state', choices=["on", "off"])
args = parser.parse_args()


with open('codes.yaml', 'r') as file:
    data = yaml.load(file)

thing = data[args.thing]
if args.state == 'on':
    packet = thing[True]
elif args.state == 'off':
    packet = thing[False]

devices = broadlink.discover(timeout=5)
device = devices[0]
device.auth()
device.send_data(packet)
