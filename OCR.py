import pytesseract
from pytesseract import Output
import PIL.Image
import cv2

myconfig = r"--psm 3 --oem 3"
img=cv2.imread("test7.jpeg")
text=pytesseract.image_to_string(PIL.Image.open("test7.jpeg"))
height,width, _=img.shape


img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

data=pytesseract.image_to_data(img,config=myconfig, output_type=Output.DICT)

amount_boxes=len(data['text'])
for i in range(amount_boxes):
    if float(data['conf'][i])>55:
        (x,y,width,height)=(data['left'][i],data['top'][i],data['width'][i],data['height'][i])
        img=cv2.rectangle(img,(x,y),(x+width,y+height),(0,255,0),2)
    

cv2.imshow("img", img)
cv2.waitKey(0)
print(text)