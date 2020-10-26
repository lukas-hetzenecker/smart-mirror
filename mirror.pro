QT += qml quick

CONFIG += c++11

SOURCES += main.cpp

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH = /home/lukas/Sync/projects/smart-mirror/mirror/plugins

# Additional import path used to resolve QML modules just for Qt Quick Designer
QML_DESIGNER_IMPORT_PATH =

# The following define makes your compiler emit warnings if you use
# any feature of Qt which as been marked deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

DISTFILES += \
    ui/TimePanel.qml \
    ui/WeatherPanel.qml \
    ui/AppPanel.qml \
    ui/main.qml \
    ui/Triangle.qml \
    qtquickcontrols2.conf \
    ui/PopupWidget.qml \
    ui/apps/assistant/AssistantWidget.qml \
    ui/apps/uber/UberWidget.qml \
    ui/apps/debug/DebugWidget.qml \
    ui/controls/MirrorRoundButton.qml \
    ui/AppButton.qml \
    ui/apps/assistant/AssistantWidget.qml \
    ui/apps/assistant/AssistantButton.qml \
    ui/apps/debug/DebugButton.qml \
    ui/apps/uber/UberButton.qml \
    ui/apps/time/TimePanel.qml \
    ui/apps/wienerlinien/WienerLinienPanel.qml \
    ui/apps/wienerlinien/StopDelegate.qml \
    ui/apps/weather/WeatherPanel.qml \
    ui/apps/homeassistant/HomeAssistantButton.qml \
    ui/apps/slack/SlackButton.qml \
    ui/apps/slack/SlackWidget.qml \
    ui/apps/slack/SlackChannelDelegate.qml \
    ui/config/Secret.qml \
    ui/apps/slack/SlackMessageDelegate.qml \
    ui/apps/slack/SlackMessageSectionDelegate.qml \
    ui/LightsWidget.qml \
    ui/apps/camera/CameraWidget.qml \
    ui/apps/camera/CameraButton.qml \
    ui/apps/camera/PersonRectangle.qml \
    ui/apps/fortune/FortunePanel.qml \
    ui/apps/fortune/fortunes.js \
    ui/apps/greeting/GreetingPanel.qml \
    ui/apps/weather/WeatherCanvas.qml \
    ui/apps/facerecognizer/FaceRecognizer.qml \
    ui/apps/oralb/Knob.qml \
    ui/apps/oralb/ToothbrushPanel.qml

RESOURCES += \
    ui/qml.qrc
