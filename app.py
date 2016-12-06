#!/usr/bin/env python3
"""An app for controlling the broadlink."""

import os
import yaml

import broadlink
from flask import Flask
from flask import request


# pylint: disable=C0103
app = Flask(__name__)

CODES_PATH = os.path.dirname(os.path.abspath(__file__)) + '/codes.yaml'
with open(CODES_PATH, 'r') as file:
    CODE_DATA = yaml.load(file)

BROADLINKS = broadlink.discover(timeout=5)
BROADLINK = BROADLINKS[0]
BROADLINK.auth()

DEVICE_STATE = {}


@app.route('/')
def hello_world():
    """Hello to the worldiest of worlds."""
    return 'Hello, World!'


@app.route('/<device_id>', methods=['GET', 'POST'])
def device(device_id=None):
    """Send a code to turn on a device."""
    if request.method == 'POST':
        packet = None

        state = request.data.decode('UTF-8')  # lol
        print(state)
        if state == 'ON':
            packet = CODE_DATA[device_id][True]
        elif state == 'OFF':
            packet = CODE_DATA[device_id][False]

        if packet is not None:
            BROADLINK.send_data(packet)
            DEVICE_STATE[device_id] = state
            print(state)
            return state
        else:
            return 'WHAT? ' + str(request.data)
    else:
        state = DEVICE_STATE.get(device_id, 'OFF')
        print(state)
        return state

# @app.route('/<device>/on')
# def device_on(device=None):
#     """Send a code to turn on a device."""
#     packet = CODE_DATA[device][True]
#     BROADLINK.send_data(packet)
#     return 'OK'
#
#
# @app.route('/<device>/off')
# def device_off(device=None):
#     """Send a code to turn off a device."""
#     packet = CODE_DATA[device][False]
#     BROADLINK.send_data(packet)
#     return 'OK'
