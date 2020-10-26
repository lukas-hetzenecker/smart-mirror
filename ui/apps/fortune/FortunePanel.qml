import QtQuick 2.0
import QtQuick.Controls 2.1

import "fortunes.js" as Fortunes

Label {
    property string fortune

    id: fortuneLabel
    text: fortune
    anchors.top: parent.top
    anchors.topMargin: 500
    anchors.horizontalCenter: parent.horizontalCenter
    font.pixelSize: 25

    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignTop
    height: 150
    width: parent.width

    Component.onCompleted: {
        next()
    }

    MouseArea {
        anchors.fill: parent;

        onPressed: {
            next()
        }
    }

    function next() {
        fortuneLabel.fortune = Fortunes.next()
    }
}

