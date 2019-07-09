import pytesseract
import cv2
import numpy as np
from googletrans import Translator
import googletrans

im = cv2.imread('trtest.png',cv2.IMREAD_UNCHANGED)
s = pytesseract.image_to_string(im,lang='kor',config='--psm 6')
tr = Translator()
print(googletrans.LANGCODES)
print(tr.translate(s,dest='ja',src='ko'))