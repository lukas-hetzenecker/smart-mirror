import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3

Item {
    height: 135
    width: 300

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        RowLayout {
            spacing: 6

            Label  {
                id: timeStr
                text: qsTr("00:00")
                anchors.topMargin: 0
                font.pixelSize: 80
            }

            Label {
                id: secStr
                color: Material.color(Material.Grey, Material.Shade400)
                text: qsTr("30")
                topPadding: 11
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                font.pixelSize: 50
            }
        }

        Label {
            id: dateStr
            text: "Saturday, <b>29</b> April 2017"
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 20
            textFormat: Text.RichText
        }

    }

    Timer {
        interval: 500; running: true; repeat: true
        onTriggered: {
            timeStr.text = new Date().toLocaleTimeString(Qt.locale("en_UK"), "hh:mm")
            secStr.text = new Date().toLocaleTimeString(Qt.locale("en_UK"), "ss")
            dateStr.text = new Date().toLocaleDateString(Qt.locale("en_UK"), "dddd, <b>dd</b> MMMM yyyy")
        }
    }
}
