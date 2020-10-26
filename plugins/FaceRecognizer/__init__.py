from PySide2.QtQml import qmlRegisterType, QQmlExtensionPlugin
  
from .facerecognizerservice import FaceRecognizerService, Face

qmlRegisterType(FaceRecognizerService, "FaceRecognizer", 1, 0, "FaceRecognizerService")

