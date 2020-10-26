import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3

import WienerLinien 1.0

Item {
    // get the RBLs from https://till.mabe.at/rbl/
    property var rbls;
    property string key;

    id: wienerLinienPanel

    /*
    ListModel {
        id: transportationModel
        ListElement { stop: "Fendigasse"; line: "14A"; direction: "Neubaugasse"; departures: [ ListElement { time: 1 }, ListElement { time: 7 } ] }
        ListElement { stop: "Reinprechtsdf. Str./Arbeiterg."; line: "59A"; direction: "Kärntner Ring"; departures: [ ListElement { time: 2 }, ListElement { time: 9 } ] }
        ListElement { stop: "Reinprechtsdf. Str./Arbeiterg."; line: "59A"; direction: "Bahnhof Meidling"; departures: [ ListElement { time: 3 }, ListElement { time: 5 } ] }
    }
    */

    // The delegate for each section header
    Component {
        id: sectionHeading

        Label {
            width: 200
            height: 50
            text: section
            topPadding: 10
            font.pixelSize: 25
            color: Material.color(Material.Red, Material.Shade100)
        }
    }

    ListView {
        id: view
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: parent.width
        interactive: false
        // model: transportationModel
        model: wienerLinienService.model

        delegate: StopDelegate { }

        section.property: "stop"
        section.criteria: ViewSection.FullString
        section.delegate: sectionHeading
    }

    WienerLinienService {
        id: wienerLinienService
        rbls: wienerLinienPanel.rbls
        key: wienerLinienPanel.key
    }

}
