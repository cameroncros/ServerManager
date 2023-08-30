import os
import sys

from wakeonlan import send_magic_packet
import paho.mqtt.client as mqtt

from ExplicitSwitchDeviceInfo import ExplicitSwitchDeviceInfo


# Debugging: mosquitto_sub -h 192.168.1.152 -p 36669 -P multimqttservice -u hisenseservice -t "#" --insecure --cafile /etc/mosquitto/tv.crt -v
class TVManager(ExplicitSwitchDeviceInfo):
    name = "TV Switch"
    short_id = "tv_switch"
    location = "Living Room"

    tv_mac = os.environ.get('TV_MAC').replace(':', '')
    tv_addr = os.environ.get('TV_ADDR')

    def callback(self, state: bool):
        super().callback(state)
        if state:
            print("Starting TV", file=sys.stderr)
            send_magic_packet(self.tv_mac)
        else:
            print("Stopping TV", file=sys.stderr)
            self.stop()

    def _connect_tv(self) -> mqtt.Client:
        tvmqttclient = mqtt.Client(client_id="hisenseservice")
        tvmqttclient.username_pw_set('hisenseservice', 'multimqttservice')
        tvmqttclient.tls_set(ca_certs='tv.crt')
        tvmqttclient.tls_insecure_set(True)
        tvmqttclient.connect(self.tv_addr, 36669)
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
        try:
            connection = self._connect_tv()
            self.state = True
            connection.disconnect()
        except Exception:
            self.state = False
