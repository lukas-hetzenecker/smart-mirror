import QtQuick 2.0

import Serial 1.0

import "../../"

AppButton {
    id: debugButton
    image: "../icons/wrench-outlined-tool-inverted.png"

    onReleased: debugWidget.open()


    DebugWidget {
        id: debugWidget
        target: debugButton

        onAboutToShow: {
            debugButton.highlighted = true;
        }

        onClosed:  {
            debugButton.highlighted = false;
        }
    }
}
