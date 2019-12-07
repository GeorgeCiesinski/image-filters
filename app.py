# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:37:51 2019

@author: George Ciesinski
"""

import cv2
import numpy as np
import tkinter
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk


# Temporary function
# TODO: Delete this function
def doNothing():
    print("I am doing nothing")

# Dummy function that does nothing (as a dummy event handler for Trackbars)
def dummy():
    pass

# Opens an open_dialog allowing users to select a file they want to open
def open_dialog():
    root.filename = filedialog.askopenfilename(
        initialdir="/", 
        title = "Select a File", 
        filetypes=(
                ("png files", "*.png"), 
                ("jpg files", "*jpg"), 
                ("all files", "*.*")
                )
        )

"""
tkinter GUI
"""

# Main tkinter window
root = tkinter.Tk()

# Window Setup
root.title("Image Filters")
root.geometry("800x400")

"""
Window Menu
"""

menu = tkinter.Menu(root)
root.config(menu=menu)

# File Menu
fileMenu = tkinter.Menu(menu)
menu.add_cascade(label="File", menu = fileMenu)
fileMenu.add_command(label="Open", command = open_dialog)
fileMenu.add_command(label="Save", command = doNothing)
fileMenu.add_separator()
fileMenu.add_command(label="Quit", command = doNothing)

# Edit Menu
editMenu = tkinter.Menu(menu)
menu.add_cascade(label="Help", menu=editMenu)


# OpenCV Test
# Load image
image = cv2.imread('cityscape.jpg')

# Get image dimensions
height, width, no_channels = image.shape

# Create canvas to fit the image
canvas = tkinter.Canvas(root, width = width, height = height)
canvas.pack()

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = Image.fromarray(image)
image = ImageTk.PhotoImage(image)

canvas.create_image(0, 0, image=image, anchor=tkinter.NW)
root.geometry(f"{width}x{height}")





root.mainloop()

"""
Define convolution kernels
"""

# Kernels

identity_kernel = np.array([
        [0, 0, 0],
        [0, 1, 0], 
        [0, 0, 0]
        ])
    
sharpen_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
        ])

# getGaussianKernel(size, standard_deviation) | Larger numbers result in more blurring
gaussian_kernel1 = cv2.getGaussianKernel(3, 0)

gaussian_kernel2 = cv2.getGaussianKernel(5, 0)

# also known as the averaging kernel (takes average of pixel values in the window)
box_kernel = np.array([
        [1, 1, 1], 
        [1, 1, 1], 
        [1, 1, 1]
        ], np.float32) / 9

    
# Kernel array
kernels = [
        identity_kernel, 
        sharpen_kernel, 
        gaussian_kernel1, 
        gaussian_kernel2, 
        box_kernel
        ]
    
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
# TODO: Make trackbars the same width in Linux...
# Arguments: trackbarName, windowName, value (initial), count (max value), onChange (event handler)
# Contrast Trackbar
cv2.createTrackbar('contrast', 'Image Filters', 1, 100, dummy)
# Brightness Trackbar - initial value is 50 to compensate for negative brightness (cv doesn't allow negative values)
cv2.createTrackbar('brightness', 'Image Filters', 50, 100, dummy)
# Filter Trackbar
cv2.createTrackbar('filters', 'Image Filters', 0, len(kernels)-1, dummy)
# Grayscale Trackbar - switch only: values 0 & 1.
cv2.createTrackbar('grayscale', 'Image Filters', 0, 1, dummy)

# Count for saving images
count = 1

# Main UI Loop
# For each iteration: Pulls trackbar values, applies any filters, waits for keypress, and shows image
while True:
    # read all of the trackbar values
    grayscale = cv2.getTrackbarPos('grayscale', 'Image Filters')
    contrast = cv2.getTrackbarPos('contrast', 'Image Filters')
    brightness = cv2.getTrackbarPos('brightness', 'Image Filters')
    # kernel index
    kernel_idx = cv2.getTrackbarPos('filters', 'Image Filters')
    
    # apply the filters
    color_modified = cv2.filter2D(color_original, -1, kernels[kernel_idx])
    gray_modified = cv2.filter2D(gray_original, -1, kernels[kernel_idx])
    
    """
    Apply the brightness and contrast
    dst = cv2.addWeighted(src1, alpha, src2, beta, gamma)
    dst = cv2.addWeighted(image, contrast, zeros_image, 0, brightness) || src2 must be image of 0's, so we use np.zeros_like to do this
    """
    color_modified = cv2.addWeighted(color_modified, contrast, np.zeros_like(color_original), 0, brightness - 50)
    gray_modified = cv2.addWeighted(gray_modified, contrast, np.zeros_like(gray_original), 0, brightness - 50)
    
    # Wait for keypress (100 milliseconds)
    key = cv2.waitKey(100)
    
    # ord converts character into integer, compares it to the integer value "key"
    # If key is q, program will quit
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Save image
        if grayscale == 0:
            cv2.imwrite('output\output-{}.png'.format(count), color_modified)
        else:
            cv2.imwrite('output\output-{}.png'.format(count), gray_modified)
        
        # Increment count to avoid overwriting previous saved files
        count +=1
    
    # Show the image
    if grayscale == 0:
        # Show color as trackbar is set to color
        cv2.imshow('Image Filters', color_modified)
    else:
        cv2.imshow('Image Filters', gray_modified)

    # Todo: If x is pressed, app should quit the same way as with q

# Window Cleanup
cv2.destroyAllWindows()
