import QtQuick 2.7

Item {
    property string name: "Unknown"

    Rectangle {
        id: rectangle
        color: "#00000000"
        radius: 5
        anchors.fill: parent
        border.width: 5
        border.color: "#eb3333"
    }

    Text {
        id: text1
        color: "#eb3333"
        text: name
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.top
        anchors.bottomMargin: 0
        font.pixelSize: 12
    }

}
