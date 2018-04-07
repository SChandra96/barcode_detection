import cv2
import numpy as np
import math

img = cv2.imread('UPC-A.png')
img = cv2.resize(img, (350, 350))
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

numpy_row = np.asarray(binarized_scanline_row)
numpy_row = np.trim_zeros(numpy_row)

map_pixels_to_bit = 0
bit_sequence = []
left_bit_to_digit_map = {'0001101': 0,
                        '0011001': 1,
                        '0010001': 2,
                        '0111101': 3,
                        '0100011': 4,
                        '0110001': 5,
                        '0101111': 6,
                        '0111011': 7,
                        '0110111': 8,
                        '0001011': 9,
                         }
num_of_digits_read = 0
for col in range(len(numpy_row)):
    if numpy_row[col] == 1:
        map_pixels_to_bit += 1
    else:
        break
last_index_appended = 0
for col in range(1, len(numpy_row)):
    if numpy_row[col] != numpy_row[col-1]:
        print(col)
        print(last_index_appended)
        bit_sequence.append(str(numpy_row[col-1])*(math.ceil(float(col-last_index_appended)/map_pixels_to_bit)))
        last_index_appended = col

string_bit_sequence = ''.join(bit_sequence)
upc_code_array= []

for i in range(3, len(string_bit_sequence), 7):
    if num_of_digits_read == 7:
        break

    num_of_digits_read += 1
    current_bit_sequence = string_bit_sequence[i:i + 7]
    print(current_bit_sequence)
    if current_bit_sequence in left_bit_to_digit_map:
        upc_code_array.append(str(left_bit_to_digit_map[current_bit_sequence]))
    else:
        upc_code_array.append('*')
print(white_bg)
print(map_pixels_to_bit)
print(numpy_row)
print(np.asarray(bit_sequence))
print(''.join(upc_code_array))