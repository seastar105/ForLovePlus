import sys
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QWidget, QLabel,
                                QFrame, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox,
                                QPushButton, QLineEdit, QGridLayout)
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
        self.initUI()

        self.captureUnit = CaptureUnit()
        self.curHwnd = None
        self.curQim = None
        self.windowName = None
        self.windowlist = getOpenWindow()
        self.updateList()

    def initUI(self):
        self.screen = QLabel()          # displays captured image
        self.outImage = None            # saves Captured Image
        self.VLayout = QVBoxLayout()
        self.HLayout1 = QHBoxLayout()
        self.HLayout2 = QHBoxLayout()
        self.listBox = QComboBox()
        self.srcLangBox = QComboBox()
        self.dstLangBox = QComboBox()
        self.clockButton = QPushButton()
        self.counterClockButton = QPushButton()
        self.topInput = QLineEdit()
        self.botInput = QLineEdit()
        self.leftInput = QLineEdit()
        self.rightInput = QLineEdit()
        self.transAble = QCheckBox()


        self.srcLangBox.setItemText(0,"src")
        self.dstLangBox.setItemText(0,"dst")
        self.srcLangBox.addItem("src1")
        self.dstLangBox.addItem("dst1")
        self.transAble.setText("translate")
        self.HLayout1.addWidget(self.screen)
        self.HLayout2.addWidget(self.srcLangBox)
        self.HLayout2.addWidget(self.dstLangBox)
        self.VLayout.addLayout(self.HLayout1)
        self.VLayout.addWidget(self.listBox)
        self.VLayout.addLayout(self.HLayout2)
        self.screen.setFrameShape(QFrame.Box)
        self.screen.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.VLayout)
        self.inputUI()

    def inputUI(self):
        hlayout = QHBoxLayout()
        gridLayout1 = QGridLayout()
        gridLayout1.addWidget(QLabel('Top'),0,0)
        gridLayout1.addWidget(QLabel('Bottom'),0,2)
        gridLayout1.addWidget(self.topInput,1,0)
        gridLayout1.addWidget(self.botInput,1,2)
        gridLayout1.addWidget(QLabel('Left'),2,0)
        gridLayout1.addWidget(QLabel('Right'),2,2)
        gridLayout1.addWidget(self.leftInput,3,0)
        gridLayout1.addWidget(self.rightInput,3,2)
        hlayout.addWidget(self.counterClockButton)
        hlayout.addWidget(self.clockButton)
        hlayout.addLayout(gridLayout1)
        hlayout.addWidget(self.transAble)
        self.VLayout.addLayout(hlayout)

    def updateList(self):
        self.listBox.clear()
        for i in self.windowlist:
            self.listBox.addItem(i[1])

    def setSize(self, w, h):
        self.windowSize = QtCore.QSize(w,h)

    def GetNextImage(self):
        self.outImage = self.captureUnit.GetScreen()
        height, width, channel = self.outImage.shape
        bytesPerLine = 3 * width
        self.curQim = QtGui.QImage(self.outImage.tobytes(), width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(self.curQim)
        self.screen.setPixmap(pixmap.scaled(self.screenWidth,self.screenHeight,
                        QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        self.screen.setAlignment(QtCore.Qt.AlignCenter)

    def SetHWND(self, HWND):
        self.captureUnit.mut.acquire()
        if self.captureUnit.GetHWND(HWND):
            self.windowName = win32gui.GetWindowText(HWND)
            self.curHwnd = HWND
            self.captureUnit.curImage = self.captureUnit.GetScreenImg()
        self.captureUnit.mut.release()

    def Start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.GetNextImage)
        self.timer.start(1000./30)
        self.captureUnit.Start()

    def Stop(self):
        self.timer.stop()
        self.captureUnit.Stop()

    def SetSize(self, height, width):
        self.screenHeight = height
        self.screenWidth = width
        self.screen.resize(self.screenWidth, self.screenHeight)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def resizeEvent(self, event):
        print("resize")
        QMainWindow.resizeEvent(self, event)

    def initUI(self):
        self.desktopWidth =  QDesktopWidget().screenGeometry().width()
        self.desktopHeight = QDesktopWidget().screenGeometry().height()
        self.windowWidth = self.desktopWidth * 2 / 3
        self.windowHeight = self.desktopHeight * 2 / 3
        self.setGeometry((self.desktopWidth - self.windowWidth)/2, (self.desktopHeight - self.windowHeight)/2,
                            self.windowWidth, self.windowHeight)
        self.centerWidget = MainWidget()
        self.centerWidget.SetSize(self.desktopHeight/2, self.desktopWidth/2)
        self.windowlist = getOpenWindow()
        self.SetHWND(self.windowlist[0][0])     # debugging code
        self.setCentralWidget(self.centerWidget)
        self.centerWidget.setSize(self.desktopWidth/2, self.desktopHeight/2)
        self.centerWidget.Start()                            # debugging code

    def SetHWND(self, HWND):
        self.centerWidget.SetHWND(HWND)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    print(win.centerWidget.windowName)
    '''
    win = MainWidget()
    windowlist = getOpenWindow()
    win.SetHWND(windowlist[1][0])
    win.Start()
    win.setGeometry(100,100,1000,1000)
    print(win.windowName)
    '''
    win.show()
    sys.exit(app.exec_())