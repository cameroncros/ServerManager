import paho.mqtt.client as mqtt
import sys
from datetime import datetime

from ServerManager import ServerManager


def on_message(client: mqtt.Client, userdata: str, message):
    print(f'{datetime.now()} - {client} - {userdata} - {message}', file=sys.stderr)

    if message.topic == 'homeassistant/status' and message.payload == 'online':
        for plugin in plugins:
            plugin.register()

    for plugin in plugins:
        plugin.on_message(message.topic, message.payload)


if __name__ == '__main__':
    mqttclient = mqtt.Client(client_id="server_manager")
    mqttclient.connect('192.168.1.100')
    mqttclient.on_message = on_message
    plugins = [ServerManager(mqttclient, name="server", room="ServerRoom")]
    mqttclient.loop_forever()
