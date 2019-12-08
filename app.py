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
import logging


class Kernels:
    
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
    k_array = [
            identity_kernel, 
            sharpen_kernel, 
            gaussian_kernel1, 
            gaussian_kernel2, 
            box_kernel
            ]

"""
tkinter GUI
"""

class Gui:
    
    # TODO: Create save dialog
    
    def __init__(self):
        
        # Create the window
        self.create_window()
        
        # Creates the menu bar
        self.create_menu()

    # Dummy function that does nothing (as a dummy event handler for Trackbars)
    def dummy():
        print("Dummy method.")
        
    def create_window(self):
        """
        create_window creates a new tkinter window including basic setup
        """
        
        # Main tkinter window
        self.root = tkinter.Tk()
        
        # Window Setup
        self.root.title("Image Filters")
        self.root.geometry("800x400")
        
        logger.debug("Successfully created a new window.")

    def create_menu(self):
        """
        create_menu creates the menu and submenus inside of it
        """
        
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        
        logger.debug("Successfully created the base menu.")
        
        # File Menu
        self.fileMenu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="File", menu = self.fileMenu)
        self.fileMenu.add_command(
                label="Open", 
                command = self.open_dialog
                )
        self.fileMenu.add_command(
                label="Save", 
                command = self.dummy
                )
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
                label="Quit", 
                command = self.close_window
                )
        
        logger.debug("Successfully created the File menu.")
        
        # Help Menu
        self.helpMenu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        
        logger.debug("Successfully created the Help menu.")

    # Opens an open_dialog allowing users to select a file they want to open
    def open_dialog(self):
        """
        open_dialog creates a new window allowing the user to get the filepath of the file they want to open
        """
        
        self.root.filename = filedialog.askopenfilename(
            initialdir="/", 
            title = "Select a File", 
            filetypes=(
                    ("Png files", "*.png"), 
                    ("Jpg files", "*jpg"), 
                    ("All files", "*.*")
                    )
            )
        
        logger.debug(f"Successfully acquired the filepath: {self.root.filename}")
        
        if len(self.root.filename) > 0:
            ip.load_image(self.root.filename)

    def close_window(self):
        """
        close_window destroys the tkinter window and closes the program
        """
        
        logger.debug("User selected Quit from the File menu. Quitting program.")
        
        # Destroys window and closes program
        self.root.destroy()

"""
Image Processor
"""

class ImageProcessor:
    
    def __init__(self):
        
        self.welcome_image()
    
    def welcome_image(self):
        """
        welcome_image creates a new canvas and updates it with the welcome image
        """        
        # Welcome image path
        self.image = cv2.imread("welcome.png")
        
        # Get image dimensions
        height, width, no_channels = self.image.shape
        
        # Create canvas to fit the image
        self.canvas = tkinter.Canvas(g.root, width = width, height = height)
        self.canvas.grid(row=2, column=0, columnspan=3)
        
        # Convert from BGR to RGB, then to PhotoImage
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(self.image)
        self.image = ImageTk.PhotoImage(self.image)
        
        # Create an image on the canvas
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        
        # Change window size to match picture
        g.root.geometry(f"{width}x{height}")
        
        logger.debug("Successfully created a canvas and loaded Welcome image.")
        
    def create_sliders(self):
        """
        create_sliders adds some sliders for image modification and lays them out in a grid
        """
        
        # TODO: Resize Sliders when window resizes & set size as fraction of window size
        
        # Brightness Slider
        self.brightness = tkinter.Scale(
                g.root, 
                from_=0, 
                to=100, 
                label="Brightness",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.update_image
                )
        # Sets Brightness to 50 to start
        self.brightness.set(50)
        
        # Contrast Slider
        self.contrast = tkinter.Scale(
                g.root, 
                from_=1, 
                to=100, 
                label="Contrast",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.update_image
                )        
        
        # Grayscale Slider
        self.grayscale = tkinter.Scale(
                g.root, 
                from_=0, 
                to=1, 
                label="Grayscale",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.update_image
                )     
        
        # Filters Slider
        self.filters = tkinter.Scale(
                g.root, 
                from_=1, 
                to=len(Kernels.k_array)-1, 
                label="Filters",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.update_image
                )      
        
        self.filter_label = tkinter.Label(
                g.root,
                text="Current filter:"
                )
        
        logger.debug("Successfully created sliders and label.")
        
        # Put all the sliders in their grid spots
        self.brightness.grid(row=0, column=0, sticky=tkinter.W)
        self.contrast.grid(row=1, column=0, sticky=tkinter.W)
        self.grayscale.grid(row=0, column=1, sticky=tkinter.W)
        self.filters.grid(row=1, column=1, sticky=tkinter.W)
        
        # Put the labels in their grid spots
        self.filter_label.grid(row=0, column=2, sticky=tkinter.W)
        
        logger.debug("Successfully packed sliders and label into grid.")

    def load_image(self, path):
        """
        load_image loads whichever filepath was selected in open_dialog
        """
        
        # TODO: Put a try catch here to catch failed image opens
        
        # OpenCV Test
        # Load image
        print(path)
        self.color_original = cv2.imread(path)
        
        logger.debug(f"Successfully read image from the filepath: {path}")
                
        # Converts to grayscale and saves as gray_original variable
        self.gray_original = cv2.cvtColor(self.color_original, cv2.COLOR_BGR2GRAY)
        
        logger.debug("Successfully created gray_original image.")
        
        # Create sliders
        self.create_sliders()
        
        # Get new image dimensions
        height, width, no_channels = self.color_original.shape
        
        # Load PhotoImage into existing canvas        
        self.image = cv2.cvtColor(self.color_original, cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(self.image)
        self.image = ImageTk.PhotoImage(self.image)
        
        logger.debug("Successfully created PhotoImage.")
        
        self.canvas.config(width = width, height = height)
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        g.root.geometry(f"{width}x{height}")

        logger.debug("Successfully created an image on the canvas, and changed window size.")

    def update_canvas():
        pass

    def update_image(self, var):
        """
        update_image modifies the image based on slider values
        """
        
        self.current_grayscale = self.grayscale.get()
        
        # Display color or gray original
        if self.current_grayscale == 0:
            # Load PhotoImage into existing canvas        
            self.image = cv2.cvtColor(self.color_original, cv2.COLOR_BGR2RGB)
            self.image = Image.fromarray(self.image)
            self.image = ImageTk.PhotoImage(self.image)
            
            logger.debug("Successfully created PhotoImage.")
            
            self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
    
            logger.debug("Successfully created an image on the canvas, and changed window size.")
        else:
            # Load PhotoImage into existing canvas        
            self.image = cv2.cvtColor(self.gray_original, cv2.COLOR_GRAY2RGB)
            self.image = Image.fromarray(self.image)
            self.image = ImageTk.PhotoImage(self.image)
            
            logger.debug("Successfully created PhotoImage.")
            
            self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
    
            logger.debug("Successfully created an image on the canvas, and changed window size.")            
            
        
        
"""
Basic setup and class initialization
"""

# Logger Setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s, -%(levelname)s : %(message)s')
file_handler = logging.FileHandler('Logs/logs.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create GUI object
g = Gui()

# Starts the image processor
ip = ImageProcessor()

# Tkinter main loop
g.root.mainloop()




    
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
cv2.createTrackbar('contrast', 'Image Filters', 1, 100, g.dummy)
# Brightness Trackbar - initial value is 50 to compensate for negative brightness (cv doesn't allow negative values)
cv2.createTrackbar('brightness', 'Image Filters', 50, 100, g.dummy)
# Filter Trackbar
cv2.createTrackbar('filters', 'Image Filters', 0, len(Kernels.k_array)-1, g.dummy)
# Grayscale Trackbar - switch only: values 0 & 1.
cv2.createTrackbar('grayscale', 'Image Filters', 0, 1, g.dummy)

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
    color_modified = cv2.filter2D(color_original, -1, Kernels.k_array[kernel_idx])
    gray_modified = cv2.filter2D(gray_original, -1, Kernels.k_array[kernel_idx])
    
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
            cv2.imwrite('Output\output-{}.png'.format(count), color_modified)
        else:
            cv2.imwrite('Output\output-{}.png'.format(count), gray_modified)
        
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
