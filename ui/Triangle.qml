import QtQuick 2.7
import QtQuick.Controls.Material 2.1

Canvas {
        id: root

        // canvas size
        width: 30; height: 20
        // handler to override for drawing
        onPaint: {
            // get context to draw with
            var ctx = getContext("2d")
            // setup the fill
            ctx.fillStyle = Material.color(Material.Grey, Material.Shade600)
            // begin a new path to draw
            ctx.beginPath()
            ctx.moveTo(0,0)
            ctx.lineTo(width,0)
            ctx.lineTo(width/2,height)
            ctx.closePath()
            ctx.fill()
        }
    }
