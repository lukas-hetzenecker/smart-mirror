from PySide2.QtQml import qmlRegisterType, QQmlExtensionPlugin
  
from .weatherservice import WeatherService

qmlRegisterType(WeatherService, "Weather", 1, 0, "WeatherService")

