import broadlink
from IPython import embed
import time
import yaml

with open('codes.yaml', 'r') as file:
    data = yaml.load(file)

devices = broadlink.discover(timeout=5)
device = devices[0]
device.auth()
embed()
