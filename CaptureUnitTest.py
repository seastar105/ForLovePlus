import time
import win32gui
import numpy as np
import matplotlib.pyplot as plt
from Windowlist import getOpenWindow
from CaptureUnit import CaptureUnit
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QImage

def main():
    windowList = list(getOpenWindow())
    for i in range(len(windowList)):
        print(i,".",win32gui.GetWindowText(windowList[i][0]))
    print(len(windowList))
    num = 1
    sv = CaptureUnit()
    sv.GetHWND(windowList[num][0])
    im = sv.GetScreenImg()
    plt.imshow(im)
    plt.show()

if __name__ == "__main__":
    main()