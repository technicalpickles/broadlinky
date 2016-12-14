broadlinky!!
============

broadlinksy is an HTTP and MQTT bridge to control RF and IR devices via a [Broadlink RM Pro](http://www.ibroadlink.com/rm/)

<a href="https://www.amazon.com/Broadlink-Automation-Universal-Compatible-Smartphones-IR/dp/B01GIXZDKO"><img src="https://images-na.ssl-images-amazon.com/images/I/319nCGssbhL.jpg"></a>

```
You -> HTTP or MQTT -> broadlinky -> Broadlink RM Pro -> 433Mhz RF radio or IR -> your device
```

Concepts
--------

The RM Pro only really knows how to capture IR and RF signals, and emit them. It doesn't know anything about devices, or the state they are in.

Broadlinky adds this concept. You can configure any number of devices. A device can have different states, like 'power' or 'color'. Each state then has different values like 'on' and 'off' and an IR or RF signal to put it in that mode. The last value of the state is remembered so it can be queried later.

For example, an Etekcity Zap outlet has one state, power, that can be off or on. A Phillips Pick-A-Color has also has a power state, but it also has a 'color' (with red, blue, pink and others) and 'mode' (steady, twinkle, fade).

NOTE: this maps well to things that have state, but maybe not as much for 'actions' or up/down controls like on a TV remote. PR plz?

Usage
-----

```
$ python3 -m broadlinky.command_line --help
usage: broadlinky [-h] {learn,send,server} ...

positional arguments:
  {learn,send,server}  command help
    learn              learn device commands
    send               send a device command
    server             start webserver

optional arguments:
  -h, --help           show this help message and exit
```

Start with `learn`, passing in a name of a device and a state. This kicks of a loop to enter the RM Pro into learning mode, you can press the button, and it will let you know what it gets. Sometimes it takes a lot of pressing before it's captured. Once captured, you can replay it to confirm it works, and then save it as a value. Values are saved in `devices.yaml`.

You can test with `send`, specifying a device, state, and value to send.

Run `server` to start interacting it with over HTTP or MQTT. It integrates well with HomeAssistant using [Restful Switches](https://home-assistant.io/components/switch.rest/) and better yet [MQTT Switches](https://home-assistant.io/components/switch.mqtt/)

Examples
--------

Learn power settings for an outlet:

```
$ python3 -m broadlinky.command_line learn zap_319_2 power
Learning..
Learned a thing. Replay it to confirm functioning? yes
What do you want to save it as (Blank resumes learning) on
Learning.....................
Learned a thing. Replay it to confirm functioning? yes
What do you want to save it as (Blank resumes learning) off
Learning.^C
```

Test new settings:

```
$ python3 -m broadlinky.command_line send zap_319_2 power on
$ python3 -m broadlinky.command_line send zap_319_2 power off
```

HA Restful Switch for power:

```yaml
- platform: rest
  name: Nursery Night Lights
  resource: http://localhost:5000/nursery_night_lights/power
```

HA Restful swithces for changing color:

```yaml
- platform: rest
  name: Exterior Christmas Lights Blue
  resource: http://localhost:5000/exterior_christmas_lights/color/blue
- platform: rest
  name: Exterior Christmas Lights Red
  resource: http://localhost:5000/exterior_christmas_lights/color/red
```

HA MQTT Switch for controlling power:

```yaml
- platform: mqtt
  name: "Zap Outlet 1"
  state_topic:   "broadlinky/devices/zap_319_1/power/state"
  command_topic: "broadlinky/devices/zap_319_1/power/command"
  qos: 0
  optimistic: true
  payload_on: "on"
  payload_off: "off"
```

HA MQTT Switch for changing multiple colors:

```yaml
- platform: mqtt
  name: "Exterior Christmas Lights Cool White"
  state_topic:   "broadlinky/devices/exterior_christmas_lights/color/cool_white/state"
  command_topic: "broadlinky/devices/exterior_christmas_lights/color/cool_white/command"
  qos: 0
  optimistic: true
  payload_on: "on"
  payload_off: "off"

- platform: mqtt
  name: "Exterior Christmas Lights Red"
  state_topic:   "broadlinky/devices/exterior_christmas_lights/color/red/state"
  command_topic: "broadlinky/devices/exterior_christmas_lights/color/red/command"
  qos: 0
  optimistic: true
  payload_on: "on"
  payload_off: "off"

- platform: mqtt
  name: "Exterior Christmas Lights Blue"
  state_topic:   "broadlinky/devices/exterior_christmas_lights/color/blue/state"
  command_topic: "broadlinky/devices/exterior_christmas_lights/color/blue/command"
  qos: 0
  optimistic: true
  payload_on: "on"
  payload_off: "off"
```


Incomplete list of devices
--------------------------

<a href="https://www.amazon.com/Etekcity-Programmable-Electrical-Household-Appliances/dp/B00DQELHBS"><img src="https://cloud.githubusercontent.com/assets/260/10120707/3a85de1a-6497-11e5-86a5-f26cbd11de3d.jpeg" width="225"></a>

<a href="http://www.target.com/p/philips-25-ct-led-c9-faceted-pick-a-color-string-lights-with-remote-multicolored/-/A-50873237"><img src="http://target.scene7.com/is/image/Target/50873237?wid=450&hei=450&fmt=pjpeg"></a>
