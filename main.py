import time
import win32gui
import numpy as np
import matplotlib.pyplot as plt
from Windowlist import getOpenWindow
from ScreenViewer import ScreenViewer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QImage

def main():
    windowList = list(getOpenWindow())
    for i in range(len(windowList)):
        print(i,".",win32gui.GetWindowText(windowList[i][0]))
    print(len(windowList))
    num = 2#int(input("Choose Window"))         can't capture visual code
    sv = ScreenViewer()
    sv.GetHWND(win32gui.GetWindowText(windowList[num][0]))
    im = sv.GetScreenImg()
    plt.imshow(im)
    plt.show()
    
if __name__ == "__main__":
    main()