import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3
import QtWebEngine 1.5
import QtQuick.VirtualKeyboard 2.2
import QtQml.Models 2.2
import QtGraphicalEffects 1.0


import "apps/assistant"
import "apps/uber"
import "apps/debug"
import "apps/homeassistant"
import "apps/slack"
//import "apps/camera"

Item {
    id: item1
    height: 1120

    anchors.right: parent.right
    anchors.bottom: parent.bottom
    anchors.left: parent.left

    ListView {
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.right: parent.right
        anchors.left: parent.left
        snapMode: ListView.SnapToItem

        height: 120

        spacing: 15
        model: itemModel
        orientation: ListView.Horizontal
    }

    ObjectModel {
        id: itemModel

        AssistantButton {

        }

        HomeAssistantButton {
            id: bellButton
            connection: homeAssistantService
            entityId: 'switch.door_buzzer_switch'
            image: "../icons/bell-alarm-symbol-inverted.png"
            highlighted: state === 'on'

            onPressed: {
                console.log('pressed!')
                homeAssistantService.callService('homeassistant', 'turn_on', {'entity_id': 'script.door_buzzer'})
            }
        }

        HomeAssistantButton {
            LightsWidget {
                id: lightsWidget
                target: lightsButton

                x: 0

                onAboutToShow: {
                    lightsButton.highlighted = true;
                }

                onClosed:  {
                    lightsButton.highlighted = false;
                }
            }

            id: lightsButton
            connection: homeAssistantService
            entityId: 'group.lights'
            image: state == "on" ? "../icons/light-inverted.png" : "../icons/light-out-inverted.png"
            onPressed: {
                homeAssistantService.callService('homeassistant', 'turn_off', {'entity_id': 'group.lights'})
            }

            onPressAndHold: {
                lightsWidget.open()
            }

        }

        HomeAssistantButton {
            id: powerButton

            connection: homeAssistantService
            entityId: 'sensor.smart_meter_power'

            property int power: parseInt(state)

            contentItem: Label {
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 20
                text: powerButton.power + "W"
            }
        }

        UberButton {

        }

        AppButton {
            id: spotifyButton
            image: "../icons/apps/spotify.svg"
        }


        SlackButton {
            connection: slackService
        }

        DebugButton {
        }

        /* CameraButton {
            camera: cameraService
        } */

    }

}
