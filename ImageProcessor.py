# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:30:01 2019

@author: georg
"""

"""
Image Processor
"""

import cv2
import tkinter
from Kernels import Kernels
import numpy as np
from PIL import Image
from PIL import ImageTk

class ImageProcessor:
    
    def __init__(self, logger):
        
        # Logger
        self.logger = logger
    
    def welcome_image(self, g):
        
        """
        welcome_image creates a new canvas and updates it with the welcome image
        """
        
        # Gui instance
        self.g = g
                
        # Welcome image path
        self.image = cv2.imread("welcome.png")
        
        # Get image dimensions
        height, width, no_channels = self.image.shape
        
        # Create canvas to fit the image
        self.canvas = tkinter.Canvas(self.g.root, width = width, height = height)
        self.canvas.grid(row=2, column=0, columnspan=3)
        
        # Convert to PhotoImage and update canvas
        self.update_canvas_color(self.image)
        
        # Creates image opened variable
        self.image_opened = False
        
        self.logger.debug("Successfully created a canvas and loaded Welcome image.")
        
    def create_sliders(self):
        
        """
        create_sliders adds some sliders for image modification and lays them out in a grid
        """
        
        # TODO: Resize Sliders when window resizes & set size as fraction of window size
        
        # Brightness Slider
        self.brightness = tkinter.Scale(
                self.g.root, 
                from_=0, 
                to=100, 
                label="Brightness",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.modify_image
                )
        # Sets Brightness to 50 to start
        self.brightness.set(50)
        
        # Contrast Slider
        self.contrast = tkinter.Scale(
                self.g.root, 
                from_=1, 
                to=100, 
                label="Contrast",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.modify_image
                )        
        
        # Grayscale Slider
        self.grayscale = tkinter.Scale(
                self.g.root, 
                from_=0, 
                to=1, 
                label="Grayscale",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.modify_image
                )     
        
        # Filters Slider
        self.filters = tkinter.Scale(
                self.g.root, 
                from_=0, 
                to=len(Kernels.k_array)-1, 
                label="Filters",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.modify_image
                )      
        
        # TODO: Make label text larger and easier to read.
        
        # Kernel Labels
        self.filter_label = tkinter.Label(
                self.g.root,
                text="Current Convolution Filter:"
                )
        
        self.filter_name_label = tkinter.Label(
                self.g.root,
                text=""
                )
        
        self.logger.debug("Successfully created sliders and label.")
        
        # Put all the sliders in their grid spots
        self.brightness.grid(row=0, column=0, sticky=tkinter.W)
        self.contrast.grid(row=1, column=0, sticky=tkinter.W)
        self.grayscale.grid(row=0, column=1, sticky=tkinter.W)
        self.filters.grid(row=1, column=1, sticky=tkinter.W)
        
        # Put the labels in their grid spots
        self.filter_label.grid(row=0, column=2, sticky=tkinter.W)
        self.filter_name_label.grid(row=1, column=2, sticky=tkinter.W)
        
        self.logger.debug("Successfully packed sliders and label into grid.")

    def load_image(self, path):
        
        """
        load_image loads whichever filepath was selected in open_dialog
        """

        # Load image
        print(path)
        
        try:
        
            self.color_original = cv2.imread(path)
        
        except:
            
            self.logger.debug(f"Failed to open the image from the path: {path}")
            raise
            
        else:
            
            self.logger.debug(f"Successfully read image from the filepath: {path}")
            # Sets image_opened to True
            self.image_opened = True
                
        # Converts to grayscale and saves as gray_original variable
        self.gray_original = cv2.cvtColor(self.color_original, cv2.COLOR_BGR2GRAY)
        
        self.logger.debug("Successfully created gray_original image.")
        
        # Create sliders
        self.create_sliders()
        
        self.modify_image(self.color_original)

    def save_image(self, path):
        
        """
        Save an image to the specified path
        """
        
        if self.current_grayscale == 0:
            
            try:
                cv2.imwrite(path, self.color_modified)
            except:
                self.logger.debug(f"Failed to save color_modified to {path}")
            else:
                self.logger.debug(f"Successfully saved color_modified to {path}")    
        
        else: 
            try:
                cv2.imwrite(path, self.gray_modified)
            except:
                self.logger.debug(f"Failed to save gray_modified to {path}")
            else:
                self.logger.debug(f"Successfully saved gray_modified to {path}")

    def modify_image(self, var):
        
        """
        update_image modifies the image based on slider values
        """
        
        # Get trackbar values
        self.get_trackbars()
        
        # Apply kernels
        self.apply_kernels()
        
        # Apply brightness and contrast
        self.apply_brightness_contrast()
        
        # Display color or gray original
        if self.current_grayscale == 0:
            self.update_canvas_color(self.color_modified)
        else:
            self.update_canvas_gray(self.gray_modified)    

    def get_trackbars(self):
        
        """
        Gets the trackbar values
        """
        
        # Brightness
        self.current_brightness = self.brightness.get()
        
        # Contrast
        self.current_contrast = self.contrast.get()
        
        # Grayscale
        self.current_grayscale = self.grayscale.get()

        # Filters
        self.current_filters = self.filters.get()
        
    def apply_kernels(self):
        
        """
        Applies the kernels to image
        """
        
        kernel_idx = self.current_filters
        
        # apply the filters
        self.color_kernel = cv2.filter2D(self.color_original, -1, Kernels.k_array[kernel_idx])
        self.gray_kernel = cv2.filter2D(self.gray_original, -1, Kernels.k_array[kernel_idx])
        
        self.filter_name_label.configure(text=Kernels.k_name[self.current_filters])
        
    def apply_brightness_contrast(self):
        
        """
        Apply the brightness and contrast
        dst = cv2.addWeighted(src1, alpha, src2, beta, gamma)
        dst = cv2.addWeighted(image, contrast, zeros_image, 0, brightness) || src2 must be image of 0's, so we use np.zeros_like to do this
        """
        
        # Applies brightness and contrast to color image
        self.color_modified = cv2.addWeighted(
                self.color_kernel, 
                self.current_contrast, 
                np.zeros_like(self.color_original), 
                0, 
                self.current_brightness - 50
                )
        
        # Applies brightness and contrast to gray image
        self.gray_modified = cv2.addWeighted(
                self.gray_kernel, 
                self.current_contrast, 
                np.zeros_like(self.gray_original), 
                0, 
                self.current_brightness - 50)
        

    def update_canvas_color(self, color_image):
        
        """
        update_canvas_color converts BGR to RGB and then PhotoImage before displaying on canvas
        """
        
        # Get image dimensions
        height, width, no_channels = color_image.shape
        
        # Update canvas size
        self.canvas.config(width = width, height = height)
        
        # Change window size to match image
        self.g.root.geometry(f"{width}x{height}")
        
        # Convert from BGR to RGB, then to PhotoImage
        self.color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.color_image = Image.fromarray(self.color_image)
        self.color_image = ImageTk.PhotoImage(self.color_image)
        
        # Create an image on the canvas
        self.canvas.create_image(0, 0, image=self.color_image, anchor=tkinter.NW)

    def update_canvas_gray(self, gray_image):
        
        """
        update_canvas_gray converts Gray to RGB and then PhotoImage before displaying on canvas
        """
        
        # Convert from BGR to RGB, then to PhotoImage
        self.color_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        self.color_image = Image.fromarray(self.color_image)
        self.color_image = ImageTk.PhotoImage(self.color_image)
        
        # Create an image on the canvas
        self.canvas.create_image(0, 0, image=self.color_image, anchor=tkinter.NW)