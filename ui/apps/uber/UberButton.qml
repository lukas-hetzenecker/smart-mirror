import QtQuick 2.0
import "../../"

AppButton {
    id: uberButton
    image: "../icons/apps/uber.svg"

    onReleased: uberWidget.open()

    UberWidget {
        id: uberWidget
        target: uberButton

        height: 1000
        width: 800

        onAboutToShow: {
            uberButton.highlighted = true;
            mainWindow.overrideInputpanel = true;
        }

        onClosed:  {
            uberButton.highlighted = false;
            mainWindow.overrideInputpanel = false;
        }

    }
}
