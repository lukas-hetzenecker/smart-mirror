import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3
import QtWebEngine 1.5
import QtQuick.VirtualKeyboard 2.2

import "../../"

PopupWidget {
    id: uberPopup

    contentItem: Column {
        spacing: 10

        WebEngineView {
                width: uberPopup.width - 2*parent.spacing - 2
                height: uberPopup.height - uberPopup.arrowHeight - uberInput.height - parent.spacing
                url: "https://m.uber.com/sign-up"
            }
        InputPanel {
            id: uberInput
            width: uberPopup.width - 2*parent.spacing - 2
            height: visible ? uberInput.implicitHeight : 0
            visible: Qt.inputMethod.visible
        }
    }
}
