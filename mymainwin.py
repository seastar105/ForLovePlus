import sys
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QWidget, QLabel,
                                QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox)
from win32 import win32gui
from CaptureUnit import CaptureUnit
from Windowlist import getOpenWindow

'''
    MainScreen displays processed Image
    And comboboxes to choose languages to be translated
    And checkbox to choose to translate or not
'''
class MainWidget(QWidget) :
    def __init__(self):
        super().__init__()

        self.screen = QLabel()          # displays captured image
        self.outImage = None            # saves Captured Image
        self.VLayout = QVBoxLayout()
        self.HLayout1 = QHBoxLayout()
        self.HLayout2 = QHBoxLayout()
        self.srcLangBox = QComboBox()
        self.dstLangBox = QComboBox()
        self.transAble = QCheckBox()

        self.srcLangBox.setItemText(0,"src")
        self.dstLangBox.setItemText(0,"dst")
        self.srcLangBox.addItem("src1")
        self.dstLangBox.addItem("dst1")
        self.transAble.setText("trans")
        self.HLayout1.addWidget(self.screen)
        self.HLayout2.addWidget(self.srcLangBox)
        self.HLayout2.addWidget(self.dstLangBox)
        self.VLayout.addLayout(self.HLayout1)
        self.VLayout.addLayout(self.HLayout2)
        self.VLayout.addWidget(self.transAble)
        self.screenHeight = 640
        self.screenWidth = 480          # screen size will be determined by mainwindow, just default size
        self.screen.resize(self.screenHeight, self.screenWidth)
        self.screen.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.VLayout)

        self.captureUnit = CaptureUnit()
        self.curHwnd = None
        self.curQim = None
        self.windowName = None


    def GetNextImage(self):
        self.outImage = self.captureUnit.GetScreenImg()
        height, width, channel = self.outImage.shape
        bytesPerLine = 3 * width
        self.outImage = np.require(self.outImage, np.uint8, 'C')
        self.curQim = QtGui.QImage(self.outImage.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(self.curQim)
        self.screen.setPixmap(pixmap.scaled(self.screen.width(),self.screen.height(),
                        QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        self.screen.setAlignment(QtCore.Qt.AlignCenter)

    def SetHWND(self, HWND):
        self.captureUnit.mut.acquire()
        if self.captureUnit.GetHWND(HWND):
           self.windowName = win32gui.GetWindowText(HWND)
           self.curHwnd = HWND
        self.captureUnit.mut.release()

    def Start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.GetNextImage)
        self.timer.start(1000./30)

    def Stop(self):
        self.timer.stop()
        self.captureUnit.Stop()

    def SetSize(self, height, width):
        self.screenHeight = height
        self.screenWidth = width


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.desktopWidth =  QDesktopWidget().screenGeometry().width()
        self.desktopHeight = QDesktopWidget().screenGeometry().height()
        self.setGeometry(0,0,self.desktopWidth,self.desktopHeight)
        self.centerWidget = MainWidget()
        self.centerWidget.SetSize(self.desktopHeight/2, self.desktopWidth/2)
        self.windowlist = getOpenWindow()
        self.centerWidget.SetHWND(self.windowlist[1][0])
        self.setCentralWidget(self.centerWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWidget()
    windowlist = getOpenWindow()
    win.SetHWND(windowlist[1][0])
    win.Start()
    win.setGeometry(100,100,1000,1000)
    win.show()
    sys.exit(app.exec_())