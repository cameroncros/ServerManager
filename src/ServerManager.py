import sys
import os
from os import system
from ExplicitSwitchDeviceInfo import ExplicitSwitchDeviceInfo
from wakeonlan import send_magic_packet


class ServerManager(ExplicitSwitchDeviceInfo):
    name = "Server Switch"
    short_id = "server_switch"
    location = "Server Room"
    server_mac = os.environ.get('SERVER_MAC').replace(':', '')
    server_addr = os.environ.get('SERVER_ADDR')

    def callback(self, state: bool):
        super().callback(state)
        if state:
            print("Starting Server", file=sys.stderr)
            send_magic_packet(self.server_mac)
        else:
            print("Stopping Server", file=sys.stderr)
            system(f'ssh -o StrictHostKeyChecking=no -i /app/id_rsa shutdown@{self.server_addr} "sudo shutdown"')

    def status_update(self):
        self.state = True if system(f'ping -c 1 {self.server_addr} 2>&1 >/dev/null') == 0 else False