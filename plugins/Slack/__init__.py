from PySide2.QtQml import qmlRegisterType, QQmlExtensionPlugin
  
from .slackservice import SlackService

qmlRegisterType(SlackService, "Slack", 1, 0, "SlackService")

