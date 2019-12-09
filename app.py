# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:37:51 2019

@author: George Ciesinski
"""

import cv2
import numpy as np
import tkinter
from tkinter import filedialog
from tkinter import messagebox
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
    
    k_name = [
            "Identity Kernel",
            "Sharpen Kernel",
            "Gaussian Kernel 1",
            "Gaussian Kernel 2",
            "Box Kernel",
            ]

class Gui:
    
    """
    tkinter GUI
    """
    
    # TODO: Create save dialog
    
    def __init__(self):
        
        # Create the window
        self.create_window()
        
        # Creates the menu bar
        self.create_menu()
        
    def dummy(self):
        pass
    
    def create_window(self):
        
        """
        create_window creates a new tkinter window including basic setup
        """
        
        # TODO: When window resizes, resize all widgets. Prevent window from becoming too small
        
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
        self.menu.add_cascade(label="File", underline=0, menu = self.fileMenu)
        self.fileMenu.add_command(
                label="Open", 
                underline=1,
                command=self.open_dialog,
                accelerator="Ctrl+O"
                )
        self.fileMenu.add_command(
                label="Save", 
                underline=1,
                command=self.save_dialog,
                accelerator="Ctrl+S"
                )
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
                label="Quit", 
                underline=1,
                command=self.close_window,
                accelerator="Ctrl+Q"
                )
        
        logger.debug("Successfully created the File menu.")
        
        # Help Menu
        self.helpMenu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(
                label="How to use",
                command=self.how_to
                )
        self.helpMenu.add_command(
                label="Export Logs",
                # TODO: Open log directory
                command=self.dummy
                )
        self.helpMenu.add_command(
                label="Repository & Documentation",
                # TODO: Link to repository
                command=self.dummy
                )
        
        logger.debug("Successfully created the Help menu.")

    # Opens an open_dialog allowing users to select a file they want to open
    def open_dialog(self):
        
        """
        open_dialog creates a new window allowing the user to get the filepath of the file they want to open
        """
        
        # TODO: Make sure file extension is valid
        # TODO: Change the options so that All Files is primary, and multiple extensions are listed onder each menu option
        
        logger.debug("User has opened the open_dialog.")
        
        try:
            self.root.filename = filedialog.askopenfilename(
                initialdir="/", 
                title = "Select a File", 
                filetypes=(
                        (".bmp files", "*.bmp"),
                        (".jpg files", "*jpg"), 
                        (".png files", "*.png"), 
                        (".tiff files", "*.tiff"),
                        ("All files", "*.*")
                        )
                )
        except:
            logger.exception(f"Failed to acquire the filepath: {self.root.filename}")
            raise
        else:
            logger.debug(f"Successfully acquired the filepath: {self.root.filename}")
        
        # TODO: Check to make sure filepath ends in compatible format extension
        
        if len(self.root.filename) > 0:
            
            # Calls ip.load_image to open the specified image file
            logger.debug("Calling ip.load_image.")
            ip.load_image(self.root.filename)

    def save_dialog(self):
        
        """
        save_dialog creates a new window allowing user to specify the save file path for the modified file
        """
        
        # TODO: Make sure user specified a file extension. Pop up message box advising to use an available extension
        # TODO: Automatically populate the file extension?
        
        logger.debug("User has opened the save_dialog.")
        
        #Check if a file has actually been opened        
        if ip.image_opened == False:
            
            # Warn user that there is no file open and file cannot be saved
            tkinter.messagebox.showinfo("Image Filters: Unable to save file", "There is no file to save. Please open and modify a file first.")
        
        else: 
        
            try: 
                # Ask user to select file save location
                self.root.savepath = filedialog.asksaveasfilename(
                    initialdir="/",
                    title="Save file",
                    filetypes=(
                            (".bmp files", "*.bmp"),
                            (".jpg files", "*jpg"), 
                            (".png files", "*.png"), 
                            (".tiff files", "*.tiff"),
                            ("All files", "*.*")
                            )
                    )
            except:
                logger.exception(f"Failed to acquire the save path: {self.root.filename}")
                raise
            else:
                logger.debug(f"Successfully acquired the save path: {self.root.filename}")
                
            # Calls ip.save_image to save the image at specified path
            logger.debug("Calling ip.save_image.")
            ip.save_image(self.root.savepath)
    
    def close_window(self):
        
        """
        close_window destroys the tkinter window and closes the program
        """
        
        logger.debug("User selected Quit from the File menu. Quitting program.")
        
        # Destroys window and closes program
        self.root.destroy()
        
    def how_to(self):
        
        """
        Shows a how to use screen in a message box
        """
        
        how_to_instructions = """HOW TO USE:
            
1. Open a file using File > Open, or Ctrl+O
2. Modify image using sliders
3. Save modified file using File > Save, or Ctrl+S

In case of any bugs, export the logs and submit them as a bug at the repository which can be found by clicking: 

Help > Repository & Documentation.
"""
        
        tkinter.messagebox.showinfo("Instructions", how_to_instructions)

    def export_logs(self):
        
        # TODO: Grab the latest few logs and zip them into a file on the desktop
        pass
        
    def repo_docs(self):
        
        # TODO: Create a new window, advise user they are about to go to the repository/documentation link and if they want to continue.
        # TODO: Close new window if no clicked. Close window and open link if yes clicked. 
        pass
    

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
        
        # TODO: Update welcome_image so that it looks more professional
        
        # Welcome image path
        self.image = cv2.imread("welcome.png")
        
        # Get image dimensions
        height, width, no_channels = self.image.shape
        
        # Create canvas to fit the image
        self.canvas = tkinter.Canvas(g.root, width = width, height = height)
        self.canvas.grid(row=2, column=0, columnspan=3)
        
        # Convert to PhotoImage and update canvas
        self.update_canvas_color(self.image)
        
        # Creates image opened variable
        self.image_opened = False
        
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
                command=self.modify_image
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
                command=self.modify_image
                )        
        
        # Grayscale Slider
        self.grayscale = tkinter.Scale(
                g.root, 
                from_=0, 
                to=1, 
                label="Grayscale",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.modify_image
                )     
        
        # Filters Slider
        self.filters = tkinter.Scale(
                g.root, 
                from_=0, 
                to=len(Kernels.k_array)-1, 
                label="Filters",
                length=400,
                orient=tkinter.HORIZONTAL,
                command=self.modify_image
                )      
        
        # TODO: Make label text larger and easier to read.
        # TODO: Replace second widget with some kind of input field or something.
        
        # Kernel Labels
        self.filter_label = tkinter.Label(
                g.root,
                text="Current Convolution Filter:"
                )
        
        self.filter_name_label = tkinter.Label(
                g.root,
                text=""
                )
        
        logger.debug("Successfully created sliders and label.")
        
        # Put all the sliders in their grid spots
        self.brightness.grid(row=0, column=0, sticky=tkinter.W)
        self.contrast.grid(row=1, column=0, sticky=tkinter.W)
        self.grayscale.grid(row=0, column=1, sticky=tkinter.W)
        self.filters.grid(row=1, column=1, sticky=tkinter.W)
        
        # Put the labels in their grid spots
        self.filter_label.grid(row=0, column=2, sticky=tkinter.W)
        self.filter_name_label.grid(row=1, column=2, sticky=tkinter.W)
        
        logger.debug("Successfully packed sliders and label into grid.")

    def load_image(self, path):
        
        """
        load_image loads whichever filepath was selected in open_dialog
        """
        
        # TODO: Put a try catch here to catch failed image opens
        
        # OpenCV Test
        # Load image
        print(path)
        
        try:
        
            self.color_original = cv2.imread(path)
        
        except:
            
            logger.debug(f"Failed to open the image from the path: {path}")
            raise
            
        else:
            
            logger.debug(f"Successfully read image from the filepath: {path}")
            # Sets image_opened to True
            self.image_opened = True
                
        # Converts to grayscale and saves as gray_original variable
        self.gray_original = cv2.cvtColor(self.color_original, cv2.COLOR_BGR2GRAY)
        
        logger.debug("Successfully created gray_original image.")
        
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
                logger.debug(f"Failed to save color_modified to {path}")
            else:
                logger.debug(f"Successfully saved color_modified to {path}")    
        
        else: 
            try:
                cv2.imwrite(path, self.gray_modified)
            except:
                logger.debug(f"Failed to save gray_modified to {path}")
            else:
                logger.debug(f"Successfully saved gray_modified to {path}")

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
        # TODO: Change to color_modified
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
        g.root.geometry(f"{width}x{height}")
        
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
        
        
"""
Basic setup and class initialization
"""

# Logger Setup
# TODO: Create several logs to track past several attempts to use app (5 - 10 tops)
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
