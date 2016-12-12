"""Interface for discovering/sending codes with a Broadlink device."""
import os
import re
import time

import broadlink
import yaml


class Device:
    def __init__(self, broadlinky, name, device_commands):
        self.broadlinky = broadlinky
        self.name = name
        self.device_commands = device_commands
        self.state = 'OFF'

    def turn_on(self):
        self.send_command('on')

    def turn_off(self):
        self.send_command('on')

    def send_command(self, command_name):
        command_name = command_name.lower()
        new_state = None
        if command_name == 'on':
            packet = self.device_commands[True]
            new_state = 'ON'
        elif command_name == 'off':
            packet = self.device_commands[False]
            new_state = 'OFF'
        elif re.search(r"^\d+$", command_name):
            packet = self.device_commands[int(command_name)]
        else:
            packet = self.device_commands[command_name]

        self.broadlinky.broadlink.send_data(packet)
        if new_state is not None:
            self.state = new_state

        return new_state


class Broadlinky:
    """Interface for grouping IR/RF packets into logical devices."""

    def __init__(self, packets_path=None, devices_path=None):
        if packets_path is None:
            packets_path = os.path.dirname(os.path.abspath(__file__)) + '/../packets.yaml'
        self.packets_path = packets_path
        # TODO handle nonexistant file
        with open(packets_path, 'r') as file:
            # TODO handle empty data
            self.packet_data = yaml.load(file)

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

    def known_device_packets(self, device_name):
        """Known packets for a device."""
        return self.packet_data.get(device_name, [])

    # TODO timeout argument?
    def learn_device_packet(self, device_name):
        """Learn an IR or RF packet for the device."""
        print("Learning", end="", flush=True)

        known_device_packets = self.known_device_packets(device_name)

        packet = None
        self.broadlink.enter_learning()
        while packet is None or packet == self.last_learned_packet:
            print(".", end="", flush=True)
            time.sleep(1)
            packet = self.broadlink.check_data()

        if not packet in known_device_packets:
            print("\n" + yaml.dump(packet), flush=True)
            self.remember_device_packet(device_name, packet, known_device_packets)
            return packet

    def remember_device_packet(self, device_name, packet, known_device_packets):
        """Remember a device packet for later."""
        known_device_packets.append(packet)
        self.packet_data[device_name] = known_device_packets

        with open(self.packets_path, "w") as packets_file:
            yaml.dump(self.packet_data, packets_file)

    def send_device_command(self, device_name, command_name):
        """Send a named command to a device."""
        device_commands = self.devices_data[device_name]

        if command_name == 'on':
            packet = device_commands[True]
        elif command_name == 'off':
            packet = device_commands[False]
        elif re.search(r"^\d+$", command_name):
            packet = device_commands[int(command_name)]
        else:
            packet = device_commands[command_name]

        self.broadlink.send_data(packet)
