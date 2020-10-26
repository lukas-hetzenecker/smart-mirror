import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3
import QtQuick.VirtualKeyboard 2.2

RowLayout {
    width: 750

    Rectangle {
        id: rectangle
        width: 200
        height: 1
        color: Material.color(Material.Grey, Material.Shade400)
        Layout.fillWidth: true
    }

    Label {
        width: 750
        text: Qt.formatDate(section, Qt.DefaultLocaleLongDate)
        font.pointSize: 20
        font.bold: true
        color: Material.color(Material.Grey, Material.Shade400)
        horizontalAlignment: Text.AlignHCenter
    }

    Rectangle {
        id: rectangle1
        width: 200
        height: 1
        color: Material.color(Material.Grey, Material.Shade400)
        Layout.fillWidth: true
    }

}
