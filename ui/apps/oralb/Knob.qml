import QtQuick 2.0

Item {
    id: knob
    transformOrigin: Item.Center

    property int lineWidth: width / 10

    property color knobBackgroundColor: Qt.rgba(0.8, 0.8, 0.8, 0.2)
    property color knobColor: "white";

    property double from:0
    property double value: 10
    property double to: 100

    function update(value) {
        knob.value = value
        canvas.requestPaint()
    }

    Canvas {
        id: background
        width: parent.width
        height: parent.height
        antialiasing: true

        property int radius: background.width/2 - spacing/2
        property int spacing: 1.5 * knob.lineWidth

        onPaint: {
            var ctx = background.getContext('2d');
            ctx.strokeStyle = knob.knobBackgroundColor;
            ctx.lineWidth = knob.lineWidth;
            ctx.lineCap = "round"

            ctx.beginPath();
            ctx.clearRect(0, 0, background.width, background.height);
            ctx.arc(spacing + radius, radius, radius - knob.lineWidth, -Math.PI/2, 0, false);
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(spacing + radius, radius + spacing, radius - knob.lineWidth, 0, Math.PI/2, false);
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(radius, radius + spacing, radius - knob.lineWidth, Math.PI/2, Math.PI, false);
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(radius, radius, radius - knob.lineWidth, Math.PI, Math.PI*3/2, false);
            ctx.stroke();
        }
    }

    Canvas {
        id:canvas
        width: parent.width
        height: parent.height
        antialiasing: true

        property double step1: Math.min((Math.max(knob.value -  0, 0) / 100 * Math.PI/2) * 4, Math.PI/2)
        property double step2: Math.min((Math.max(knob.value - 25, 0) / 100 * Math.PI/2) * 4, Math.PI/2)
        property double step3: Math.min((Math.max(knob.value - 50, 0) / 100 * Math.PI/2) * 4, Math.PI/2)
        property double step4: Math.min((Math.max(knob.value - 75, 0) / 100 * Math.PI/2) * 4, Math.PI/2)
        property int spacing: 1.5 * knob.lineWidth
        property int radius: width/2 - spacing/2

        onPaint: {
            var ctx = canvas.getContext('2d');
            ctx.strokeStyle = knob.knobColor;
            ctx.lineWidth = knob.lineWidth;
            ctx.lineCap = "round"

            ctx.beginPath();
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.arc(spacing + radius, radius, radius - knob.lineWidth, -Math.PI/2, -Math.PI/2 + step1, false);
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(spacing + radius, radius + spacing, radius - knob.lineWidth, 0, 0 + step2, false);
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(radius, radius + spacing, radius - knob.lineWidth, Math.PI/2, Math.PI/2 + step3, false);
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(radius, radius, radius - knob.lineWidth, Math.PI, Math.PI + step4, false);
            ctx.stroke();
        }
    }
}
