from win32 import win32gui
from win32 import win32process
import win32con

def EnumWindowsHandler(hwnd, extra):
    style = win32gui.GetWindowLong(hwnd,-16)
    if style & 0x10000000 == 0x10000000 and style & 0x00C00000 == 0x00C00000:
        if win32gui.GetWindowTextLength(hwnd) != 0:
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetParent(hwnd) == 0:
                hicon = win32gui.GetClassLong(hwnd, -14)
                if hicon:
                    extra.add((hwnd, win32gui.GetWindowText(hwnd)))

def EnumWindowsHandler2(hwnd,extra):
    if win32gui.GetWindowTextLength(hwnd) != 0 and \
        win32gui.IsWindowEnabled(hwnd) and \
        win32gui.IsWindowVisible(hwnd) and \
        win32gui.GetWindowLong(hwnd, win32con.WS_EX_TOOLWINDOW) == 0 and \
        win32gui.GetParent(hwnd) == 0:
            extra.add((hwnd, win32gui.GetWindowText(hwnd)))

'''
    it returns list of handlers of open windows as set
'''

def getOpenWindow():
    desktop = win32gui.GetDesktopWindow()
    windowSet = set()
    win32gui.EnumWindows(EnumWindowsHandler,windowSet)
    return list(windowSet)

if __name__ == '__main__':
    list1 = getOpenWindow()
    print(list1)