import logging
import re
import threading
from concurrent.futures import ProcessPoolExecutor
from glob import glob

import dlib
import multiprocessing

import pickle
import os
import numpy as np
import scipy
from PySide2.QtCore import QPoint
from PySide2.QtCore import QRect
from PySide2.QtCore import Qt, QMetaObject, Q_ARG, Q_RETURN_ARG
import asyncio

from PySide2.QtCore import QRunnable
from PySide2.QtCore import QThreadPool
from PySide2.QtCore import Property, Signal, Slot, QObject, QThread
from PySide2.QtGui import QImage
from PySide2.QtMultimedia import QAbstractVideoBuffer
from PySide2.QtMultimedia import QAbstractVideoFilter
from PySide2.QtMultimedia import QCamera
from PySide2.QtMultimedia import QCameraImageCapture
from PySide2.QtMultimedia import QVideoFilterRunnable
from PySide2.QtMultimedia import QVideoFrame
from PySide2.QtMultimedia import QVideoProbe
from PySide2.QtQml import QQmlListProperty
from aioprocessing import AioQueue, AioProcess, AioJoinableQueue, AioEvent
from scipy import ndimage

import skimage.color
import cv2

from contexttimer import Timer

logger = logging.getLogger(__name__)

FACES_DIR = '/home/lukas/faces'


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]


class Face(QObject):
    def __init__(self, data):
        self._rect = data[0]
        self._name = data[1]

    @pyqtProperty(QRect)
    def rectangle(self):
        return self._rect

    @pyqtProperty(str)
    def name(self):
        return self._name


class FaceRecognizerService(QObject):
    cameraChanged = pyqtSignal(QObject)
    facesDetected = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._camera = None
        self._busy = False

        self._recognizer = None
        self._probe = None
        self._faces = []
        self._running = False

    @pyqtProperty(QObject, notify=cameraChanged)
    def camera(self):
        return self._hostname

    @camera.setter
    def camera(self, camera):
        self._camera = camera
        print("camera is now", self._camera)
        print("dir", dir(self._camera))
        print("media", self._camera.property("mediaObject"))

        camera = self._camera.property("mediaObject")

        self._probe = QVideoProbe(self)
        self._probe.setSource(camera)

        self.cameraChanged.emit(self._camera)


    @pyqtSlot()
    def start(self):
        if self._running:
            return

        if self._camera is None:
            print("error!! no camera!!")
            return

        print("FACERECOGNIZER start")

        self._tasks = AioJoinableQueue(maxsize=1)
        self._results = AioQueue()
        self._exit = AioEvent()
        self._recognizer = FaceRecognizerWorker(self._tasks, self._results, self._exit)
        self._recognizer.start()

        self._probe.videoFrameProbed.connect(self.handleFrame)

        self._running = True

    @pyqtSlot()
    def stop(self):
        if not self._running:
            return

        self._exit.set()

        self._probe.videoFrameProbed.disconnect()

        self._running = False

        self.stopped.emit()

    @pyqtSlot(str, result=str)
    def folderForPerson(self, person):
        path = os.path.join(FACES_DIR, person)
        os.makedirs(path, exist_ok=True)

        files = glob(os.path.join(path, 'IMG_*.jpg'))
        files = sorted(files, key=natural_keys)

        if len(files) > 0:
            cur_num = int(os.path.basename(files[-1])[7:-4])
            cur_num += 1
        else:
            cur_num = 1

        path = os.path.join(path, 'IMG_%04i.jpg' % cur_num)
        print("PATH", path)

        return path

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

        result = await self._results.coro_get()
        print("result", result)

        self._faces = [f for f in result]
        #result = QQmlListProperty(Face, self, result)

        self.facesDetected.emit()

    @pyqtProperty(list)
    def faces(self):
        return self._faces

class FaceRecognizerWorker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, exit_event):
        multiprocessing.Process.__init__(self)

        self.task_queue = task_queue
        self.result_queue = result_queue
        self.exit_event = exit_event

    def run(self):
        import face_recognition

        #detector = dlib.get_frontal_face_detector()

        known_faces = {}

        persons = [o for o in os.listdir(FACES_DIR)
                    if os.path.isdir(os.path.join(FACES_DIR,o))]
        for person in persons:
            images = os.listdir(os.path.join(FACES_DIR, person))
            known_faces[person] = list()
            for image in images:
                if not image.endswith(".jpg"):
                    continue

                image_path = os.path.join(FACES_DIR, person, image)
                cache_path = image_path + '.c'

                #print("IMAGE for", person, ": ", image)

                if os.path.isfile(cache_path):
                    face_encodings = pickle.load(open(cache_path, "rb"))
                else:
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)
                    pickle.dump(face_encodings, open(cache_path, "wb"))
                #print("FACES", face_encodings)
                known_faces[person].append(face_encodings[0])

        while not self.exit_event.is_set():
            y, u, v, h, w, h2, w2 = self.task_queue.get()

            y = y.reshape((h, w))
            u = u.reshape((h2, w2)).repeat(2, axis=0).repeat(2, axis=1)
            v = v.reshape((h2, w2)).repeat(2, axis=0).repeat(2, axis=1)

            yuv_img = np.dstack((y, u, v))[:h, :w, :].astype(np.float)

            rgb_img = convertYUVtoRGB(yuv_img)

            #print("has detector...")

            #dets = detector(rgb_img, 1)
            face_locations = face_recognition.face_locations(rgb_img, number_of_times_to_upsample=1, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

            #print("has detected...")
            #print("dets", face_locations)

            rects = []
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                #print("Left: {} Top: {} Right: {} Bottom: {}".format(
                #    left, top, right, bottom))

                min_value = 1
                min_person = "Unknown"
                for person, pictures in known_faces.items():
                    distances = face_recognition.face_distance(pictures, face_encoding)
                    #print("FACE distance for ", person, distances)
                    if min(distances) < min_value and min(distances) < 0.6:
                        min_value = any(distances)
                        min_person = person

                rects.append([QRect(QPoint(left, top), QPoint(right, bottom)), min_person])

            self.task_queue.task_done()
            self.result_queue.put(rects)


def convertYUVtoRGB(yuv):
    # according to ITU-R BT.709
    yuv[:,:, 0] = yuv[:,:, 0].clip(16, 235).astype(yuv.dtype) - 16
    yuv[:,:,1:] = yuv[:,:,1:].clip(16, 240).astype(yuv.dtype) - 128

    A = np.array([[1.164, 0.000,  1.793],
                 [1.164,  -0.213, -0.533],
                 [1.164,  2.112,  0.000]])
    # our result
    rgb = np.dot(yuv, A.T).clip(0, 255).astype('uint8')
    return rgb
