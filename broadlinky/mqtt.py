import os
import re
import sys

import paho.mqtt.client as mqtt


def run(broadlinky):

    state_command_pattern = re.compile(r'broadlinky/devices/(?P<device>[^/]+)/(?P<state>[^/]+)/command')
    state_with_value_command_pattern = re.compile(r'broadlinky/devices/(?P<device>[^/]+)/(?P<state>[^/]+)/(?P<value>[^/]+)/command')

    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            if rc == 1:
                print("Connection refused - incorrect protocol version")
            elif rc == 2:
                print("Connection refused - invalid client identifier")
            elif rc == 3:
                print("Connection refused - server unavailable")
            elif rc == 4:
                print("Connection refused - bad username or password")
            elif rc == 5:
                print("Connection refused - not authorised")

            sys.exit()

        print("Connected.")
        # broadlinky/devices/<device>/<state>/command
        client.subscribe("broadlinky/devices/+/+/command")

        # broadlinky/devices/<device>/<state>/<value>/command
        client.subscribe("broadlinky/devices/+/+/+/command")

    def on_message(client, userdata, msg):
        state_command_match = state_command_pattern.match(msg.topic)
        state_with_value_command_match = state_with_value_command_pattern.match(msg.topic)
        payload = msg.payload.decode('UTF-8')

        if state_command_match:
            device_name = state_command_match.group('device')
            state = state_command_match.group('state')
            new_value = payload

            print("Handling state with value in payload, %s/%s: %s" % (device_name, state, new_value))
            device = broadlinky.get_device(device_name)
            device.set_state(state, new_value)

            # FIXME duplication below
            state_topic = 'broadlinky/devices/%s/%s/state'  % (device_name, state)
            client.publish(state_topic,
                           payload=new_value, qos=0, retain=True)

            for value in device.state_config[state]:
                if new_value == value:
                    new_value_payload = 'on'
                else:
                    new_value_payload = 'off'

                print("Updating %s/%s/%s: %s" % (device_name, state, value, new_value_payload))
                value_topic = 'broadlinky/devices/%s/%s/%s/state' % (device_name, state, value)
                client.publish(value_topic,
                               payload=new_value_payload, qos=0, retain=True)

        
        elif state_with_value_command_match:
            device_name = state_with_value_command_match.group('device')
            state = state_with_value_command_match.group('state')
            new_value = state_with_value_command_match.group('value')

            print("Handling state with value in topic, %s/%s: %s" % (device_name, state, new_value))
            device = broadlinky.get_device(device_name)
            device.set_state(state, new_value)

            state_topic = 'broadlinky/devices/%s/%s/state'  % (device_name, state)
            client.publish(state_topic,
                           payload=new_value, qos=0, retain=True)

            for value in device.state_config[state]:
                if new_value == value:
                    new_value_payload = 'on'
                else:
                    new_value_payload = 'off'

                print("Updating %s/%s/%s: %s" % (device_name, state, value, new_value_payload))
                value_topic = 'broadlinky/devices/%s/%s/%s/state' % (device_name, state, value)
                client.publish(value_topic,
                               payload=new_value_payload, qos=0, retain=True)

        else:
            print("unhandled topic " + msg.topic + ": " + payload)

    # FIXME use a URL w/ host, port, user, pass instead of multiple env
    user = os.environ['BROADLINKY_MQTT_USER']
    password = os.environ['BROADLINKY_MQTT_PASSWORD']
    host = os.environ['BROADLINKY_MQTT_HOST']
    port = int(os.environ['BROADLINKY_MQTT_PORT'])
    client = mqtt.Client(protocol=mqtt.MQTTv31)
    client.username_pw_set(user, password)
    # FIXME make exit enter process on failure (HTTP still up)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, 60)
    client.loop_start()
