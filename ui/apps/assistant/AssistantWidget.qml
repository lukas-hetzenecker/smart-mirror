import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3
//import QtGraphicalEffects 1.0

import "../../"

PopupWidget {
    id: debugPopup

    width: 50 + rectangle.width + rowLayout.spacing + Math.max(100, label.implicitWidth)
    height: 130
    padding: 20

    // we have to re-emit al signals with named parameters, because of https://bugreports.qt.io/browse/PYSIDE-634 :-(
    // see also: https://stackoverflow.com/questions/10506398/pyside-signal-argument-cant-be-retrieved-from-qml

    signal recognizingSpeechFinished(string text)
    signal renderResponse(string response, int type)

    Component.onCompleted: {
        assistantService.recognizingSpeechFinished.connect(debugPopup.recognizingSpeechFinished);
        assistantService.renderResponse.connect(debugPopup.renderResponse);
    }

    Timer {
        id: closeTimer
        interval: 2000;
        running: false;
        onTriggered: {
            debugPopup.close()
        }
    }


    Connections {
        target: assistantService

        function onEndOfUtterance() {
            colorAnimation.stop();
            rectangle.color = Material.color(Material.Grey, Material.Shade800);
        }

        function onConversationTurnStarted() {
            closeTimer.stop();

            label.font.italic = true;
            label.text = "Listening..."
            colorAnimation.start();
        }

        function onConversationTurnFinished() {
            closeTimer.restart();
        }
    }

    onRecognizingSpeechFinished: {
        label.font.italic = false;
        label.text = "\"" + text + "\"";
    }

    RowLayout {
        id: rowLayout
        spacing: 30
        anchors.fill: parent

        Rectangle {
            id: rectangle
            width: 90
            height: 90

            radius: width*0.5

            SequentialAnimation on color {
                id: colorAnimation
                loops: Animation.Infinite

                ColorAnimation { to: Material.color(Material.Red, Material.Shade200); duration: 600 }
                ColorAnimation { to: Material.color(Material.Red, Material.Shade500); duration: 600 }
            }

            Image {
                id: image
                width: 70
                height: 70
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                sourceSize.height: 70
                sourceSize.width: 70
                mipmap: true
                source: "../../../icons/voice-microphone-intreface-symbol-inverted.png"
            }
        }

        Label {
            id: label
            height: 90
            font.pointSize: 20
            Layout.fillWidth: true
        }
    }

}
