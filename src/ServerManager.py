import sys
import time
from os import system

from wakeonlan import send_magic_packet

from AbstractSwitch import AbstractSwitch


class ServerManager(AbstractSwitch):

    def start(self):
        print("Starting Server", file=sys.stderr)
        send_magic_packet('5065f3346ca6')

    def stop(self):
        print("Stopping Server", file=sys.stderr)
        system('ssh -o StrictHostKeyChecking=no -i /app/id_rsa shutdown@192.168.1.150 "sudo shutdown"')

    def status_update(self):
        while True:
            server_up = True if system('ping -c 1 192.168.1.150 2>&1 >/dev/null') == 0 else False
            self.set_state(on=server_up)
            if server_up:
                print("Server is: ON", file=sys.stderr)
            else:
                print("Server is: OFF", file=sys.stderr)

            time.sleep(1)
