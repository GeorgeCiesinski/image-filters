# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 19:59:29 2019

@author: georg
"""

import cv2
import numpy as np


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

# Averaging kernel (takes average of pixel values in the window)
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

# Kernel names (mirrors above array)
k_name = [
        "Identity Kernel",
        "Sharpen Kernel",
        "Gaussian Kernel 1",
        "Gaussian Kernel 2",
        "Box Kernel",
        ]