import QtQuick 2.0
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.12

import HomeAssistant 1.0

Rectangle {
    id: toothbrushRectangle
    width: 400
    height: 170
    color: pressureDetected ? Material.color(Material.Red, Material.Shade900) : Material.color(Material.Grey, Material.Shade700);
    radius: 11
    border.color: pressureDetected ? Material.color(Material.Red, Material.Shade800) : Material.color(Material.Grey, Material.Shade600);
    border.width: 6

    visible: false

    property bool pressureDetected: false;

    Knob {
        id: knob
        x: 20
        y: 20
        width: 150
        height: 150
        anchors.leftMargin: 10
        anchors.topMargin: 10
        anchors.top: parent.top
        anchors.left: parent.left
    }

    ColumnLayout {
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.left: knob.right
        anchors.leftMargin: 10
        spacing: 0

        Label {
            id: timeLabel
            text: "1:24"
            Layout.fillHeight: true
            verticalAlignment: Text.AlignBottom
            font.pixelSize: 45
        }

        Label {
            id: modeLabel
            text: "mode"
            Layout.fillHeight: true
            verticalAlignment: Text.AlignTop
            font.pixelSize: 25
        }
    }


    property HomeAssistantStateListener listener: HomeAssistantStateListener {
        connection: homeAssistantService
        entityId: "sensor.lukas_toothbrush"

        onStateChanged: {
            console.log("toothbrush state: " + state)
            toothbrushRectangle.visible = (state != "unknown");

            if (attributes.brushMode === "daily_clean") {
                modeLabel.text = "Daily Clean";
            } else if (attributes.brushMode === "sensitive") {
                modeLabel.text = "Sensitive";
            } else if (attributes.brushMode === "massage") {
                modeLabel.text = "Massage";
            } else if (attributes.brushMode === "whitening") {
                modeLabel.text = "Whitening";
            } else if (attributes.brushMode === "deep_clean") {
                modeLabel.text = "Deep Clean";
            } else if (attributes.brushMode === "tongue_cleaning") {
                modeLabel.text = "Tongue Cleaning";
            } else if (attributes.brushMode === "turbo") {
                modeLabel.text = "Turbo";
            } else if (attributes.brushMode === "unknown") {
                modeLabel.text = "Unknown";
            } else {
                modeLabel.text = attributes.brushMode;
            }

            var min = Math.floor(attributes.brushTime / 60);
            var sec = Math.floor(attributes.brushTime % 60);

            timeLabel.text = String(min) + ":" + String(sec).padStart(2, '0');
            knob.update(attributes.brushTime / 120 * 100);
            toothbrushRectangle.pressureDetected = attributes.pressureDetected;
        }
    }


}
