import pytesseract
import cv2
import numpy as np

def detectLine(data):
    block_num = data["block_num"]
    line_num = data["line_num"]
    word_num = data["word_num"]
    left = data["left"]
    top = data["top"]
    width = data["width"]
    height = data["height"]
    conf = data["conf"]
    texts = data["text"]

    blocks = []
    lines = []  # left, right, width, height, string
    tmpStr = ''
    curBlock = block_num[0]
    curLine = line_num[0]
    lineStart = False
    l = t = w = h = 0
    for i in range(len(block_num)):
        if curBlock != block_num[i]:
            # add this block
            pass
        if curLine != line_num[i]:
            # add this line
            pass
        if conf[i] < 0:
            continue
print(type(np.array([1,2,3,4])))
im = cv2.imread("rotated.JPG",cv2.IMREAD_UNCHANGED)
cv2.rectangle(im,(100,100),(500,500),(0,255,0),3)
#im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#ret, im = cv2.threshold(im,127,255,cv2.THRESH_BINARY_INV)
#w, h = im.shape
#m = cv2.getRotationMatrix2D((w/2,h/2),90,1)
dst = im
#dst = cv2.warpAffine(im,m,(h,w))
cv2.imshow("thr",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(pytesseract.image_to_string(dst, lang="jpn", config='--psm 3'))
#a = pytesseract.image_to_boxes(im, lang="jpn", config='--psm 7')
b = pytesseract.image_to_data(dst, lang="jpn",config='--psm 6',output_type=pytesseract.Output.DICT)
#export_csv = b.to_csv(r'test.csv', index = None, header=True, encoding='utf-8-sig')
#print(a)
print(b)