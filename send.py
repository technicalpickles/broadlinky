#!/usr/bin/env python3
from IPython import embed
import argparse
import broadlink
import yaml
import os
import re

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('thing')
parser.add_argument('state')
args = parser.parse_args()

codes_path = os.path.dirname(os.path.abspath(__file__)) + '/devices.yaml'

with open(codes_path, 'r') as file:
    code_data = yaml.load(file)

thing = code_data[args.thing]
if args.state == 'on':
    packet = thing[True]
elif args.state == 'off':
    packet = thing[False]
elif re.search('^\d+$', args.state):
    packet = thing[int(args.state)]
else:
    packet = thing[args.state]

devices = broadlink.discover(timeout=5)
device = devices[0]
device.auth()
device.send_data(packet)
