import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Layouts 1.3
import QtMultimedia 5.8

import "../../"

PopupWidget {
    id: cameraPopup
    width: 1200
    property var persons: []

    contentItem: Item {
        width: 1200
        height: 1200

        ColumnLayout {
            spacing: 10
            Layout.alignment: Qt.AlignVCenter

            TextField {
                id: personName
                Layout.fillWidth: true
                height: 40
                focus: false
                font.pointSize: 20
            }

            VideoOutput {
                id: videoOutput
                source: camera
                focus : visible // to receive focus and capture key events when visible

                MouseArea {
                    anchors.fill: parent;

                    onPressed: {
                        camera.setCaptureMode(Camera.CaptureStillImage)
                        camera.imageCapture.captureToLocation(faceRecognitionService.folderForPerson(personName.text))
                    }
                }


                Connections {
                    target: faceRecognitionService
                    onFacesDetected: {
                        var faces = faceRecognitionService.faces
                        console.log("faces: " + faces.value);
                        console.log("faces length: " + faces.length);

                        while(persons.length > 0) {
                            var p = persons.pop();
                            p.destroy();
                        }

                        var component = Qt.createComponent("PersonRectangle.qml");
                        for (var i = 0; i < faces.length; i++) {
                            var face = faces[i];
                            console.log("face: " + face);
                            var rect = face[0];
                            var name = face[1];
                            console.log("rect: " + rect);
                            console.log("name: " + name);
                            var iRect = videoOutput.mapRectToItem(rect);
                            console.log(iRect);
                            var person = component.createObject(videoOutput, {
                                                                    "name": name,
                                                                    "x": /*videoOutput.contentRect.x +*/ iRect.x,
                                                                    "y": /*videoOutput.contentRect.y +*/ iRect.y,
                                                                    "height": iRect.height,
                                                                    "width": iRect.width
                                                                });
                            console.log(person);
                            persons.push(person);
                        }
                    }
                }

                Connections {
                    target: camera.imageCapture
                    onImageSaved: {
                        faceRecognitionService.stop()
                        faceRecognitionService.start()
                    }
                }
            }
        }

    }

}
