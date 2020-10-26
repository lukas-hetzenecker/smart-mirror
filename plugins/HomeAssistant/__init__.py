from PySide2.QtQml import qmlRegisterType, QQmlExtensionPlugin

from .homeassistantservice import HomeAssistantService, HomeAssistantStateListener

qmlRegisterType(HomeAssistantService, "HomeAssistant", 1, 0, "HomeAssistantService")
qmlRegisterType(HomeAssistantStateListener, "HomeAssistant", 1, 0, "HomeAssistantStateListener")

