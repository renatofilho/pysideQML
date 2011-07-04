from pyqml import Rectangle, Image, MouseArea, Anchor, parent
from PySide.QtCore import Qt
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView


class Rectangle1(Rectangle):
    anchors = Anchor(centerIn = parent, fill = parent)
    width = 200
    height = 200
    color = 'red'
    class Rectangle2(Rectangle):
        anchors = Anchor(centerIn = parent)
        width = 100
        height = 100
        color = 'white'
        class Image1(Image):
            anchors = Anchor(centerIn = parent)
            source = 'logo.png'
            width = 64
            height = 64
            class MouseArea2(MouseArea):
                anchors = Anchor(fill = parent)
                def onClick(self):
                    print "show"


#main

app = QApplication([])
view = QDeclarativeView()
view.scene().setBackgroundBrush(Qt.blue)

r = Rectangle1(view)
view.show()
app.exec_()

