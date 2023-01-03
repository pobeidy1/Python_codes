#part2
from matplotlib.widgets import RectangleSelector
from skimage.measure import label, regionprops, regionprops_table
from scipy import ndimage
import cv2
import numpy as np 
import matplotlib.pylab as plt
from skimage.filters import try_all_threshold 
import pandas as pd
import warnings

warnings.filterwarnings('ignore')



def filter_img_func(image,select_method, automated="on"):   
    
    
    from skimage.filters import threshold_mean

    if automated=="on":
        thresh = threshold_mean(image)
    else: 
        #if neede one can change the threshhold value 
        thresh=800
    
    binary = image > thresh


    fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
    ax = axes.ravel()
    ax[0] = plt.subplot(1, 3, 1)
    ax[1] = plt.subplot(1, 3, 2)
    ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0])

    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].set_title('Original')
    ax[0].axis('off')

    ax[1].hist(image.ravel(), bins=256)
    ax[1].set_title('Histogram')
    ax[1].axvline(thresh, color='r')

    ax[2].imshow(binary, cmap=plt.cm.gray)
    ax[2].set_title('Thresholded')
    ax[2].axis('off')

    plt.show() 
    mask=binary

    return mask