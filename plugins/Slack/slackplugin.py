from PyQt5.QtQml import qmlRegisterType, QQmlExtensionPlugin

from slackservice import SlackService


class HomeAssistantPlugin(QQmlExtensionPlugin):

    def registerTypes(self, uri):
        qmlRegisterType(SlackService, "Slack", 1, 0, "SlackService")
