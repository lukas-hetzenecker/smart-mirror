import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3

import "../../"

PopupWidget {
    id: debugPopup
    width: 1100

    contentItem: Row {
        spacing: 10

        Button {
            height: 120
            width: 120
            text: "OFF"

            onReleased: serialService.turnDisplayOff()
        }

        Button {
            height: 120
            width: 120
            text: "Power"

            onReleased: serialService.pressPowerButton()
        }

        Button {
            height: 120
            width: 120
            text: "Volume +"

            onReleased: serialService.pressVolumeUpButton()
        }

        Button {
            height: 120
            width: 120
            text: "Volume -"

            onReleased: serialService.pressVolumeDownButton()
        }

        Button {
            height: 120
            width: 120
            text: "Auto"

            onReleased: serialService.pressAutoButton()
        }

        Button {
            height: 120
            width: 120
            text: "Menu"

            onReleased: serialService.pressMenuButton()
        }

        Button {
            height: 120
            width: 120
            text: "Exit"

            onReleased: serialService.pressExitButton()
        }
    }

}
