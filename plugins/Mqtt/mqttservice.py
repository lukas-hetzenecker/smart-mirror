import logging
import asyncio
import collections

from hbmqtt.client import MQTTClient, ClientException

from PySide2.QtCore import Property, Signal, Slot, QObject, QThread
from asyncqt import asyncSlot

logger = logging.getLogger(__name__)


class MqttService(QObject):
    hostnameChanged = Signal(str)
    portChanged = Signal(int)
    secureChanged = Signal(bool)
    passwordChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hostname = "localhost"
        self._port = 1883
        self._client = None

    def getHostname(self):
        return self._hostname

    def setHostname(self, hostname):
        self._hostname = hostname
        self.hostnameChanged.emit(self._hostname)

    hostname = Property(str, getHostname, setHostname, notify=hostnameChanged)

    def getPort(self):
        return self._port

    def setPort(self, port):
        self._port = port
        self.portChanged.emit(self._port)

    port = Property(int, getPort, setPort, notify=portChanged)

    @asyncSlot()
    async def start(self):
        self._client = MQTTClient(config={'reconnect_retries': 500})
        try:
            await self._client.connect('mqtt://%s:%s/' % (self._hostname, self._port))
        except ClientException as ce:
            logger.error("Client exception: %s" % ce)

    @asyncSlot(str, str)
    async def publish(self, topic, payload):
        if self._client is None or not self._client._connected_state.is_set():
            return
        try:
            await self._client.publish(topic, payload.encode())
        except ClientException as ce:
            logger.error("Client exception: %s" % ce)
