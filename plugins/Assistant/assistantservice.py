import logging
import json

import google.oauth2.credentials
import time
from google.assistant.library import Assistant

from PySide2.QtCore import Property, Signal, Slot, QObject, QThread
from google.assistant.library.event import EventType

logger = logging.getLogger(__name__)


class AssistantService(QObject):
    credentialsChanged = Signal(str)
    deviceModelIdChanged = Signal(str)
    conversationTurnStarted = Signal()
    conversationTurnFinished = Signal()
    endOfUtterance = Signal()
    recognizingSpeechFinished = Signal(str)
    renderResponse = Signal(str, int)
    respondingFinished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._deviceModelId = ""
        self._credentialFile = ""
        self._assistantThread = None

    def getCredentials(self):
        return self._credentialFile

    def setCredentials(self, credentialFile):
        self._credentialFile = credentialFile
        self.credentialsChanged.emit(self._credentialFile)

    credentials = Property(str, getCredentials, setCredentials, notify=credentialsChanged)

    def getDeviceModelId(self):
        return self._deviceModelId

    def setDeviceModelId(self, deviceModelId):
        self._deviceModelId = deviceModelId
        self.deviceModelIdChanged.emit(self._deviceModelId)

    deviceModelId = Property(str, getDeviceModelId, setDeviceModelId, notify=deviceModelIdChanged)

    @Slot()
    def start(self):
        if self._assistantThread is not None:
            return

        def processEvent(event):
            logger.debug("got event %s", event)
            if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
                self.conversationTurnStarted.emit()
            elif event.type == EventType.ON_END_OF_UTTERANCE:
                self.endOfUtterance.emit()
            elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
                text = event.args['text']
                self.recognizingSpeechFinished.emit(text)
            elif event.type == EventType.ON_RENDER_RESPONSE:
                text = event.args['text']
                type_ = event.args['type']
                self.renderResponse.emit(text, type_)
            elif event.type == EventType.ON_RESPONDING_FINISHED:
                self.respondingFinished.emit()
            elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
                self.conversationTurnFinished.emit()

        self._assistantThread = AssistantThread(self._credentialFile, self._deviceModelId)
        self._assistantThread.receivedEvent.connect(processEvent)
        self._assistantThread.start()

    @Slot()
    def stop(self):
        if self._assistantThread is not None:
            self._assistantThread.quit()
            self._assistantThread = None

    @Slot()
    def startConversation(self):
        if self._assistantThread is not None:
            self._assistantThread.startConversation()

    @Slot()
    def stopConversation(self):
        if self._assistantThread is not None:
            self._assistantThread.stopConversation()


class AssistantThread(QThread):
    receivedEvent = Signal(object)

    def __init__(self, credentialFile, deviceModelId, parent=None):
        super().__init__(parent)

        with open(credentialFile, 'r') as f:
            self._credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            self._deviceModelId = deviceModelId
        self._assistant = None

    def run(self):
        logger.debug("Starting assistant...")

        try:
            with Assistant(self._credentials, self._deviceModelId) as self._assistant:
                for event in self._assistant.start():
                    self.receivedEvent.emit(event)
        except Exception as e:
            logger.error(e)
            time.sleep(10)
            self.run()

    @Slot()
    def startConversation(self):
        self._assistant.start_conversation()

    @Slot()
    def stopConversation(self):
        self._assistant.stop_conversation()
