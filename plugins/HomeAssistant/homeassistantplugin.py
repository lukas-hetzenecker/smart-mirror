from PyQt5.QtQml import qmlRegisterType, QQmlExtensionPlugin

from homeassistantservice import HomeAssistantService, HomeAssistantStateListener


class HomeAssistantPlugin(QQmlExtensionPlugin):

    def registerTypes(self, uri):
        qmlRegisterType(HomeAssistantService, "HomeAssistant", 1, 0, "HomeAssistantService")
        qmlRegisterType(HomeAssistantStateListener, "HomeAssistant", 1, 0, "HomeAssistantStateListener")
