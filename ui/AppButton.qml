import QtQuick 2.5
import QtQuick.Controls 2.1

import "controls"

MirrorRoundButton {
    property var image

    width: 120
    height: 120
    padding: 30
    contentItem: Image {
        antialiasing: true
        mipmap: true
        source: image
    }
}
