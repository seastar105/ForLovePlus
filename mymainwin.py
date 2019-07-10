import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QWidget, QLabel,
                                QFrame, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox,
                                QPushButton, QLineEdit, QGridLayout)
from win32 import win32gui
from myWidget import MainWidget


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