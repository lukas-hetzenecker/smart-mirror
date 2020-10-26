from PyQt5.QtQml import qmlRegisterType, QQmlExtensionPlugin

from wienerlinienservice import WienerLinienService


class WienerLinienPlugin(QQmlExtensionPlugin):

    def registerTypes(self, uri):
        qmlRegisterType(WienerLinienService, "WienerLinien", 1, 0, "WienerLinienService")
        #qmlRegisterType(WienerLinienModel, "WienerLinien", 1, 0, "WienerLinienModel")
        #qmlRegisterType(WienerLinienItem, "WienerLinien", 1, 0, "WienerLinienItem")
