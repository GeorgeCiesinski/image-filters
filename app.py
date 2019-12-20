# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:37:51 2019

@author: George Ciesinski
"""

import logging
from logging import handlers
from Gui import Gui
from ImageProcessor import ImageProcessor
from os import path

def on_closing():
    """
    Closes program if user clicks x button on the window
    """
    
    g.root.destroy()
        

"""
Basic setup and class initialization
"""

# Logger Setup

# Basic settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s -%(levelname)s : %(message)s')

# Rotating File Handler creates 5 backups on top of the current logs
rollover_check = path.exists('Logs/logs.log')
file_handler = handlers.RotatingFileHandler('Logs/logs.log', mode='w', maxBytes=10000, backupCount=5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Every time program is ran, check if log exists, rollover if yes
if rollover_check:    
    file_handler.doRollover()

# Starts the image processor
ip = ImageProcessor(logger)

# Create GUI object
g = Gui(ip, logger)

# Put up welcome image, includes GUI instance
ip.welcome_image(g)

# Close program if window is destroyed
g.root.protocol("WM_DELETE_WINDOW", on_closing)

# Tkinter main loop
g.root.mainloop()
