# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:37:51 2019

@author: georg
"""

import cv2
import numpy as np


# Dummy function that does nothing (as a dummy event handler for Trackbars)
def dummy():
    pass

"""
Read in an image and make a grayscale copy
"""

# TODO: Add button to open a specific image using relative paths
# Reads image in folder and assigns it to color_original variable
color_original = cv2.imread('cityscape.jpg')
# Converts to grayscale and saves as gray_original variable
gray_original = cv2.cvtColor(color_original, cv2.COLOR_BGR2GRAY)

"""
Create the UI (Window and trackbars)
"""

cv2.namedWindow('Image Filters')
# TODO: Get rid of the black rectangle in window

# TODO: Make trackbars the same width in Linux...
# Arguments: trackbarName, windowName, value (initial), count (max value), onChange (event handler)
# Contrast Trackbar
cv2.createTrackbar('contrast', 'Image Filters', 1, 100, dummy)
# Brightness Trackbar - initial value is 50 to compensate for negative brightness (cv doesn't allow negative values)
cv2.createTrackbar('brightness', 'Image Filters', 50, 100, dummy)
# Filter Trackbar
# TODO: Update max value to number of filters
cv2.createTrackbar('filters', 'Image Filters', 0, 1, dummy)
# Grayscale Trackbar - switch only: values 0 & 1.
cv2.createTrackbar('grayscale', 'Image Filters', 0, 1, dummy)


# Main UI Loop
# For each iteration: Pulls trackbar values, applies any filters, waits for keypress, and shows image
while True:
    # TODO: read all of the trackbar values
    # Read grayscale trackbar value
    grayscale = cv2.getTrackbarPos('grayscale', 'Image Filters')
    # TODO: apply the filters
    # TODO: apply the brightness and contrast
    
    # Wait for keypress (100 milliseconds)
    key = cv2.waitKey(100)
    
    # ord converts character into integer, compares it to the integer value "key"
    # If key is q, program will quit
    if key == ord('q'):
        break
    elif key == ord('s'):
        # TODO: Save image
        pass
    
    # Show the image
    if grayscale == 0:
        # Show color as trackbar is set to color
        # TODO: Show modified image
        cv2.imshow('Image Filters', color_original)
    else:
        cv2.imshow('Image Filters', gray_original)


# Window Cleanup
cv2.destroyAllWindows()
