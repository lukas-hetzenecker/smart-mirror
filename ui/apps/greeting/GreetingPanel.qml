import QtQuick 2.0
import QtQuick.Controls 2.1

Label {
    property string salute

    id: greetingLabel
    text: salute + "<b>" + mainWindow.faces + "</b>!"
    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignBottom
    height: 150
    width: parent.width
    font.pixelSize: 45

    Component.onCompleted: {
        next()
    }

    MouseArea {
        anchors.fill: parent;

        onPressed: {
            next()
        }
    }

    function next() {
        var date = new Date()
        if (date.getHours() > 4 && date.getHours() < 12) {
            var salutes = [
                'Good morning',
                'Rise n’ shine',
                'Wakey, wakey, eggs and bakey',
                "Top o' the mornin’ to ya",
                "Rise and shine, it's time for wine",
                "Mornin', good-lookin'",
                'A vivid and creative mind characterizes you',
            ]
            greetingLabel.salute = salutes[Math.floor(Math.random() * salutes.length)];
        } else if (date.getHours() < 14) {
            var salutes = [
                'Good Day',
                'See you later',
                'Have a safe day',
                "G'day, mate",
                "Live long and prosper",
                'Welcome',
            ]
            greetingLabel.salute = salutes[Math.floor(Math.random() * salutes.length)];
        } else if (date.getHours() < 17) {
            var salutes = [
                'Good Afternoon',
                'Ahoy',
                'Howdy',
                "Aloha",
                "Whaddup",
                '‘Ello',
            ]
            greetingLabel.salute = salutes[Math.floor(Math.random() * salutes.length)];
        } else {
            var salutes = [
                'Good Night',
                'Nighty Night',
                'Go to bed, you sleepy head',
                "Sleep tight",
                "Lights out",
                "See ya' in the mornin'",
                'Sweet dreams',
                'Goodnight',
                'Dream about me',
                'Sleep snug as a bug in a rug',

            ]
            greetingLabel.salute = salutes[Math.floor(Math.random() * salutes.length)];
        }
    }
}
