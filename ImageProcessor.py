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
        ---
        Tkinter init configurations should happen here and not __init__
        """
        
        # Gui instance
        self.g = g
                
        # Welcome image path
        self.image = cv2.imread("welcome.png")
        
        # Get image dimensions
        height, width, no_channels = self.image.shape
        
        # Create canvas to fit the image
        self.canvas = tkinter.Canvas(self.g.root, width = width, height = height)
        self.canvas.grid(row=2, column=0, columnspan=3, sticky = tkinter.NSEW)
        
        # Convert to PhotoImage and update canvas
        self.update_canvas_color(self.image)
        
        # Indicates this is welcome image and that an actual image hasn't been opened
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
                orient=tkinter.HORIZONTAL,
                command=self.modify_image
                )        
        
        # Grayscale Slider
        self.grayscale = tkinter.Scale(
                self.g.root, 
                from_=0, 
                to=1, 
                label="Grayscale",
                orient=tkinter.HORIZONTAL,
                command=self.modify_image
                )     
        
        # Filters Slider
        self.filters = tkinter.Scale(
                self.g.root, 
                from_=0, 
                to=len(Kernels.k_array)-1, 
                label="Filters",
                orient=tkinter.HORIZONTAL,
                command=self.modify_image
                )      
        
        # TODO: Make label text larger and easier to read.
        
        # Kernel Labels
        self.filter_label = tkinter.Label(
                self.g.root,
                text="Current Convolution Filter:",
                font=("Segoe UI", 12)
                )
        
        self.filter_name_label = tkinter.Label(
                self.g.root,
                text="",
                font=("Segoe UI", 16)
                )
        
        self.logger.debug("Successfully created sliders and label.")
        
        # Put all the sliders in their grid spots
        self.brightness.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.contrast.grid(row=1, column=0, sticky=tkinter.NSEW)
        self.grayscale.grid(row=0, column=1, sticky=tkinter.NSEW)
        self.filters.grid(row=1, column=1, sticky=tkinter.NSEW)
        
        # Put the labels in their grid spots
        self.filter_label.grid(row=0, column=2, sticky=tkinter.NSEW)
        self.filter_name_label.grid(row=1, column=2, sticky=tkinter.NSEW)
        
        # Configures grid with a weight
        self.g.root.grid_columnconfigure(0, weight=1)
        self.g.root.grid_columnconfigure(1, weight=1)
        self.g.root.grid_columnconfigure(2, weight=1)
        self.g.root.grid_rowconfigure(0, weight=0)
        self.g.root.grid_rowconfigure(1, weight=0)
        self.g.root.grid_rowconfigure(2, weight =1)
        
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
         
        # Sets original window geometry
        self.initial_geometry()
        
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
        
    def initial_geometry(self):
        """
        initial_geometry changes the window geometry to match image
        """
        
        # Get image dimensions
        self.image_height, self.image_width, no_channels = self.color_original.shape
        
        # Update canvas size
        self.canvas.config(width = self.image_width, height = self.image_height)
        
        # Calculate initial root geometry
        if self.image_width < 500:
            self.i_width = 500
        else:
            self.i_width = self.image_width
        self.i_height = self.image_height + 150
        
        # Change window size to match image
        self.g.root.geometry(f"{self.i_width}x{self.i_height}")
        
        self.logger.debug(f"The initial window size is: height - {self.i_height}, width - {self.i_width}.")
        
        # Binds window size to resize_image function
        self.g.root.bind('<Configure>', self.resize_image)
        
    def resize_image(self, event = None):
        """
        resize_image resizes the canvas and photoImage whenever the root window is resized
        """
        
        # Get new window height
        self.n_width = self.g.root.winfo_width()
        self.n_height = self.g.root.winfo_height()
        
        # Calculate difference between old window and new window
        self.width_diff = self.n_width - self.i_width
        self.height_diff = self.n_height - self.i_height
        
        print(f"The difference is:: width : {self.width_diff}, height : {self.height_diff}.")
        
        self.new_image_width = self.image_width + self.width_diff
        self.new_image_height = self.image_height + self.height_diff
        
        self.color_resized = cv2.resize(self.color_modified, (self.new_image_width, self.new_image_height))
        self.gray_resized = cv2.resize(self.gray_modified, (self.new_image_width, self.new_image_height))
        
        # Display color or gray original
        if self.current_grayscale == 0:
            self.update_canvas_color(self.color_resized)
        else:
            self.update_canvas_gray(self.gray_resized)
        
    def update_canvas_color(self, color_image):
        
        """
        update_canvas_color converts BGR to RGB and then PhotoImage before displaying on canvas
        """
        
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