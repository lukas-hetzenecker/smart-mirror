import QtQuick 2.0

import HomeAssistant 1.0

import "../../"

AppButton {
    id: homeassistantButton
    property HomeAssistantService connection
    property string entityId
    property string state: listener.state

    property HomeAssistantStateListener listener: HomeAssistantStateListener {
        connection: homeAssistantService
        entityId: homeassistantButton.entityId
    }

}
