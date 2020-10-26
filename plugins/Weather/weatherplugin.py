from PyQt5.QtQml import qmlRegisterType, QQmlExtensionPlugin

from weatherservice import WeatherService


class ChartsPlugin(QQmlExtensionPlugin):

    def registerTypes(self, uri):
        qmlRegisterType(WeatherService, "Weather", 1, 0, "WeatherService")

