import QtQuick 2.0
import QtMultimedia 5.8

import Serial 1.0

import "../../"

AppButton {
    property Camera camera
    id: cameraButton
    image: "../icons/photo-camera-outlined-interface-symbol-inverted.png"

    onReleased: cameraWidget.open()


    CameraWidget {
        id: cameraWidget
        target: cameraButton

        onAboutToShow: {
            cameraButton.highlighted = true;

            faceRecognitionService.start()
        }

        onClosed:  {
            cameraButton.highlighted = false;
        }
    }
}
