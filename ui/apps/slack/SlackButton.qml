import QtQuick 2.0

import Slack 1.0

import "../../"

AppButton {
    property SlackService connection

    id: slackButton
    image: "../icons/apps/slack.svg"

    onReleased: slackWidget.open()

    SlackWidget {
        id: slackWidget
        target: slackButton

        onAboutToShow: {
            slackButton.highlighted = true;
        }

        onClosed:  {
            slackButton.highlighted = false;
        }

    }
}
