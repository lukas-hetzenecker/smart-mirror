from PySide2.QtQml import qmlRegisterType, QQmlExtensionPlugin
  
from .serialservice import SerialService

qmlRegisterType(SerialService, "Serial", 1, 0, "SerialService")

