import logging
import asyncio
from datetime import datetime

import websockets
import aiohttp
import json
import ssl
import collections

from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import QDate
from PySide2.QtCore import QDateTime
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import Property, Signal, Slot, QObject
from PySide2.QtCore import Qt

from libs.ListModel import ListModel
from libs.ListModelItem import ListModelItem

logger = logging.getLogger(__name__)

BASE_URL = 'https://slack.com/api/'
HEADERS = {
    'user-agent': 'smart-mirror lukas@hetzenecker.me',
}
MESSAGE_REQUEST_COUNT = 150


class SlackService(QObject):
    tokenChanged = Signal(str)
    channelsChanged = Signal('QVariant')

    def __init__(self, parent=None):
        super().__init__(parent)

        self.session = None

        self._token = None
        self._channelsModel = ChannelModel(ChannelItem, self)

    def getToken(self):
        return self._token

    def setToken(self, token):
        self._token = token
        self.tokenChanged.emit(self._token)

    token = Property(str, getToken, setToken, notify=tokenChanged)

    def getChannels(self):
        return self._channelsModel

    channels = Property('QVariant', getChannels, notify=channelsChanged)

    @Slot()
    def start(self):
        asyncio.ensure_future(self._start())

    async def _start(self):
        logger.debug("connecting to slack...")

        if not self._token:
            return logger.error('No token!')

        try:
            self.session = aiohttp.ClientSession()

            url = BASE_URL + 'rtm.start'
            params = {
                'token': self._token,
            }

            async with self.session.get(url, headers=HEADERS, params=params) as resp:
                logger.debug("response: %s", resp)
                data = await resp.json()
                logger.debug("data: %s", data)

            url = data['url']

            for channel in data['channels']:
                self._channelsModel.addChannel(channel)

            logger.debug('Connecting to slack websocket %s ...', url)
            self._websocket = await websockets.connect(url)
            logger.debug('Connected to slack websocket')

            while True:
                data = await self._websocket.recv()
                if not data:
                    break
                message = json.loads(data)
                if message['type'] == 'channel_joined':
                    self._channelsModel.addChannel(message['channel'])
                elif message['type'] == 'channel_left':
                    self._channelsModel.removeChannel(message['channel'])
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(10.0)
            asyncio.ensure_future(self._start())


class ChannelModel(ListModel):
    def addChannel(self, channel_data):
        if not channel_data['is_member']:
            return

        logger.debug("add channel %s", channel_data['name'])
        self.addItem(ChannelItem(channel_id=channel_data['id'],
                                 name=channel_data['name'],
                                 messageModel=MessagesModel(MessagesItem, channel_data['id'], self)))

    def removeChannel(self, channel_id):
        index = self.indexOf(b'id', channel_id)
        self.removeIndex(index)

    @property
    def slackService(self):
        return self.parent


class ChannelItem(ListModelItem):
    roles = {
        Qt.UserRole + 1: b'id',
        Qt.UserRole + 2: b'name',
        Qt.UserRole + 3: b'messageModel',
    }

    def __init__(self, parent=None, **kwargs):
        super(ChannelItem, self).__init__(parent, **kwargs)
        self.messageModel.requestMore()

    def getId(self):
        return self._data[b'id']

    id = Property(str, getId)

    def getMessageModel(self):
        return self._data[b'messageModel']

    messageModel = Property('QVariant', getMessageModel)


class MessagesModel(ListModel):
    def __init__(self, prototype, channel_id, parent=None):
        super(MessagesModel, self).__init__(prototype, parent)
        self._channel_id = channel_id
        self._latest = ''

    def requestMore(self):
        asyncio.ensure_future(self._requestMore())

    async def _requestMore(self):
        logger.debug("Request more messages from channel %s", self.channelId)
        url = BASE_URL + 'channels.history'
        params = {
            'token': self.slackService.token,
            'channel': self.channelId,
            'count': MESSAGE_REQUEST_COUNT,
            'latest': self._latest
        }
        async with self.slackService.session.get(url, headers=HEADERS, params=params) as resp:
            logger.debug("response: %s", resp)
            data = await resp.json()
            #logger.debug("data: %s", data)
            messageData = data['messages']
            if messageData:
                self._latest = messageData[0]['ts']
            messages = [
                MessagesItem(
                    ts=QDateTime.fromMSecsSinceEpoch(float(m['ts'])*1000),
                    date=QDateTime.fromMSecsSinceEpoch(float(m['ts'])*1000).date(),
                    time=QDateTime.fromMSecsSinceEpoch(float(m['ts'])*1000).time(),
                    user=m.get('username', m.get('user')),
                    text=m['text']
                ) for m in data['messages'] if m['type'] == 'message'
            ]

            self.addItems(list(reversed(messages)))


    @property
    def channelModel(self):
        return self.parent

    @property
    def slackService(self):
        return self.channelModel.slackService

    def getChannelId(self):
        return self._channel_id

    channelId = Property(str, getChannelId)

class MessagesItem(ListModelItem):
    roles = {
        Qt.UserRole + 1: b'ts',
        Qt.UserRole + 2: b'date',
        Qt.UserRole + 3: b'time',
        Qt.UserRole + 4: b'user',
        Qt.UserRole + 5: b'text',
    }

    def getTimestamp(self):
        return self._data[b'ts']

    timestamp = Property(QDateTime, getTimestamp)

    def getDate(self):
        return self._data[b'date']

    date = Property(QDate, getDate)

    def getTime(self):
        return self._data[b'time']

    time = Property(QDateTime, getTime)

    def getUser(self):
        return self._data[b'user']

    user = Property(str, getUser)

    def getText(self):
        return self._data[b'text']

    text = Property(str, getText)

