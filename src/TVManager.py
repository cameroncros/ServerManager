import sys
import time
from os import system

from wakeonlan import send_magic_packet

from AbstractSwitch import AbstractSwitch
import paho.mqtt.client as mqtt


# Debugging: mosquitto_sub -h 192.168.1.152 -p 36669 -P multimqttservice -u hisenseservice -t "#" --insecure --cafile /etc/mosquitto/tv.crt -v
class TVManager(AbstractSwitch):
    tv_mac = '10:C7:53:E0:0E:F8'

    def start(self):
        print("Starting TV", file=sys.stderr)
        send_magic_packet(self.tv_mac.replace(':', ''))

    @staticmethod
    def _connect_tv() -> mqtt.Client:
        tvmqttclient = mqtt.Client(client_id="hisenseservice")
        tvmqttclient.username_pw_set('hisenseservice', 'multimqttservice')
        tvmqttclient.tls_set(ca_certs='tv.crt')
        tvmqttclient.tls_insecure_set(True)
        tvmqttclient.connect('192.168.1.152', 36669)
        return tvmqttclient

    def stop(self):
        print("Stopping TV", file=sys.stderr)
        try:
            tvmqttclient = self._connect_tv()

            tvmqttclient.publish("/remoteapp/tv/remote_service/A8:DB:03:85:87:F2$normal/actions/sendkey",
                                 payload='KEY_POWER', retain=False, qos=0)
            tvmqttclient.disconnect()
        except Exception as e:
            print(f'Failed to stop TV: {e}', file=sys.stderr)

    def status_update(self):
        while True:
            try:
                connection = self._connect_tv()
                print("TV is: ON", file=sys.stderr)
                self.set_state(on=True)
                connection.disconnect()
            except Exception:
                print("TV is: OFF", file=sys.stderr)
                self.set_state(on=False)

            time.sleep(1)
