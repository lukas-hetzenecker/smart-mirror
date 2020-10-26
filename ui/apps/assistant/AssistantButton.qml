import QtQuick 2.0

import Assistant 1.0

import "../../"

AppButton {
    id: assistantButton
    image: "../icons/voice-microphone-intreface-symbol-inverted.png"

    onReleased: {
        assistantService.startConversation()
        assistantWidget.open()
    }

    Component.onCompleted: {
        assistantService.conversationTurnStarted.connect(function() {
            assistantWidget.open();
        });
    }


    AssistantWidget {
        id: assistantWidget
        target: assistantButton

        x: 0

        onAboutToShow: {
            assistantButton.highlighted = true;
        }

        onClosed:  {
            assistantButton.highlighted = false;
            assistantService.stopConversation()
        }
    }

    AssistantService {
        id: assistantService
        credentials: "config/credentials.json"
        deviceModelId: secret.assistantDeviceModelId
        Component.onCompleted: {
            this.start()
        }
    }

    Connections {
        target: mainWindow
        function onMirrorActiveChanged() {
            if (mainWindow.mirrorActive) {
                assistantService.start()
            } else {
                assistantService.stop()
            }
        }
    }

}
