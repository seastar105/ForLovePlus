from PIL import Image
import numpy as np
from win32 import win32gui
import win32ui, win32con
from threading import Thread, Lock
import time
from ctypes import windll

# this code is based on code at https://github.com/nicholastoddsmith/poeai/blob/master/ScreenViewer.py
# which has MIT License

#Asynchronously captures screens of a window. Provides functions for accessing
#the captured screen.
class CaptureUnit:

    def __init__(self):
        self.mut = Lock()
        self.first = False
        self.hwnd = None
        self.its = None               #Time stamp of last image
        self.curImage = None          #i0 is the latest image
        self.tmpImage = None          #i1 is used as a temporary variable
        self.loopFlag = False         #Continue looping flag
        self.thrd = Thread(target=self.ScreenUpdateT)
        #Left, Top, Right, and bottom of the screen window
        self.winLeft, self.winTop, self.winRight, self.winBottom = 0, 0, 0, 0

    def GetHWND(self, HWND):
        '''
        Gets handle of window to view
        HWND:         Handle of window to be captured
        Return:        True on success; False on failure
        '''
        if win32gui.IsWindowVisible(HWND):
            self.hwnd = HWND
            self.winLeft, self.winTop, self.winRight, self.winBottom = win32gui.GetWindowRect(self.hwnd)
            return True
        return False

    #Get the latest image of the window
    def GetScreen(self):
        while self.curImage is None:      #Screen hasn't been captured yet
            pass
        s = self.curImage
        return s

    #Get's the latest image of the window along with timestamp
    def GetScreenWithTime(self):
        while self.curImage is None:      #Screen hasn't been captured yet
            pass
        self.mut.acquire()
        s = self.curImage
        t = self.its
        self.mut.release()
        return s, t

    #Gets the screen of the window referenced by self.hwnd
    def GetScreenImg(self):
        if self.hwnd is None:
            raise Exception("HWND is none. HWND not called or invalid window name provided.")
        l,t,r,b = win32gui.GetWindowRect(self.hwnd)
        self.winLeft, self.winTop, self.winRight, self.winBottom = win32gui.GetClientRect(self.hwnd)
        # Calculate Width of Window
        w = self.winRight - self.winLeft
        # Calculate Height of Window
        h = self.winBottom - self.winTop

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        #First 2 tuples are top-left and bottom-right of destination
        #Third tuple is the start position in source
        cDC.BitBlt((0,0), (w, h), dcObj, (9, 9), win32con.SRCCOPY)
        #result = windll.user32.PrintWindow(self.hwnd, cDC.GetSafeHdc(),0)
        bmInfo = dataBitMap.GetInfo()
        im = np.frombuffer(dataBitMap.GetBitmapBits(True), dtype = np.uint8)   # Numpy Implementation
        #bmStr = dataBitMap.GetBitmapBits(True)
        #im = Image.frombuffer('RGB',(bmInfo['bmWidth'],bmInfo['bmHeight']),bmStr,'raw','BGRX',0,1) PIL is too slow
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        #Bitmap has 4 channels like: BGRA. Discard Alpha and flip order to RGB
        return np.array(im.reshape(bmInfo['bmHeight'], bmInfo['bmWidth'], 4)[:, :, -2::-1])

    #Begins recording images of the screen
    def Start(self):
    #if self.hwnd is None:
    #    return False
        if self.first == False:
            self.first = True
            self.thrd.start()
        self.loopFlag = True
        return True

    #Stop the async thread that is capturing images
    def Stop(self):
        if self.first == False:
            return
        self.loopFlag = False

    #Thread used to capture images of screen
    def ScreenUpdateT(self):
        #Keep updating screen until terminating
        while self.loopFlag:
            t1 = time.time()
            self.tmpImage = self.GetScreenImg()
            #print('Elapsed: ' + str(time.time() - t1))
            self.mut.acquire()
            self.curImage = self.tmpImage               #Update the latest image in a thread safe way
            self.its = time.time()
            self.mut.release()