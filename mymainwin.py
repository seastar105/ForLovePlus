import sys
import numpy as np
import pytesseract
from googletrans import Translator
import cv2
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QWidget, QLabel,
                                QFrame, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox,
                                QPushButton, QLineEdit, QGridLayout)
from win32 import win32gui
import pytesseract
from CaptureUnit import CaptureUnit
from Windowlist import getOpenWindow

class Worker(QtCore.QObject):
    ''' This class is created for executing OCR.

        pytesseract takes time, and googletrans uses reqests api
    '''
    send_script = QtCore.pyqtSignal(str)
    trans_signal = QtCore.pyqtSignal(str,str,np.ndarray,str,bool)
    def __init__(self, parent=None):
        super(self.__class__,self).__init__(parent)
        self.translator = Translator()

    def trLang(self, src, dst):
        trSrc = ''
        trDst = ''
        if src == 'eng' : trSrc = 'en'
        if src == 'jpn' : trSrc = 'ja'
        if src == 'kor' : trSrc = 'ko'
        if dst == 'eng' : trDst = 'en'
        if dst == 'jpn' : trDst = 'ja'
        if dst == 'kor' : trDst = 'ko'
        return trSrc, trDst

    # SLOT for trans_signal, it emits send_script to send translated script
    def cropOCRandTranslate(self, src, dst, cropImage, config,inverted):
        ''' It returns translated script and it is pyqtslot

        src : source language
        dst : destination language
        cropImage : Image contains texts in source language
        config : config string used in tesseract
        inverted : it determines binarization method, it is good to use inverted
                    when text has white color and has black background
        '''
        if (cropImage.shape[0] == 0 and cropImage.shape[1] == 0) \
                    or cropImage.size <= 0:
            self.send_script.emit('')
            return
        QtCore.QThread.msleep(100)
        method = cv2.THRESH_BINARY_INV if inverted else cv2.THRESH_BINARY
        trSrc, trDst = self.trLang(src, dst)
        im = cv2.cvtColor(cropImage,cv2.COLOR_RGB2GRAY)
        ret, im = cv2.threshold(im,127,255,method)
        script = pytesseract.image_to_string(im,lang=src,config=config)
        translated = self.translator.translate(script, dest=trDst,src=trSrc)
        self.send_script.emit(translated.text)


class MainWidget(QWidget) :
    ''' Main Widget used as centralwidget of mainwindow'''
    def __init__(self):
        super().__init__()
        self.initUI()

        self.captureUnit = CaptureUnit()
        self.outImage = None            # saves Captured Image
        self.invertFlag = False
        self.curHwnd = None
        self.cropImage = None
        self.curQim = None
        self.curShape = (0,0)
        self.windowName = None
        self.timer = None
        self.windowlist = []
        self.rectL, self.rectT, self.rectR, self.rectB = 0,0,0,0
        self.transFlag = False
        self.src = 'eng'
        self.dst = 'jpn'
        self.config = {'eng':'--psm 6','kor':'--psm 6','jpn':'--psm 6'}
        self.tessThrd = QtCore.QThread()
        self.tessClass = Worker()
        self.tessClass.moveToThread(self.tessThrd)
        self.resolution.setText('Resolution : ' + str(self.curShape[0]) + 'X' + str(self.curShape[1]))

        ''' ------------- connect signals ------------------'''
        self.listBox.installEventFilter(self)
        self.listBox.activated.connect(self.changeHWND)
        self.srcLangBox.activated[str].connect(self.changeSrcLang)
        self.dstLangBox.activated[str].connect(self.changeDstLang)
        self.leftInput.textChanged[str].connect(self.leftChanged)
        self.rightInput.textChanged[str].connect(self.rightChanged)
        self.topInput.textChanged[str].connect(self.topChanged)
        self.botInput.textChanged[str].connect(self.botChanged)
        self.transAble.stateChanged.connect(self.toggleTrans)
        self.tessClass.send_script.connect(lambda script:self.printTranslation(script))
        self.tessClass.trans_signal.connect(self.tessClass.cropOCRandTranslate)
        self.inverted.stateChanged.connect(self.toggleInvert)
        self.tessThrd.start()
        ''' ------------- end connect signals ----------------'''

    def initUI(self):
        self.screen = QLabel()          # displays captured image
        self.scription = QLabel()
        self.resolution = QLabel()
        self.VLayout = QVBoxLayout()
        self.HLayout1 = QHBoxLayout()
        self.HLayout2 = QHBoxLayout()
        self.listBox = QComboBox()
        self.srcLangBox = QComboBox()
        self.dstLangBox = QComboBox()
        self.topInput = QLineEdit()
        self.botInput = QLineEdit()
        self.leftInput = QLineEdit()
        self.rightInput = QLineEdit()
        self.transAble = QCheckBox()
        self.inverted = QCheckBox()

        self.lrValidator = QtGui.QIntValidator()
        self.tbValidator = QtGui.QIntValidator()
        self.leftInput.setText('0')
        self.rightInput.setText('0')
        self.topInput.setText('0')
        self.botInput.setText('0')
        self.topInput.setValidator(self.tbValidator)
        self.botInput.setValidator(self.tbValidator)
        self.leftInput.setValidator(self.lrValidator)
        self.rightInput.setValidator(self.lrValidator)

        self.scription.setText("Translated Script")
        self.scription.setMinimumSize(50,50)
        self.scription.setFrameShape(QFrame.Box)
        self.srcLangBox.addItem("eng")
        self.srcLangBox.addItem("kor")
        self.srcLangBox.addItem("jpn")
        self.dstLangBox.addItem("jpn")
        self.dstLangBox.addItem("eng")
        self.dstLangBox.addItem("kor")
        self.transAble.setText("translate")
        self.inverted.setText("Binary Invert")
        self.HLayout1.addWidget(self.screen)
        self.HLayout2.addWidget(self.srcLangBox)
        self.HLayout2.addWidget(self.dstLangBox)
        self.VLayout.addWidget(self.resolution)
        self.VLayout.addStretch()
        self.VLayout.addLayout(self.HLayout1)
        self.VLayout.addStretch()
        self.VLayout.addWidget(self.listBox)
        self.VLayout.addStretch()
        self.VLayout.addLayout(self.HLayout2)
        self.VLayout.addStretch()
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
        hlayout.addWidget(self.scription)
        hlayout.addLayout(gridLayout1)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.transAble)
        vlayout.addWidget(self.inverted)
        hlayout.addLayout(vlayout)
        self.VLayout.addLayout(hlayout)

    ''' ------------------------ SLOTS ------------------------'''
    def toggleInvert(self):
        if self.inverted.isChecked():
            self.invertFlag = True
        else:
            self.invertFlag = False

    def toggleTrans(self):
        if self.transAble.isChecked() :
            self.transFlag = True
            self.tessClass.trans_signal.emit(self.src, self.dst, self.cropImage, self.config[self.src],self.invertFlag)
        else:
            self.transFlag = False

    def printTranslation(self, script):
        ''' This function is called when send_script signal is emitted

            it emits trans_signal after print translated script for syncrhonizing
        '''
        self.scription.setText(script)
        if self.transFlag:
            self.tessClass.trans_signal.emit(self.src, self.dst, self.cropImage, self.config[self.src],self.invertFlag)

    def changeSrcLang(self, str):
        self.src = str

    def changeDstLang(self, str):
        self.dst = str

    def leftChanged(self, str):
        if str == '':
            self.rectL = 0
        else :
            self.rectL = int(str)

    def rightChanged(self, str):
        if str == '':
            self.rectR = 0
        else :
            self.rectR = int(str)

    def topChanged(self, str):
        if str == '':
            self.rectT = 0
        else :
            self.rectT = int(str)

    def botChanged(self, str):
        if str == '':
            self.rectB = 0
        else :
            self.rectB = int(str)
    ''' ---------------------END SLOTS ------------------------'''

    def cropFlush(self):
        self.lrValidator.setRange(0,self.curShape[1])
        self.tbValidator.setRange(0,self.curShape[0])
        self.leftInput.setText('0')
        self.rightInput.setText('0')
        self.topInput.setText('0')
        self.botInput.setText('0')

    def eventFilter(self, target, event):
        ''' it extends parent's eventFilter '''
        if target == self.listBox and event.type() == QtCore.QEvent.MouseButtonPress:
            self.updateList()
        return super().eventFilter(target, event)

    def changeHWND(self, i):
        self.Stop()
        self.SetHWND(self.windowlist[i][0])
        self.Start()

    def updateList(self):
        tmp = self.listBox.currentText()
        self.listBox.clear()
        self.windowlist = getOpenWindow()
        for i in self.windowlist:
            self.listBox.addItem(i[1])
        self.listBox.setCurrentText(tmp)

    def GetNextImage(self):
        self.outImage = self.captureUnit.GetScreenImg()
        #self.outImage = np.array(self.outImage[:,:,:])
        if self.outImage.shape != self.curShape:
            self.curShape = self.outImage.shape
            self.cropFlush()
            self.resolution.setText('Resolution : ' + str(self.curShape[0]) + 'X' + str(self.curShape[1]))
        self.cropImage = self.outImage[self.rectT:self.rectB, self.rectL:self.rectR]
        cv2.rectangle(self.outImage, (self.rectL,self.rectT),(self.rectR,self.rectB),(0,255,0),2)
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
            self.curShape = self.captureUnit.curImage.shape
            self.lrValidator.setRange(0,self.curShape[1])
            self.tbValidator.setRange(0,self.curShape[0])
            self.leftInput.setText('0')
            self.rightInput.setText('0')
            self.topInput.setText('0')
            self.botInput.setText('0')
            self.resolution.setText('Resolution : ' + str(self.curShape[0]) + 'X' + str(self.curShape[1]))
        self.captureUnit.mut.release()

    def Start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.GetNextImage)
        self.timer.start(1000./30)

    def Stop(self):
        if self.timer:
            self.timer.stop()

    def SetSize(self, height, width):
        self.screenHeight = int(height)
        self.screenWidth = int(width)
        self.screen.resize(self.screenWidth, self.screenHeight)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

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
        self.setCentralWidget(self.centerWidget)

    def resizeEvent(self,event):
        self.windowWidth = self.size().width()
        self.windowHeight = self.size().height()
        self.centerWidget.SetSize(self.windowHeight * (3/4), self.windowWidth * (3/4))
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())