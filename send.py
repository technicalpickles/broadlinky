#!/usr/bin/env python3
from IPython import embed
import argparse
import broadlink
import yaml
import os

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('thing')
parser.add_argument('state', choices=["on", "off"])
args = parser.parse_args()

codes_path = os.path.dirname(os.path.abspath(__file__)) + '/codes.yaml'

with open(codes_path, 'r') as file:
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
