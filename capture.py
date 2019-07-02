import time
from PIL import ImageGrab

def GetScreenshot1():
    im = ImageGrab.grab()

if __name__ == "__main__":
    while True:
        t1 = time.time()
        GetScreenshot1()
        t2 = time.time()
        print("Elapsed: " + str(t2-t1))
        