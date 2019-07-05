from win32 import win32gui


def EnumWindowsHandler(hwnd, extra):
    style = win32gui.GetWindowLong(hwnd,-16)
    if style & 0x10000000 == 0x10000000 and style & 0x00C00000 == 0x00C00000:
        if win32gui.GetWindowTextLength(hwnd) != 0:
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetParent(hwnd) == 0:
                hicon = win32gui.GetClassLong(hwnd, -14)
                if hicon:
                    extra.add((hwnd, win32gui.GetWindowText(hwnd)))


'''
    it returns list of handlers of open windows as set
'''

def getOpenWindow():
    desktop = win32gui.GetDesktopWindow()
    windowSet = set()
    win32gui.EnumWindows(EnumWindowsHandler,windowSet)
    return list(windowSet)