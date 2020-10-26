from PyQt5.QtQml import qmlRegisterType, QQmlExtensionPlugin

from facerecognizerservice import FaceRecognizerService, Face


class FaceRecognizerPlugin(QQmlExtensionPlugin):

    def registerTypes(self, uri):
        qmlRegisterType(FaceRecognizerService, "FaceRecognizer", 1, 0, "FaceRecognizerService")
