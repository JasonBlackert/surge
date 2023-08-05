import asyncio
import json
import logging
import time
from typing import Any, TypedDict

import paho.mqtt.client as mqtt

from pulse.util import parse_args
from pulse.util.database import Database
from pulse.util.store import Store

args = parse_args()
config = args.config

client = mqtt.Client()
logger = logging.getLogger(__name__)


class TelemetryData(TypedDict):
    timestamp: int
    mac_address: str
    ip_address: str


def subscribe(topic: str):
    queue: asyncio.Queue[TelemetryData] = asyncio.Queue()

    def on_message(_client: mqtt.Client, _userdata: Any, message: mqtt.MQTTMessage):
        try:
            payload: TelemetryData = json.loads(message.payload)
            queue.put_nowait(payload)
        except json.JSONDecodeError:
            logger.exception("Failed to decode message payload: %s", message.payload)
        except asyncio.QueueFull:
            logger.exception("Dropping message payload: %s", message.payload)

    client.subscribe(topic)
    client.message_callback_add(topic, on_message)

    return queue


class Cache(Store):
    def __init__(self) -> None:
        self.cache: dict[str, TelemetryData] = Database().populate_cache()

    def select_telemetry(self, measure: str) -> dict[str, Any]:
        return {id: self.cache[id][measure] for id in self.cache}

    def write_telemetry(self, data: TelemetryData):
        self.cache[data["mac_address"]] = data

    def stale_data_check(self):
        for mac in self.cache:
            if time.time() - self.cache[mac]["timestamp"] > 120:
                logger.info("Evicting cache entry for %s: %s", mac, self.cache[mac])
                del self.cache[mac]

    async def listen(self):
        client.connect(config["mqtt"]["host"], config["mqtt"]["port"])
        queue = subscribe("Yotta/+/json")
        client.loop_start()

        client.publish("Yotta/cmd", "set fast_period 1")

        while True:
            data = await queue.get()
            self.write_telemetry(data)
            self.stale_data_check()
