# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:30:01 2019

@author: georg
"""

"""
Image Processor
"""

import cv2
import Kernels
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
        
        # Get original image dimensions
        self.orig_height, self.orig_width, no_channels = self.image.shape
        
        # Create canvas
        self.g.create_canvas()
        
        # Convert to PhotoImage and update canvas
        self.update_canvas_color(self.image)
        
        # Indicates this is welcome image and that an actual image hasn't been opened
        self.image_opened = False
        
        self.logger.debug("Successfully created a canvas and loaded Welcome image.")

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
        
    # TODO: Update this to reflect geometry method in GUI
        # Sets original window geometry
        self.g.initial_geometry()
        
        # Converts to grayscale and saves as gray_original variable
        self.gray_original = cv2.cvtColor(self.color_original, cv2.COLOR_BGR2GRAY)
        
        self.logger.debug("Successfully created gray_original image.")
        
        # Create sliders
        self.g.create_sliders()
        
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

        # Checks current image size selection and updates canvas (ensures image doesn't unintentionally resize during modification)
        self.g.resize_image()

    def get_trackbars(self):
        
        """
        Gets the trackbar values
        """
        
        # Brightness
        self.current_brightness = self.g.brightness.get()
        
        # Contrast
        self.current_contrast = self.g.contrast.get()
        
        # Grayscale
        self.current_grayscale = self.g.grayscale.get()

        # Filters
        self.current_filters = self.g.filters.get()
        
    def apply_kernels(self):
        
        """
        Applies the kernels to image
        """
        
        kernel_idx = self.current_filters
        
        # apply the filters
        self.color_kernel = cv2.filter2D(self.color_original, -1, Kernels.k_array[kernel_idx])
        self.gray_kernel = cv2.filter2D(self.gray_original, -1, Kernels.k_array[kernel_idx])
        
        self.g.filter_name_label.configure(text=Kernels.k_name[self.current_filters])
        
    def apply_brightness_contrast(self):
        
        """
        Apply the brightness and contrast to color_kernel and gray_kernel images
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
    # TODO: Put this in a try catch to avoid conversion fails
        # Convert from BGR to RGB, then to PhotoImage
        self.color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.color_image = Image.fromarray(self.color_image)
        self.color_image = ImageTk.PhotoImage(self.color_image)
        
        # Create an image on the canvas
        self.g.update_canvas(self.color_image)

    def update_canvas_gray(self, gray_image):
        
        """
        update_canvas_gray converts Gray to RGB and then PhotoImage before displaying on canvas
        """
    # TODO: Put this in a try catch to avoid conversion fails
        # Convert from BGR to RGB, then to PhotoImage
        self.gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        self.gray_image = Image.fromarray(self.gray_image)
        self.gray_image = ImageTk.PhotoImage(self.gray_image)
        
        # Create an image on the canvas
        self.g.update_canvas(self.gray_image)
        
    def resize_and_update(self):
        
        # Resize color and gray images
        self.color_resized = cv2.resize(self.color_modified, (self.g.new_image_width, self.g.new_image_height))
        self.gray_resized = cv2.resize(self.gray_modified, (self.g.new_image_width, self.g.new_image_height))
        
        # Display color or gray original
        if self.current_grayscale == 0:
            self.update_canvas_color(self.color_resized)
        else:
            self.update_canvas_gray(self.gray_resized)    