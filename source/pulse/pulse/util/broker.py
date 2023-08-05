import itertools
import logging

import paho.mqtt.client as mqtt

from pulse.util import parse_args

args = parse_args()
config = args.config

log = logging.getLogger(__name__)


class MqttBroker:
    def __init__(self):
        self.broker = mqtt.Client()
        self.broker.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        log.info("Broker connected with result code " + str(rc))

    def start(self):
        self.broker.connect(config["mqtt"]["host"], config["mqtt"]["port"])
        self.broker.loop_start()

    def multicast(self, cmds: list[str], msg="Multicasting") -> None:
        log.info(f"{msg}: {cmds}")
        for cmd in cmds:
            self.broker.publish("Pulse/cmd", cmd)

    def unicast(self, cmds: list[str], macs: list[str], msg="Unicasting") -> None:
        log.info(f"{msg}: {cmds} to {macs}")
        for cmd, mac in itertools.product(cmds, macs):
            self.broker.publish(f"Pulse/{mac}/cmd", cmd)
