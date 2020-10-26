import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Controls.Universal 2.1
import QtQuick.VirtualKeyboard 2.2
import QtQuick.Extras 1.4
import QtQuick.Layouts 1.3
import QtQml 2.2
import QtMultimedia 5.8

import "../config"
import "apps/time"
import "apps/wienerlinien"
import "apps/weather"
import "apps/greeting"
import "apps/fortune"
import "apps/oralb"

import HomeAssistant 1.0
import Slack 1.0
import Serial 1.0
import Mqtt 1.0
import Performance 1.0
//import FaceRecognizer 1.0
//import FaceRecognition 1.0
//import Webinterface 1.0

ApplicationWindow {
    //property string backgroundColor: "black"
    //property string textColor: "white"
    //property string backgroundColor: "white"
    //property string textColor: "black"
    //property string lightTextColor: "#cccccc"

    property bool overrideInputpanel: false
    property Secret secret: Secret { }

    property bool mirrorActive: true
    property bool hasMovement: false
    property bool hasDisplayOn: false

    property string faces: ""

    id: mainWindow
    width: 1200
    height: 1920

 //   maximumHeight: height
 //   maximumWidth: width

 //   minimumHeight: height
 //   minimumWidth: width

    Material.theme: Material.Dark
    Universal.theme: Universal.Dark
    Material.background: "black"
    Material.foreground: "white"
    Material.accent: "#8cd3ff"
    Material.primary : Material.Blue

    color: "black"

    Component.onCompleted: {
        mirrorActive = false
    }

    HomeAssistantService {
        id: homeAssistantService
        hostname: secret.homeAssistantHostname
        port: secret.homeAssistantPort
        secure: secret.homeAssistantSecure
        accessToken: secret.homeAssistantAccessToken

        Component.onCompleted: {
            homeAssistantService.start()
        }

        // Faces

        property Timer faceTimeoutTimer: Timer {
            interval: 10000
            onTriggered: {
                mainWindow.faces = homeAssistantService.detectedFaces;
            }
        }

        property string detectedFaces;
        property HomeAssistantStateListener faceListener: HomeAssistantStateListener {
            connection: homeAssistantService
            entityId: "image_processing.dlib_face_mirror"

            onStateChanged: {
                var tmp = ""
                for (var i = 0; i < names.length; i++) {
                    if (i != 0) {
                        if (i == names.length-1) {
                            tmp += " and "
                        } else {
                            tmp += ", "
                        }
                    } else {
                        tmp += " "
                    }

                    tmp += names[i]
                }

                if ((tmp == "" && mainWindow.faces != "") || (tmp == "Unknown" && mainWindow.faces != "Unknown")) {
                    homeAssistantService.detectedFaces = tmp;
                    homeAssistantService.faceTimeoutTimer.start();
                } else {
                    mainWindow.faces = tmp;
                    homeAssistantService.faceTimeoutTimer.restart();
                    homeAssistantService.faceTimeoutTimer.stop();
                }

            }
        }
    }

    SlackService {
        id: slackService
        token: secret.slackToken
        Component.onCompleted: {
            slackService.start()
        }
    }
 
    Timer {
        id: displayTimeoutTimer
        interval: 60000
        onTriggered: {
            console.log("display off")
            serialService.turnDisplayOff()
        }
    }

    SerialService {
        id: serialService
        device: "/dev/arduino"
        Component.onCompleted: {
            this.open();
        }

        onMovementDetected: {
            //console.log("display on")
            //serialService.turnDisplayOn()
        }

        onMovementEnded: {
            console.log("movement ended")
            displayTimeoutTimer.restart()
        }

        onDisplayOn: {
            //faceRecognitionService.start()
        }

        onDisplayOff: {
            //faceRecognitionService.stop()
            greetingsPanel.next()
            fortunePanel.next()
        }
    }

    MqttService {
        id: mqttService
        hostname: secret.mqttHost
        port: secret.mqttPort

        Component.onCompleted: {
            mqttService.start()
        }
    }

    PerformanceService {
        id: performanceService
    }

    Connections {
        target: mainWindow
        function onMirrorActiveChanged() {
            if (mainWindow.mirrorActive) {
                performanceService.setPerformance(100)
            } else {
                performanceService.setPerformance(21)
            }
        }
    }

    Connections {
        target: serialService
        function onMovementDetected() {
            mqttService.publish("hallway/mirror/movement", "on")
            mainWindow.mirrorActive = true
            mainWindow.hasMovement = true
        }

        function onMovementEnded() {
            mqttService.publish("hallway/mirror/movement", "off")
            mainWindow.hasMovement = false
        }

        function onDisplayOn() {
            mqttService.publish("hallway/mirror/display", "on")
            mainWindow.hasDisplayOn = true
        }

        function onDisplayOff() {
            mqttService.publish("hallway/mirror/display", "off")
            mainWindow.mirrorActive = false
            mainWindow.hasDisplayOn = false
        }
    }

    Timer {
        interval: 10000
        running: true
        repeat: true
        onTriggered: {
           mqttService.publish("hallway/mirror/movement", mainWindow.hasMovement ? "on" : "off");
           mqttService.publish("hallway/mirror/display", mainWindow.hasDisplayOn ? "on" : "off");
        }
    }

/*    Camera {
        id: cameraService

        imageProcessing.whiteBalanceMode: CameraImageProcessing.WhiteBalanceFlash

        exposure {
            exposureCompensation: -1.0
            exposureMode: Camera.ExposurePortrait
            manualIso: 1600
        }

        viewfinder.resolution: Qt.size(1280, 720)

        flash.mode: Camera.FlashRedEyeReduction
    }

    FaceRecognizierService {
        id: faceRecognitionService
        camera: cameraService

        property string name: ""

        onFacesDetected: {
            var faces = faceRecognitionService.faces
            var tmp = ""

            for (var i = 0; i < faces.length; i++) {
                var face = faces[i]
                var name = face[1]

                if (i != 0) {
                    if (i == faces.length-1) {
                        tmp += " and "
                    } else {
                        tmp += ", "
                    }
                } else {
                    tmp += " "
                }

                tmp += name
            }

            if (tmp == "") {
                faceTimeoutTimer.start()
            } else {
                faceRecognitionService.name = tmp
                faceTimeoutTimer.stop()
            }


        }

        onStopped: {
            faceRecognitionService.name = ""
        }

    }

    /*WebinterfaceService {
        camera: cameraService
    }
*/

    Column {
        anchors.top: parent.top
        anchors.topMargin: 25
        anchors.rightMargin: 25
        anchors.right: parent.right
        spacing: 30

        WeatherPanel {
            city: "48.184981,16.355226"
            key: secret.darkSkyKey
        }

        ToothbrushPanel {
            id: toothbrushPanel
            anchors.right: parent.right
        }

    }

    InputPanel {
        id: inputPanel
        height: visible ? 400 : 0
        //y: Qt.inputMethod.visible ? parent.height - inputPanel.height : parent.height
        //visible: Qt.inputMethod.visible && !overrideInputpanel
        visible: false
        anchors.rightMargin: 50
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.leftMargin: 50
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
    }

    AppPanel {
        id: appPanel
        height: 700
        anchors.right: parent.right
        anchors.rightMargin: 25
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.bottom: inputPanel.top
        anchors.bottomMargin: 25
    }

    Column {
        id: row
        width: 300
        height: 300
        spacing: 20
        anchors.left: parent.left
        anchors.leftMargin: 25
        anchors.top: parent.top
        anchors.topMargin: 25

        TimePanel  {
            id: timePanel
        }

        WienerLinienPanel {
            width: 300
            height: 300

            rbls: [769, 1698, 1687]
            key: secret.wienerLinienKey
        }
    }

    GreetingPanel {
        id: greetingsPanel
        anchors.top: parent.top
        anchors.topMargin: 1100
        anchors.horizontalCenter: parent.horizontalCenter
    }

    FortunePanel {
        id: fortunePanel
        anchors.top: greetingsPanel.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 5
    }



}
