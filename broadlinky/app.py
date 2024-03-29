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


    @app.route('/<device_id>/<state>', methods=['GET', 'POST'])
    def device_namespace_command_in_body(device_id=None, state=None):
        """Send a code to turn on a device."""
        # TODO check exists and 404 otherwise
        device = broadlinky.devices[device_id]

        if request.method == 'POST':
            state_value = request.data.decode('UTF-8')  # lol
            device.set_state(state, state_value)

        return device.states[state]

    @app.route('/<device_id>/<state>/<state_value>', methods=['GET', 'POST'])
    def device_namespace_command_in_url(device_id=None, state=None, state_value=None):
        """Send a code to turn on a device."""
        # TODO check exists and 404 otherwise
        device = broadlinky.devices[device_id]
        if request.method == 'POST':
            state = request.data.decode('UTF-8')  # lol

            if state == 'ON' or state == '': # no body, no problem
                device.set_state(state, state_value)
            elif state == 'OFF':
                device.turn_off()

        if device.states.get(state) == state_value:
            return 'ON'
        else:
            return 'OFF'

    return app

# pylint: disable=C0103
app = build_app()
