import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3
import QtQuick.Extras 1.4

import "apps/homeassistant"

PopupWidget {
    width: 600
    height: 600

    contentItem: ColumnLayout {

        Layout.fillHeight: true
        Layout.fillWidth: true

        RowLayout {
            HomeAssistantButton {
                id: lukasLightButton
                image: "../icons/light-inverted.png"
                width: 30
                height: 30

            }
            HomeAssistantButton {
                id: middleLightButton
                image: "../icons/light-inverted.png"
                width: 30
                height: 30

            }
            HomeAssistantButton {
                id: sunnyLightButton
                image: "../icons/light-inverted.png"
                width: 30
                height: 30

            }
        }

        RowLayout {

            HomeAssistantButton {
                id: diningTableLightButton
                image: "../icons/light-inverted.png"

            }
            HomeAssistantButton {
                id: ceilingLightButton
                image: "../icons/light-inverted.png"

            }
        }

        RowLayout {
            HomeAssistantButton {
                id: kitchenLightButton
                image: "../icons/light-inverted.png"

            }
            HomeAssistantButton {
                id: kitchenSinkLightButton
                image: "../icons/light-inverted.png"

            }
        }
    }

}
