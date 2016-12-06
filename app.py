#!/usr/bin/env python3
"""An app for controlling the broadlink."""

import os
import yaml

import broadlink
from flask import Flask

# pylint: disable=C0103
app = Flask(__name__)

CODES_PATH = os.path.dirname(os.path.abspath(__file__)) + '/codes.yaml'
with open(CODES_PATH, 'r') as file:
    CODE_DATA = yaml.load(file)

BROADLINKS = broadlink.discover(timeout=5)
BROADLINK = BROADLINKS[0]
BROADLINK.auth()


@app.route('/')
def hello_world():
    """Hello to the worldiest of worlds."""
    return 'Hello, World!'


@app.route('/<device>/on')
def device_on(device=None):
    """Send a code to turn on a device."""
    packet = CODE_DATA[device][True]
    BROADLINK.send_data(packet)
    return 'OK'


@app.route('/<device>/off')
def device_off(device=None):
    """Send a code to turn off a device."""
    packet = CODE_DATA[device][False]
    BROADLINK.send_data(packet)
    return 'OK'
