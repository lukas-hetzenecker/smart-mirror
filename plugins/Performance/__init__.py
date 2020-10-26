from PySide2.QtQml import qmlRegisterType, QQmlExtensionPlugin
  
from .performanceservice import PerformanceService

qmlRegisterType(PerformanceService, "Performance", 1, 0, "PerformanceService")

