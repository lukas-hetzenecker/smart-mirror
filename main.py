#!./bin/python
from collections import OrderedDict

import sys
import os
import asyncio
import yaml
import logging.config
os.environ["QML2_IMPORT_PATH"] = "plugins"
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"

from asyncqt import QEventLoop

from PySide2.QtGui import QGuiApplication, QTouchDevice, QCursor
from PySide2.QtCore import QCoreApplication, QObject, QUrl, Qt
from PySide2.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine, QQmlApplicationEngine
from PySide2.QtPositioning import *

import plugins.HomeAssistant
import plugins.WienerLinien
import plugins.Weather
import plugins.Assistant
import plugins.Serial
import plugins.Slack
import plugins.Mqtt
import plugins.Performance

logging.config.dictConfig(yaml.load(open('logging.yaml', 'r')))
logger = logging.getLogger(__name__)

logger.debug("Geo sources: %s" % QGeoPositionInfoSource.availableSources())

QGuiApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
QGuiApplication.setAttribute(Qt.AA_Use96Dpi)
QGuiApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Create the application instance.
app = QGuiApplication(sys.argv)

loop = QEventLoop(app)
asyncio.set_event_loop(loop)

touchscreens = list(filter(lambda d: d.type() == QTouchDevice.TouchScreen, QTouchDevice.devices()))
if touchscreens:
    logger.info("touchscreens detected, disabling mouse %s" % touchscreens)
    app.setOverrideCursor(QCursor(Qt.BlankCursor))

# Create a QML engine.
engine = QQmlApplicationEngine()
engine.load('./ui/main.qml')

win = engine.rootObjects()[0]
win.show() 

with loop: ## context manager calls .close() when loop completes, and releases all resources
    sys.exit(loop.run_forever())

