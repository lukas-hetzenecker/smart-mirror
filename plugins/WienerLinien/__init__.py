from PySide2.QtQml import qmlRegisterType, QQmlExtensionPlugin

from .wienerlinienservice import WienerLinienService

qmlRegisterType(WienerLinienService, "WienerLinien", 1, 0, "WienerLinienService")
