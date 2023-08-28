import logging
import os
from time import sleep

from ham import MqttManager

from ServerManager import ServerManager
from TVManager import TVManager

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    mqtt_serv = os.environ.get('MQTT_SERV')
    mqtt_user = os.environ.get('MQTT_USER')
    mqtt_pass = os.environ.get('MQTT_PASS')

    server_switch = ServerManager()
    tv_switch = TVManager()
    manager = MqttManager(host=mqtt_serv,
                          username=mqtt_user,
                          password=mqtt_pass,
                          name="server_manager",
                          unique_identifier="server_manager",
                          base_topic="server_manager",
                          node_id="server_manager")
    manager.add_things([server_switch, tv_switch])

    manager.start()

    print("Entering an infinite loop, Ctrl+C multiple times to exit.")
    while True:
        server_switch.status_update()
        tv_switch.status_update()
        sleep(1)
