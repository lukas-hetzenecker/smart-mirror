#!./bin/python
import ctypes
from collections import OrderedDict


import sys
import os
import asyncio
import yaml
import logging.config
os.environ["QML2_IMPORT_PATH"] = "plugins"
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"

#from quamash import QEventLoop, QThreadExecutor
from asyncqt import QEventLoop
#from qasync import QEventLoop

from PySide2.QtGui import QGuiApplication, QTouchDevice, QCursor
from PySide2.QtCore import QCoreApplication, QObject, QUrl, Qt
from PySide2.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine, QQmlApplicationEngine
#from PySide2.QtWidgets import QApplication
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

import tracemalloc
import linecache
tracemalloc.start(25)
async def show_memory():
    key_type='lineno'
    limit=10
    snapshot = tracemalloc.take_snapshot()

    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    logger.info("------- Trace --------")
    logger.info("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        logger.info("#%s: %s:%s: %.1f KiB"
                      % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            logger.info('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        logger.info("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    logger.info("Total allocated size: %.1f KiB" % (total / 1024))
    logger.info("-------- End ---------")
    
    await asyncio.sleep(30)
    asyncio.Task(show_memory())

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
    print("touchscreens detected, disabling mouse:", touchscreens)
    app.setOverrideCursor(QCursor(Qt.BlankCursor))



# Create a QML engine.
engine = QQmlApplicationEngine()
engine.load('./ui/main.qml')

win = engine.rootObjects()[0]
win.show() 

#asyncio.Task(show_memory())

with loop: ## context manager calls .close() when loop completes, and releases all resources
    sys.exit(loop.run_forever())

#async def process_events(qapp):
#     while True:
#        await asyncio.sleep(0.01)
#        qapp.processEvents()

#loop = asyncio.get_event_loop()
#loop.run_until_complete(process_events(app))
