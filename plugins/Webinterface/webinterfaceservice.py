import io
import logging
import asyncio

import numpy as np
import websockets
import json
import ssl
import collections
import multiprocessing

from PIL import Image
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QThread
from PyQt5.QtMultimedia import QAbstractVideoBuffer
from PyQt5.QtMultimedia import QVideoFrame
from PyQt5.QtMultimedia import QVideoProbe
from aioprocessing import AioJoinableQueue, AioQueue, AioEvent
from quart import Quart
from quart import Response
from quart.serving import Server
from quart.views import View, MethodView

logger = logging.getLogger(__name__)


class WebinterfaceService(QObject):
    cameraChanged = pyqtSignal(QObject)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._camera = None

        self._converter = None
        self._latestImage = None

        self.app = Quart(__name__)
        self.app.add_url_rule('/camera.mjpeg', 'camerastream', self.getCameraStream)

        loop = asyncio.get_event_loop()
        create_server = loop.create_server(
            lambda: Server(self.app, loop, logger, "%(h)s %(r)s %(s)s %(b)s %(D)s", 5),
            '0.0.0.0', '9000', ssl=None,
        )
        server = loop.create_task(create_server)

    @pyqtProperty(QObject, notify=cameraChanged)
    def camera(self):
        return self._hostname

    @camera.setter
    def camera(self, camera):
        self._camera = camera
        print("camera is now", self._camera)
        print("dir", dir(self._camera))
        print("media", self._camera.property("mediaObject"))

        self.cameraChanged.emit(self._camera)

        self.start()

    def start(self):
        self._tasks = AioJoinableQueue(maxsize=1)
        self._results = AioQueue()
        self._exit = AioEvent()

        self._converter = ConverterWorker(self._tasks, self._results, self._exit)
        self._converter.start()

        camera = self._camera.property("mediaObject")

        self._probe = QVideoProbe(self)
        self._probe.setSource(camera)
        self._probe.videoFrameProbed.connect(self.handleFrame)

    def handleFrame(self, frame):
        if not self._tasks.full():
            asyncio.ensure_future(self._handleFrame(frame))

    async def _handleFrame(self, frame):
        frame.map(QAbstractVideoBuffer.ReadOnly)

        ptr = frame.bits()
        ptr.setsize(frame.mappedBytes())

        assert frame.pixelFormat() == QVideoFrame.Format_YUV420P

        w = frame.width()
        h = frame.height()

        w2 = w // 2
        h2 = h // 2

        s = w * h
        s2 = w2 * h2

        y = np.frombuffer(ptr, dtype=np.ubyte, count=s, offset=0)
        u = np.frombuffer(ptr, dtype=np.ubyte, count=s2, offset=s)
        v = np.frombuffer(ptr, dtype=np.ubyte, count=s2, offset=s + s2)

        frame.unmap()

        await self._tasks.coro_put((y, u, v, h, w, h2, w2))

        self._latestImage = await self._results.coro_get()


    async def getCameraStream(self):
        async def camera_generator():
            while True:
                if self._latestImage:
                    yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + self._latestImage + b'\r\n')
                await asyncio.sleep(0.1)

        return Response(camera_generator(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


class ConverterWorker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, exit_event):
        multiprocessing.Process.__init__(self)

        self.task_queue = task_queue
        self.result_queue = result_queue
        self.exit_event = exit_event

    def run(self):
        while not self.exit_event.is_set():
            y, u, v, h, w, h2, w2 = self.task_queue.get()

            y = y.reshape((h, w))
            u = u.reshape((h2, w2)).repeat(2, axis=0).repeat(2, axis=1)
            v = v.reshape((h2, w2)).repeat(2, axis=0).repeat(2, axis=1)

            yuv_img = np.dstack((y, u, v))[:h, :w, :].astype(np.uint8)

            img = Image.fromarray(yuv_img, 'YCbCr')

            imgByteArr = io.BytesIO()
            img.save(imgByteArr, format='JPEG')

            self.task_queue.task_done()
            self.result_queue.put(imgByteArr.getvalue())
