import broadlink
from IPython import embed
import time
import yaml


devices = broadlink.discover(timeout=5)
device = devices[0]
device.auth()
device.enter_learning()

packet = None

print("Learning", end="", flush=True)
while packet is None:
    print(".", end="", flush=True)
    time.sleep(5)
    packet = device.check_data()

print()

print(yaml.dump(packet))
embed()
