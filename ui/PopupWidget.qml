import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3

import QtQuick.Templates 2.3 as T

Popup {
    id: popup

    property Item target: parent
    property int arrowHeight: 20
    property int arrowWidth: 30

    //width: contentItem.height
    y: target.y - height - arrowHeight
    x: -parent.x

    modal: true
    focus: true
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    T.Overlay.modal: Rectangle {
        color: "#000000"
        Behavior on opacity {
            NumberAnimation {
                duration: 200
                to: 0.45
            }
        }
    }

    Component.onCompleted: {
        console.log("target.x: " + target.x);
        console.log("target.width: " + target.width);

    }

    background: Item {
        Rectangle {
            id: rect
            y: 0
            x: 0
            radius: 7
            height: popup.height
            width: popup.width
            color: Material.color(Material.Grey, Material.Shade600)
        }

        Triangle {
            x: target.width/2 - arrowWidth/2 - popup.x
            y: rect.height

            width: arrowWidth
            height: arrowHeight

        }
    }

}
