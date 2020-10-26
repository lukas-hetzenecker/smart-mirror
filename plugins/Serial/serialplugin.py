from PyQt5.QtQml import qmlRegisterType, QQmlExtensionPlugin

from serialservice import SerialService


class SerialPlugin(QQmlExtensionPlugin):

    def registerTypes(self, uri):
        qmlRegisterType(SerialService, "Serial", 1, 0, "SerialService")

