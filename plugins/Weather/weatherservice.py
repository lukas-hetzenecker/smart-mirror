import logging
import asyncio
import aiohttp
from PySide2.QtCore import QTimer

from PySide2.QtCore import Property, Signal, QObject

base_url = 'https://api.darksky.net/forecast/'
HEADERS = {
    'user-agent': 'smart-mirror lukas@hetzenecker.me',
}

logger = logging.getLogger(__name__)


class WeatherService(QObject):
    temperatureChanged = Signal(int)
    apparentTemperatureChanged = Signal(int)
    textChanged = Signal(str)
    iconChanged = Signal(str)

    cityChanged = Signal(str)
    keyChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._city = ''
        self._key = ''
        self._temperature = 0
        self._apparentTemperature = 0
        self._text = ''
        self._icon = ''

    def getCity(self):
        return self._city

    def setCity(self, city):
        self._city = city
        self.cityChanged.emit(city)

        logger.debug("City changed to %s", city)
        asyncio.ensure_future(self._update())

    city = Property(str, getCity, setCity, notify=cityChanged)

    def getKey(self):
        return self._key

    def setKey(self, key):
        self._key = key
        self.keyChanged.emit(key)
        logger.debug("Key changed to %s", key)

        asyncio.ensure_future(self._update())

    key = Property(str, getKey, setKey, notify=keyChanged)

    def getTemperature(self):
        return self._temperature

    temperature = Property(int, getTemperature, notify=temperatureChanged)

    def getApparentTemperature(self):
        return self._apparentTemperature

    apparentTemperature = Property(int, getApparentTemperature, notify=apparentTemperatureChanged)

    def getText(self):
        return self._text

    text = Property(str, getText, notify=textChanged)

    def getIcon(self):
        return self._icon

    icon = Property(str, getIcon, notify=iconChanged)

    async def _update(self):
        if not (self._key and self._city):
            return

        logger.debug("update weather!")

        url = base_url + self._key + '/' + self._city
        params = {
            'units': 'si'
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=HEADERS, params=params) as resp:
                    logger.debug("response: %s", resp)
                    data = await resp.json()
                    logger.debug("data: %s", data)

                    temperature = round(data['currently']['temperature'])
                    if temperature != self._temperature:
                        self._temperature = temperature
                        self.temperatureChanged.emit(temperature)


                    apparentTemperature = round(data['currently']['apparentTemperature'])
                    if apparentTemperature != self._apparentTemperature:
                        self._apparentTemperature = apparentTemperature
                        self.apparentTemperatureChanged.emit(apparentTemperature)

                    icon = data['currently']['icon']
                    if icon != self._icon:
                        self._icon = icon
                        print("icon changed!")
                        self.iconChanged.emit(icon)

                    #if data['daily']['data'][0]['precipProbability'] >= 0.2:
                    text = data['daily']['data'][0]['summary']
                    if text != self._text:
                        self._text = text
                        self.textChanged.emit(text)
                    #else:
                    #    self._text = ''
        except Exception as e:
            logger.error(e)

        QTimer.singleShot(1000 * 60 * 10, lambda: asyncio.ensure_future(self._update()))

