from typing import override

import paho.mqtt.client as mqtt

from .transmitter import Transmitter
from .uplink import Uplink

DEFAULT_TOPIC_TEMPLATE = "beebait/{id}/uplink"
MAX_QUEUED_MESSAGES = 1000


class MqttTransmitter(Transmitter):
    def __init__(
        self,
        host: str,
        port: int = 1883,
        topic_template: str = DEFAULT_TOPIC_TEMPLATE,
        qos: int = 1,
        client_id: str = "beebait-simulator",
    ):
        self.host = host
        self.port = port
        self.topic_template = topic_template
        self.qos = qos

        self._client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2, client_id=client_id
        )
        self._client.max_queued_messages_set(MAX_QUEUED_MESSAGES)
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect

        self._client.connect_async(host, port)
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, reason_code, properties) -> None:
        print(f"MQTT connected to {self.host}:{self.port} ({reason_code})", flush=True)

    def _on_disconnect(
        self, client, userdata, flags, reason_code, properties
    ) -> None:
        print(f"MQTT disconnected from {self.host}:{self.port} ({reason_code})", flush=True)

    @override
    def transmit(self, uplink: Uplink) -> None:
        topic = self.topic_template.format(id=uplink.beebait_id)

        self._client.publish(topic, uplink.to_json(), qos=self.qos)

    @override
    def close(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()
