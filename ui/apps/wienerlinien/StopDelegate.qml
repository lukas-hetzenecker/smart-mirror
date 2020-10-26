import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3

Item {
    height: 40
    Row {
        id: row
        height: 30
        spacing: 10

        Rectangle {
            width: 40
            color: Material.color(Material.Red, Material.Shade900)
            radius: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            anchors.top: parent.top
            anchors.topMargin: 0

            Label {
                text: line
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 20
            }
        }

        Label {
            text: direction
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            anchors.top: parent.top
            anchors.topMargin: 0
            font.pixelSize: 20
            width: 200
            verticalAlignment: Text.AlignVCenter

        }

        Row {
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            anchors.top: parent.top
            anchors.topMargin: 0
            spacing: 12

            Repeater {
                //model: departures.count
                model: departures.length

                Label {
                    //text: departures.get(index).time
                    text: departures[index]
                    font.bold: true
                    font.pixelSize: 25
                    verticalAlignment: Text.AlignVCenter
                    anchors.verticalCenter: parent.verticalCenter

                }
            }
        }

    }

}

