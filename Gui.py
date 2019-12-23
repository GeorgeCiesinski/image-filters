# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:06:11 2019

@author: georg
"""

import os
import subprocess
import webbrowser
import tkinter
import Kernels
from tkinter import filedialog
from tkinter import messagebox


class Gui:
    
    """
    tkinter GUI
    """
    
    def __init__(self, ip, logger):
        
        # Logger instance from app.py
        self.logger = logger
        
        # Image Processor instance
        self.ip = ip
        
        # Create the window
        self.create_window()
        
        # Creates the menu bar
        self.create_menu()
        
        # List of filetypes compatible with OpenCV
        self.file_types = [
                ".bmp",
                ".dib",
                ".jpeg",
                ".jpg",
                ".jpe",
                ".png",
                ".pbm",
                ".pgm",
                ".ppm",
                ".sr",
                ".ras",
                ".tiff",
                ".tif",
                ]
    
    def create_window(self):
        
        """
        create_window creates a new tkinter window including basic setup
        """
        
        # TODO: When window resizes, resize all widgets. Prevent window from becoming too small
        
        # Main tkinter window
        self.root = tkinter.Tk()
        
        # Window Setup
        self.root.title("Image Filters")
        self.root.geometry("400x400")
        
        self.logger.debug("Successfully created a new window.")

    def initial_geometry(self):
        """
        initial_geometry changes the window geometry to match image
        """
        
        # Get image dimensions
        self.image_height, self.image_width, no_channels = self.ip.color_original.shape
        
        # Update canvas size
        self.canvas.config(width = self.image_width, height = self.image_height)
        
        # Calculate initial root geometry
        if self.image_width < 500:
            self.i_width = 500
        else:
            self.i_width = self.image_width
        self.i_height = self.image_height + 150
        
        # Change window size to match image
        self.root.geometry(f"{self.i_width}x{self.i_height}")
        
        self.logger.debug(f"The initial window size is: height - {self.i_height}, width - {self.i_width}.")
        
        # Binds window size to resize_image function
        self.root.bind('<Configure>', self.resize_image)
    
    def resize_image(self, event = None):
        """
        resize_image resizes the canvas and photoImage whenever the root window is resized
        """
        
        # Get new window height
        self.n_width = self.root.winfo_width()
        self.n_height = self.root.winfo_height()
        
        # Calculate difference between old window and new window
        self.width_diff = self.n_width - self.i_width
        self.height_diff = self.n_height - self.i_height
        
        # Create a new image with the new size
        self.new_image_height = self.image_height + self.height_diff
        self.new_image_width = int((self.new_image_height * self.image_width) / self.image_height)
        
        # Asks image processor to resize image using cv2
        self.ip.resize_and_update()

    def create_menu(self):
        
        """
        create_menu creates the menu and submenus inside of it
        """
        
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        
        self.logger.debug("Successfully created the base menu.")
        
        # File Menu
        self.fileMenu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", underline=0, menu = self.fileMenu)
        self.fileMenu.add_command(
                label="Open", 
                underline=0,
                command=self.open_dialog,
                accelerator="Ctrl+O"
                )
        self.fileMenu.add_command(
                label="Save", 
                underline=0,
                command=self.save_dialog,
                accelerator="Ctrl+S"
                )
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
                label="Quit", 
                underline=0,
                command=self.close_window,
                accelerator="Ctrl+Q"
                )
        
        self.logger.debug("Successfully created the File menu.")
        
        # Help Menu
        self.helpMenu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(
                label="How to use",
                underline=0,
                command=self.how_to,
                accelerator="Ctrl+H"
                )
        self.helpMenu.add_command(
                label="Open Logs Folder",
                command=self.show_logs
                )
        self.helpMenu.add_command(
                label="Repository & Documentation",
                command=self.repo_docs
                )
        
        # Shortcuts for menu options
        self.root.bind_all("<Control-o>", self.open_dialog)
        self.root.bind_all("<Control-s>", self.save_dialog)
        self.root.bind_all("<Control-q>", self.close_window)
        self.root.bind_all("<Control-h>", self.how_to)
        
        self.logger.debug("Successfully created the Help menu.")

    def create_canvas(self):
        """
        create_canvas initially creates the canvas used by this program
        """
        
        self.canvas = tkinter.Canvas(self.root, width = self.ip.orig_width, height = self.ip.orig_height)
        self.canvas.grid(row=2, column=0, columnspan=3, sticky = tkinter.NSEW)

    def update_canvas(self, image):
        """
        update_canvas updates the canvas with the image sent to this method
        """
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=image, anchor=tkinter.NW)

    def create_sliders(self):
        
        """
        create_sliders adds some sliders for image modification and lays them out in a grid
        """
        
        # Brightness Slider
        self.brightness = tkinter.Scale(
                self.root, 
                from_=0, 
                to=100, 
                label="Brightness",
                orient=tkinter.HORIZONTAL,
                command=self.ip.modify_image
                )
        # Sets Brightness to 50 to start
        self.brightness.set(50)
        
        # Contrast Slider
        self.contrast = tkinter.Scale(
                self.root, 
                from_=1, 
                to=100, 
                label="Contrast",
                orient=tkinter.HORIZONTAL,
                command=self.ip.modify_image
                )        
        
        # Grayscale Slider
        self.grayscale = tkinter.Scale(
                self.root, 
                from_=0, 
                to=1, 
                label="Grayscale",
                orient=tkinter.HORIZONTAL,
                command=self.ip.modify_image
                )     
        
        # Filters Slider
        self.filters = tkinter.Scale(
                self.root, 
                from_=0, 
                to=len(Kernels.k_array)-1, 
                label="Filters",
                orient=tkinter.HORIZONTAL,
                command=self.ip.modify_image
                )
        
        # Kernel Labels
        self.filter_label = tkinter.Label(
                self.root,
                text="Current Convolution Filter:",
                font=("Segoe UI", 12)
                )
        
        self.filter_name_label = tkinter.Label(
                self.root,
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
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight =1)
        
        self.logger.debug("Successfully packed sliders and label into grid.")

    def open_dialog(self, event=None):
        
        """
        open_dialog creates a new window allowing the user to get the filepath of the file they want to open
        """
        
        self.logger.debug("User has opened the open_dialog.")
        
        try:
            full_path = filedialog.askopenfilename(
                initialdir="/", 
                title = "Select a File", 
                filetypes=(
                        ("All files", "*.*"),
                        (".bmp files", "*.bmp"),
                        (".jpg files", "*jpg"), 
                        (".png files", "*.png"), 
                        (".tiff files", "*.tiff")
                        )
                )
        except:
            self.logger.exception(f"Failed to acquire the filepath: {full_path}")
            raise
        else:
            self.logger.debug(f"Successfully acquired the filepath: {full_path}")
        
        # Split filename & extension
        filename, file_extension = os.path.splitext(full_path)
        
        self.logger.debug(f"Extension: {file_extension}")
        
        # Checks if file is compatible with OpenCV
        if file_extension in self.file_types:
        
            # Check if filepath is returned
            if len(full_path) > 0:
                
                # Calls ip.load_image to open the specified image file
                self.logger.debug("Calling ip.load_image.")
                self.ip.load_image(full_path)
                
        else:
            
            self.logger.debug(f"An incompatible extension was specified: {file_extension}. Failed to open file.")
            
            # Calls wrong_format method which instructs the user on correct usage
            self.wrong_format()
            

    def save_dialog(self, event=None):
        
        """
        save_dialog creates a new window allowing user to specify the save file path for the modified file
        """
        
        # TODO: Make sure user specified a file extension. Pop up message box advising to use an available extension
        
        self.logger.debug("User has opened the save_dialog.")
        
        #Check if a file has actually been opened        
        if self.ip.image_opened == False:
            
            # Warn user that there is no file open and file cannot be saved
            messagebox.showinfo("Image Filters: Unable to save file", "There is no file to save. Please open and modify a file first.")
        
        else: 
        
            try: 
                # Ask user to select file save location
                full_path = filedialog.asksaveasfilename(
                    initialdir="/",
                    title="Save file",
                    filetypes=(
                            ("All files", "*.*"),
                            (".bmp files", "*.bmp"),
                            (".jpg files", "*jpg"), 
                            (".png files", "*.png"), 
                            (".tiff files", "*.tiff")
                            )
                    )
            except:
                self.logger.exception(f"Failed to acquire the save path: {full_path}")
                raise
            else:
                self.logger.debug(f"Successfully acquired the save path: {full_path}")
                
                # Split filename & extension
                filename, file_extension = os.path.splitext(full_path)
                
                self.logger.debug(f"Extension: {file_extension}")
                
                # Checks if file_extension is compatible with OpenCV
                if file_extension in self.file_types:
            
                    # Calls ip.save_image to save the image at specified path
                    self.logger.debug("Calling ip.save_image.")
                    self.ip.save_image(full_path)
                    
                else:
            
                    self.logger.debug(f"An incompatible extension was specified: {file_extension}. Failed to save file.")
                    
                    # Calls wrong_format method which instructs the user on correct usage
                    self.wrong_format()
    
    def wrong_format(self):
        
        format_instructions = """You have tried to open or save a file using an incompatible format.

Image-Filters is compatible with the below formats: 
    
Windows Bitmaps: .bmp, .dib
JPEG Files: .jpeg, .jpg, .jpe
Portable Network Graphics: .png
Portable Image Format: .pbm, .pgm, .ppm
Sun Rasters: .sr, .ras
TIFF Files: .tiff, .tif

When opening images, please make sure that they are one of these formats as other formats are not guaranteed to work. 

When saving images, please include one of these file extensions in the filename to ensure the file is saved.
"""
        
        tkinter.messagebox.showinfo("Incorrect Format", format_instructions)
        
    def close_window(self, event=None):
        
        """
        close_window destroys the tkinter window and closes the program
        """
        
        self.logger.debug("User selected Quit from the File menu. Quitting program.")
        
        # Destroys window and closes program
        self.root.destroy()
        
    def how_to(self, event=None):
        
        """
        Shows a how to use screen in a message box
        """
        
        how_to_instructions = """HOW TO USE:
            
1. Open a file using File > Open, or Ctrl+O
2. Modify image using sliders
3. Save modified file using File > Save, or Ctrl+S
4. Close the program using File > Quit, or Ctrl+Q

In case of any bugs, export the logs and submit them as a bug at the repository which can be found by clicking: 

Help > Repository & Documentation.
"""
        
        tkinter.messagebox.showinfo("Instructions", how_to_instructions)

    def show_logs(self):
        """
        show_dir opens the Logs/ directory in Windows Explorer
        """
        
        # Logs folder
        log_folder = "Logs\\"
        
        # Get the current working directory
        current_directory = os.getcwd()
        
        # Combine into Log Directory
        log_directory = os.path.join(current_directory, log_folder)
        
        # Open directory in windows explorer
        subprocess.Popen(f'explorer {log_directory}')
        
        
    def repo_docs(self):
        
        """
        repo_docs opens a new window advising user that they are about to visit the repository link.
        If the user clicks yes, it goes to url and closes window. If they click no, it simply closes
        the window.
        """
        
        # TODO: Improve the look of the window
    
        # Repository URL
        self.repo_url = "https://github.com/GeorgeCiesinski/image-filters"
    
        # Create new window
        self.links = tkinter.Tk()
        
        # Window Setup
        self.links.title("Repository & Documentation")
        self.links.geometry("320x150")
        
        # Create Labels
        self.open_link_label = tkinter.Label(
                self.links,
                text="You are about to open the project repository link:"
                )
        self.link_url_label = tkinter.Label(
                self.links,
                text=self.repo_url
                )
        self.empty = tkinter.Label(
                self.links,
                text=""
                )
        
        # Create Buttons
        self.yes_button = tkinter.Button(
                self.links,
                text="YES",
                width=6,
                height=1,
                bd=4,
                command=self.open_link
                )
        self.no_button = tkinter.Button(
                self.links,
                text="NO",
                width=6,
                height=1,
                bd=4,
                command=self.close_links_window
                )
        
        # Pack widgets into Window
        # Labels
        self.open_link_label.grid(row=1, column=0, columnspan=3)
        self.link_url_label.grid(row=2, column=0, columnspan=3)
        self.empty.grid(row=3, column=0, columnspan=3)
        # Buttons
        self.yes_button.grid(row=4, column=0)
        self.no_button.grid(row=4, column=2)
    
    def open_link(self):
        
        # Opens link after user presses yes. Opens as a tab and raises the window
        webbrowser.open(self.repo_url, new=0, autoraise=True)
        
        # Calls function to close window
        self.close_links_window()
    
    def close_links_window(self):
        
        # Closes Repository & Documentation window
        self.links.destroy()