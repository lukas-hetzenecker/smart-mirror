import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
//import QtCharts 2.2
import QtQuick.Layouts 1.3
import Weather 1.0

ColumnLayout {
    id: column
    property string city
    property string key

    WeatherService {
        id: weatherService
        city: column.city
        key: column.key

        Component.onCompleted: {
            console.log("Temperature is: " + weatherService.temperature);
        }
    }

    RowLayout {
        id: row
        spacing: 20

        WeatherCanvas {
            id: canvas
            width: temperatureColumn.height
            height: temperatureColumn.height
        }

        ColumnLayout {
            id: temperatureColumn
            spacing: 0

            RowLayout  {
                id: temperatureRow
                Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                Label {
                    id: temperatureStr
                    text: weatherService.temperature
                    bottomPadding: -10
                    Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                    //color: textColor
                    font.pixelSize: 80
                }

                Label {
                    id: text1
                    color: Material.color(Material.Grey, Material.Shade400)
                    text: qsTr("°C")
                    Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                    font.pixelSize: 60
                }
            }

            RowLayout  {
                Layout.alignment: Qt.AlignRight | Qt.AlignTop
                Label {
                    text: "feels like "
                    horizontalAlignment: Text.AlignRight
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignRight | Qt.AlignCenter
                    font.pixelSize: 20
                }

                Label {
                    text: weatherService.apparentTemperature
                    horizontalAlignment: Text.AlignRight
                    Layout.alignment: Qt.AlignRight | Qt.AlignCenter
                    font.pixelSize: 25
                }

                Label {
                    color: Material.color(Material.Grey, Material.Shade400)
                    text: qsTr("°C")
                    horizontalAlignment: Text.AlignRight
                    Layout.alignment: Qt.AlignRight | Qt.AlignTop
                    font.pixelSize: 20
                }
            }


        }


    }
    Label {
        text: weatherService.text
        Layout.maximumWidth: row.width
        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
        wrapMode: Text.Wrap
        font.pixelSize: 18
    }


}
