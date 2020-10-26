import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3
import QtQuick.VirtualKeyboard 2.2

import "../../"

PopupWidget {
    id: slackPopup
    height: 1000
    width: 1100

    contentItem: ColumnLayout {
        RowLayout {
            Layout.fillHeight: true
            spacing: 15

            ListView {
                id: channelList
                width: 200
                Layout.fillHeight: true
                focus: true
                clip: true

                model: slackButton.connection.channels

                Connections {
                    target: channelList.model
                    function onRowsInserted() {
                        console.log("row inserted!")
                    }
                }

                delegate: SlackChannelDelegate { }
                onCurrentItemChanged: {
                    console.log(channelList.currentIndex + ' selected')
                    messagesList.model = channelList.currentItem.modelData.messageModel
                    messagesList.positionViewAtEnd()
                }
            }

            ColumnLayout {
                Layout.fillWidth: true

                ListView {
                    id: messagesList
                    clip: true
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    section.property: "date"
                    section.criteria: ViewSection.FullString
                    section.delegate: SlackMessageSectionDelegate {}

                    delegate: SlackMessageDelegate {}
                }

                TextField {
                    Layout.fillWidth: true
                    height: 40
                    focus: false
                    font.pointSize: 20
                }
            }
        }

        InputPanel {
            id: inputPanel
            Layout.fillWidth: true
            visible: Qt.inputMethod.visible
        }
    }
}
