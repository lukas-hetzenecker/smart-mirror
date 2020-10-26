import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3
import QtQuick.VirtualKeyboard 2.2

ColumnLayout {
    id: column
    width: 750

    RowLayout {
        spacing: 10
        Label {
            id: userLabel
            text: user
            font.bold: true
            font.pointSize: 18
        }

        Label {
            id: timeLabel
            text: Qt.formatTime(time)
            font.pointSize: 16
            color: Material.color(Material.Grey, Material.Shade400)
            horizontalAlignment: Text.AlignLeft
        }
    }
    Label {
        id: textLabel
        text: model.text
        Layout.maximumWidth: 750
        bottomPadding: 10
        font.pointSize: 18
        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
    }
}
