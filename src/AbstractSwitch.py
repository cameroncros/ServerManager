import json
import threading
import time
from abc import ABC, abstractmethod
from paho.mqtt.client import Client


class AbstractSwitch(ABC):

    def __init__(self, client: Client, name: str, room=""):
        self.name = name
        self.room = room
        self.client = client
        self.register()
        threading.Thread(target=self.status_update).start()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def status_update(self):
        pass

    def set_state(self, on: bool):
        self.client.publish(f"{self.room}/{self.name}/state", payload='ON' if on else 'OFF', retain=False, qos=0)

    def on_message(self, topic: str, payload: bytes):
        if topic != f"{self.room}/{self.name}/set":
            return

        if payload == b'ON':
            self.start()
        else:
            self.stop()

    def register(self):
        config = json.dumps(
            {'name': self.name,
             'command_topic': f"{self.room}/{self.name}/set",
             'state_topic': f"{self.room}/{self.name}/state",
             'state_on': 'ON',
             'state_off': 'OFF',
             'unique_id': self.name,
             'device': {
                 'name': self.name,
                 'model': 'BasicSwitch',
                 'manufacturer': 'cameron',
                 'sw_version': 0.1,
                 'suggested_area': self.room,
                 'identifiers': [self.name]
             }
             })
        self.client.publish(f"homeassistant/switch/{self.room}/{self.name}/config", payload=config, retain=False, qos=0)
        self.client.subscribe(f"{self.room}/{self.name}/set")
        time.sleep(1)
        self.set_state(on=True)
