#!/usr/bin/env python3
"""An app for controlling the broadlink."""

from broadlinky import Broadlinky

from flask import Flask
from flask import request


def build_app():
    """Initialize HTTP server for API."""
    # pylint: disable=C0103
    app = Flask(__name__)

    broadlinky = Broadlinky()

    @app.route('/')
    def hello_world():
        """Hello to the worldiest of worlds."""
        return 'Hello, World!'


    @app.route('/<device_id>/<namespace>', methods=['GET', 'POST'])
    def device_namespace_command_in_body(device_id=None, namespace=None):
        """Send a code to turn on a device."""
        # TODO check exists and 404 otherwise
        device = broadlinky.devices[device_id]

        if request.method == 'POST':
            command = request.data.decode('UTF-8')  # lol
            device.send_command(namespace, command)

        return device.states[namespace]

    @app.route('/<device_id>/<namespace>/<command>', methods=['GET', 'POST'])
    def device_namespace_command_in_url(device_id=None, namespace=None, command=None):
        """Send a code to turn on a device."""
        # TODO check exists and 404 otherwise
        device = broadlinky.devices[device_id]
        if request.method == 'POST':
            state = request.data.decode('UTF-8')  # lol

            if state == 'ON' or state == '': # no body, no problem
                device.send_command(namespace, command)
            elif state == 'OFF':
                device.turn_off()

        if device.states[namespace] == command:
            return 'ON'
        else:
            return 'OFF'

    return app

# pylint: disable=C0103
app = build_app()
