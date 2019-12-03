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


# Create the UI (Window and trackbars)
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


# TODO: Remove this line!
cv2.waitKey(0)
# Window Cleanup
cv2.destroyAllWindows()
