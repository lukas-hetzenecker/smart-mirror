import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3
import QtWebEngine 1.5
import QtQuick.VirtualKeyboard 2.2

Rectangle {
    property variant modelData: model

    width: parent.width
    height: 60
    color: ListView.isCurrentItem ? Material.color(Material.Purple, Material.Shade400) : Material.color(Material.Grey, Material.Shade600)
    radius: 5

    Row {
        id: row
        height: parent.height
        spacing: 4

        Label {
            text: "#"
            leftPadding: 10
            anchors.verticalCenter: parent.verticalCenter
            color: Material.color(Material.Grey, Material.Shade400)
            font.pixelSize: 25
        }

        Label {
            text: name
            anchors.verticalCenter: parent.verticalCenter
            Layout.fillWidth: true
            font.pixelSize: 25
        }

    }


    MouseArea {
        anchors.fill: parent
        onClicked: channelList.currentIndex = index
    }

}
