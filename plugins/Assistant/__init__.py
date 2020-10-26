from PySide2.QtQml import qmlRegisterType, QQmlExtensionPlugin
  
from .assistantservice import AssistantService

qmlRegisterType(AssistantService, "Assistant", 1, 0, "AssistantService")

