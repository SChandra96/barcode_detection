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
img = cv2.imread('zoomed_in_barcode.png')
cv2.imshow("barcode", img)
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



#cv2.waitKey(0)
#cv2.destroyAllWindows()