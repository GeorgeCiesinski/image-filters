# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:37:51 2019

@author: George Ciesinski
"""

import logging
from Gui import Gui
from ImageProcessor import ImageProcessor

        
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

# Starts the image processor
ip = ImageProcessor(logger)

# Create GUI object
g = Gui(ip, logger)

# Put up welcome image, includes GUI instance
ip.welcome_image(g)

# Tkinter main loop
g.root.mainloop()
