import win32gui
import time
from PIL import ImageGrab
from ScreenViewer import ScreenViewer
from Windowlist import getOpenWindow

def GetScreenshot1():
    im = ImageGrab.grab()

if __name__ == "__main__":
    list = list(getOpenWindow())
    sv = ScreenViewer()
    sv.GetHWND(win32gui.GetWindowText(list[1][0]))
    sv.Start()
    time.sleep(1)
    sv.Stop()