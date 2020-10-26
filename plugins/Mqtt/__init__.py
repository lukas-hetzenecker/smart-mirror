from PySide2.QtQml import qmlRegisterType, QQmlExtensionPlugin
  
from .mqttservice import MqttService

qmlRegisterType(MqttService, "Mqtt", 1, 0, "MqttService")

