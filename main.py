import json
from typing import Optional

from wakeonlan import send_magic_packet
from os import system
import paho.mqtt.client as mqtt
import sys
import time
import threading

def startserver():
    print("Starting Server", file=sys.stderr)
    send_magic_packet('5065f3346ca6')



def stopserver():
    print("Stopping Server", file=sys.stderr)
    system('ssh -o StrictHostKeyChecking=no -i /app/id_rsa shutdown@192.168.1.150 "sudo shutdown"')
    #    fabric.Connection(host='192.168.1.150',
    #                      user='shutdown',
    #                      connect_kwargs={
    #                          'key_filename': '/app/id_rsa'
    #                      }).run('sudo shutdown')
    #    client = paramiko.SSHClient()
    #    client.load_system_host_keys()
    #    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #    pkey = paramiko.RSAKey(filename='/app/id_rsa')
    #    client.connect('192.168.1.150', username='shutdown', pkey=pkey)
    #    stdin, stdout, stderr = client.exec_command('sudo shutdown')
    #    print(stdout)
    #    print(stderr)
    #    client.close()



def on_message(client: mqtt.Client, userdata: str, message):
    print(f'{client} - {userdata} - {message}')
    
    if message.topic == 'homeassistant/status' and message.payload == 'online':
        register(client)
    
    if message.topic != 'ServerRoom/server/set':
        return

    if message.payload == b'ON':
        startserver()
    else:
        stopserver()


def status_update(client):
    while True:
        server_up = True if system('ping -c 1 192.168.1.150 2>&1 >/dev/null') == 0 else False
        if server_up:
            client.publish("ServerRoom/server/state", payload='ON', retain=True, qos=0)
            print("Server is: ON", file=sys.stderr)
        else:
            client.publish("ServerRoom/server/state", payload='OFF', retain=True, qos=0)
            print("Server is: OFF", file=sys.stderr)

        time.sleep(1)


def register(client):
    config = json.dumps(
        {'name': 'Server',
         'command_topic': "ServerRoom/server/set",
         'state_topic': "ServerRoom/server/state",
         'unique_id': "server_manager",
         'device': {
             'name': 'server',
             'model': 'server',
             'manufacturer': 'cameron',
             'sw_version': 0.1,
             'suggested_area': 'Server Room',
             'identifiers': ['server_manager']
         }
         })

    client.publish("homeassistant/switch/ServerRoom/server/config", payload=config, retain=True, qos=0)
    client.on_message = on_message
    client.subscribe("ServerRoom/server/set")


if __name__ == '__main__':
    client = mqtt.Client(client_id="server_manager")
    client.connect('192.168.1.100')
    register(client)

    threading.Thread(target=status_update, args=(client,)).start()
    client.loop_forever()
