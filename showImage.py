import sys
import win32gui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from Windowlist import getOpenWindow
from ScreenViewer import ScreenViewer
from PIL.ImageQt import ImageQt

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.sv = ScreenViewer()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        label = QLabel(self)
        im = self.sv.GetScreenImg()
        height, width, channel = im.shape
        bytesPerLine = 3 * width
        qImg = QImage(im.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qImg)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    windowList = list(getOpenWindow())
    num = 1
    ex.sv.GetHWND(win32gui.GetWindowText(windowList[num]))
    ex.initUI()
    sys.exit(app.exec_())
   

    