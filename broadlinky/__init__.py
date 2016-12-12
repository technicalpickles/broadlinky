"""Interface for discovering/sending codes with a Broadlink device."""
import os
import time

import broadlink
import yaml


class Broadlinky:
    """Interface for grouping IR/RF packets into logical devices."""

    def __init__(self, packets_path=None):
        if packets_path is None:
            packets_path = os.path.dirname(os.path.abspath(__file__)) + '/../packets.yaml'
        self.packets_path = packets_path
        # TODO handle nonexistant file
        with open(packets_path, 'r') as file:
            # TODO handle empty data
            self.packet_data = yaml.load(file)

        # TODO handle multiples?
        broadlinks = broadlink.discover(timeout=5)
        self.broadlink = broadlinks[0]
        self.broadlink.auth()

        self.last_learned_packet = None

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
