import broadlink
import argparse
from IPython import embed
import time
import yaml
import os

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('device')
args = parser.parse_args()

packets_path = os.path.dirname(os.path.abspath(__file__)) + '/packets.yaml'
# TODO handle nonexistant file
with open(packets_path, 'r') as file:
    # TODO handle empty data
    packet_data = yaml.load(file)

known_device_packets = packet_data.get(args.device, [])

broadlinks = broadlink.discover(timeout=5)
broadlink = broadlinks[0]
broadlink.auth()

last_packet = None
packet = None
while True:
    broadlink.enter_learning()
    print("Learning", end="", flush=True)

    while packet is None or packet == last_packet:
        print(".", end="", flush=True)
        time.sleep(1)
        packet = broadlink.check_data()

    if not packet in known_device_packets:
        print(yaml.dump(packet), flush=True)
        print(flush=True)

        known_device_packets.append(packet)
        packet_data[args.device] = known_device_packets
        with open(packets_path, "w") as f:
            yaml.dump(packet_data, f)
    else:
        print("Already known packet, skipping")

    last_packet = packet
    packet = None
