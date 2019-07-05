import sys
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog, QVBoxLayout
import win32gui
from PIL import ImageQt
from ScreenViewer import ScreenViewer
from Windowlist import getOpenWindow

class Capture(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.sv = ScreenViewer()
        self.list = getOpenWindow()
        self.cur_img = None
        self.frame = QLabel()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.frame)
        self.setLayout(layout)
        self.fw = 640
        self.fh = 480

    def setHWND(self):
        self.list = list(getOpenWindow())
        print(self.list)
        num = 0
        self.sv.GetHWND(self.list[num][0])
        self.sv.GetScreenImg()

    def getNextFrame(self):
        im = self.sv.GetScreen()
        height, width, channel = im.shape
        bytesPerLine = 3 * width
        self.cur_img = QtGui.QImage(im.tobytes(), width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(self.cur_img)
        pixmap.scaled(self.fw, self.fh, QtCore.Qt.KeepAspectRatio)
        self.frame.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getNextFrame)
        self.timer.start(1000./30)
        self.sv.Start()
    
    def stop(self):
        self.timer.stop()
        self.sv.Stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Capture()
    ex.setHWND()
    ex.start()
    ex.show()
    sys.exit(app.exec_())
