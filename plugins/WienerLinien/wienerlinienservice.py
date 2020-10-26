import logging
import asyncio
import urllib

import aiohttp
from multidict import MultiDict
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import QStringListModel
from PySide2.QtCore import QTimer
from PySide2.QtCore import Qt
from PySide2.QtCore import Property, Signal, Slot, QObject

from libs.ListModel import ListModel
from libs.ListModelItem import ListModelItem

base_url = 'https://www.wienerlinien.at/ogd_realtime/monitor'
HEADERS = {
    'user-agent': 'smart-mirror lukas@hetzenecker.me',
}

logger = logging.getLogger(__name__)

class WienerLinienService(QObject):
    rblsChanged = Signal('QVariantList')
    keyChanged = Signal(str)
    modelChanged = Signal('QVariant')

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rbls = []
        self._key = ''
        self._model = ListModel(WienerLinienItem)

    def getRbls(self):
        return self._rbls

    def setRbls(self, rbls):
        self._rbls = rbls
        self.rblsChanged.emit(self._rbls)

        logger.debug("rbls are now %s", self._rbls)

        #self._model.appendRow(WienerLinienItem(769, "Fendigasse", "14A", "Neubaugasse", [1, 7], self._model))
        #self._model.appendRow(WienerLinienItem(1698, "Reinprechtsdf. Str./Arbeiterg.", "59A", "Kärntner Ring", [1, 7], self._model))
        #self._model.appendRow(WienerLinienItem(1687, "Reinprechtsdf. Str./Arbeiterg.", "59A", "Neubaugasse", [2, 3], self._model))

        asyncio.ensure_future(self._update())

    rbls = Property('QVariantList', getRbls, setRbls, notify=rblsChanged)

    def getKey(self):
        return self._key

    def setKey(self, key):
        self._key = key
        self.keyChanged.emit(self._key)
        logger.debug("Key changed to %s", key)

    key = Property(str, getKey, setKey, notify=keyChanged)

    def getModel(self):
        return self._model

    model = Property('QVariant', getModel, notify=modelChanged)

    async def _update(self):
        if not (self._key and self._rbls):
            return

        try:

            logger.debug("update departures!")

            self._model.beginResetModel()
            self._model.clear()

            async with aiohttp.ClientSession() as session:
                params = MultiDict([('sender', self._key)] + [('rbl', rbl) for rbl in self._rbls])
                logger.debug("requesting %s?%s", base_url, urllib.parse.urlencode(params))

                async with session.get(base_url, headers=HEADERS, params=params) as resp:
                    logger.debug("Response: %s", resp)
                    data = await resp.json()
                    logger.debug("Data: %s", data)

                    monitors = data['data']['monitors']
                    for monitor in sorted(monitors, key=lambda m: m['locationStop']['properties']['attributes']['rbl']):
                        properties = monitor['locationStop']['properties']
                        rbl = properties['attributes']['rbl']
                        stop = properties['title']
                        line = monitor['lines'][0]
                        name = line['name']
                        direction = line['towards']

                        departures = [d['departureTime']['countdown'] for d in line['departures']['departure']][:3]

                        self._model.addItem(WienerLinienItem(self._model,
                                                             rbl=rbl,
                                                             stop=stop,
                                                             line=name,
                                                             direction=direction,
                                                             departures=departures))

            self._model.endResetModel()
        except Exception as e:
            logger.error(e)

        await asyncio.sleep(5)
        asyncio.ensure_future(self._update())
        #QTimer.singleShot(5000, lambda: asyncio.ensure_future(self._update()))

class WienerLinienItem(ListModelItem):
    roles = {
        Qt.UserRole + 1: b'rbl',
        Qt.UserRole + 2: b'stop',
        Qt.UserRole + 3: b'line',
        Qt.UserRole + 4: b'direction',
        Qt.UserRole + 5: b'departures',
    }
