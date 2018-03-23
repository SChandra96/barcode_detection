import cv2
import numpy as np

"""
Luminance 0: Black color
Center bits bit pattern: 01010
Guard bits 101

(1)
Localise barcode area in image -- article illustrates a good approach for this


Questions for decpding
Do we greyscale the image before thresholding? Effects?
Remove noise from the image?
Identifying the scaline row of pixels in image?

(2)
Binarize image: Use thresholding with luminosity method. For each pixel, calculate
luminsoity value using its rgb values. Assign luminosity to 0 or 1 based pm a certain range for white
and black

Design Choice (1): Try different ways of thresholding the barcode image.
http://www.tannerhelland.com/3643/grayscale-image-algorithm-vb6/ 
Design Choice (2): Determine luminosity range for white and black

(3)
Identify centre and guard bits of barcode
Using guard bits and center bits: determine block size

(4)
Scan left and right from centre by using "pre-determined steps" or blocking pixel

"""

def detect(img):
    img = cv2.resize(img, (350, 350))
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #x gradient and y gradient
    #barcodes have high horizontal image gradient low vertical image gradient
    #image gradient: derivative of intensity of pixel: grey level value
    #of pixel with respect to x or y coordinate.


    """
    In order to identify areas with high horizontal gradient and low vertical
    gradient, subtract y gradient from x gradient.
    Scharr filter: high pass filter
    """

    #3x3 scharr filter gives better results than 3x3 sobel filter
    #hence ksize = -1
    gradX = cv2.Sobel(grayscale, cv2.CV_64F,1,0,ksize=-1)
    gradY = cv2.Sobel(grayscale, cv2.CV_64F,0,1, ksize=-1)
    subtract = cv2.subtract(gradX, gradY)
    subtract = cv2.convertScaleAbs(subtract)

    laplacian = cv2.Laplacian(img, cv2.CV_32F)

    #blur: smoothening high frequency noise

    blur = cv2.GaussianBlur(subtract, (9, 9), 0)

    #thresholding: anything that has a intensity greater than 225
    #is converted to 0.
    #
    (_, thresh) = cv2.threshold(blur, 225, 255,cv2.THRESH_BINARY)

    #Remove vertical gaps between the strips
    #Dilation followed by erosion
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    #Erosion: removes white regions in image
    #Dilation: increases white regions in image
    closed = cv2.erode(closed, kernel, iterations = 4)
    closed = cv2.dilate(closed, kernel, iterations = 6)
    #Find contours
    (_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 0:
        return None
    c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    return box

    # draw a bounding box arounded the detected barcode and display the
    # image

camera = cv2.VideoCapture(0)
while True:
    (returned, frame) = camera.read()
    if returned:
        box = detect(frame)
        print(box)
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
        cv2.imshow("closed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
camera.release()
cv2.destroyAllWindows()


#-----------------------------------------------------
max_row, max_col = img.shape[:2]
scanline_row = int(max_row/2)
binarized_scanline_row = []
white_bg = 0
for col in range(max_col):
        r, g, b = img[scanline_row, col]
        luminosity = 0.299*r + (0.587*g) + (0.144*b)
        if luminosity < 50:
            binarized_scanline_row.append(1)
        else:
            binarized_scanline_row.append(0)
            white_bg += 1
print(white_bg)
print(binarized_scanline_row)


