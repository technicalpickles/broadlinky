"""Interface for discovering/sending codes with a Broadlink device."""
import os
import re
import time

import broadlink
import yaml


class Device:
    def __init__(self, broadlinky, name, state_config):
        self.broadlinky = broadlinky
        self.name = name
        self.state_config = state_config
        self.states = {'power': 'OFF'}

    def turn_on(self):
        return self.set_state('power', 'on')

    def turn_off(self):
        return self.set_state('power', 'off')

    def set_state(self, state, value):
        value = value.lower()

        new_state = None
        state_config = self.state_config[state]
        if value == 'on':
            packet = state_config[True]
            new_state = 'ON'
        elif value == 'off':
            # toggle just sends on again
            if state_config.get('toggle', False):
                packet = state_config[True]
            else:
                packet = state_config[False]
            # TODO how to handle drift?
            new_state = 'OFF'
        elif re.search(r"^\d+$", value):
            packet = state_config[int(value)]
            new_state = value
        else:
            packet = state_config[value]
            new_state = value

        self.broadlinky.send_data(packet)
        if new_state is not None:
            self.states[state] = new_state

        return new_state

    def remember_state_value_packet(self, state, value, packet):
        if state not in self.state_config:
            self.state_config[state] = {}

        if value == 'on':
            value = True
        elif value == 'off':
            value = False

        self.state_config[state][value] = packet
        self.broadlinky.save()


class Broadlinky:
    """Interface for grouping IR/RF packets into logical devices."""

    def __init__(self, devices_path=None):
        if devices_path is None:
            devices_path = os.path.dirname(os.path.abspath(__file__)) + '/../devices.yaml'
        self.devices_path = devices_path
        with open(devices_path, 'r') as file:
            self.devices_data = yaml.load(file)

        # TODO handle multiples?
        broadlinks = broadlink.discover(timeout=5)
        self.broadlink = broadlinks[0]
        self.broadlink.auth()

        self.last_learned_packet = None

        self.devices = dict((name, Device(self, name, device_commands))
                        for name, device_commands in self.devices_data.items())

    def get_device(self, device_name):
        if device_name not in self.devices:
            device = Device(self, device_name, {})
            self.devices[device_name] = device
            self.devices_data[device_name] = device.state_config

        return self.devices[device_name]

    def known_device_packets(self, device_name):
        """Known packets for a device."""
        return self.packet_data.get(device_name, [])

    # TODO timeout argument?
    def learn(self):
        """Learn an IR or RF packet for the device."""
        print("Learning", end="", flush=True)

        packet = None
        self.broadlink.enter_learning()
        while packet is None or packet == self.last_learned_packet:
            print(".", end="", flush=True)
            time.sleep(1)
            packet = self.broadlink.check_data()

        print(flush=True)
        return packet

    def save(self):
        with open(self.devices_path, "w") as devices_file:
            # TODO preserve comments?
            yaml.dump(self.devices_data, devices_file)

    def send_data(self, packet):
        self.broadlink.send_data(packet)
