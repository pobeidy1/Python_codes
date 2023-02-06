 from skimage import io, img_as_ubyte
 import matplotlib.pyplot as plt
 import numpy as np
 from scipy import ndimage
 from skimage.filters import try_all_threshold 
 import skimage.filters as skfilt
 import skimage.measure as skmeas

def filteringIm_fun(img,sigma,correction_factor):
    #import image needs to be ubit uint16 or8
   
    uniform_filtered_img = ndimage.uniform_filter(img, size=5)
    #plt.imshow(uniform_filtered_img)
    
    #Gaussian filter: from scipy.ndimage
    # Gaussian filter smooths noise but also edges
    
    blurred_img = ndimage.gaussian_filter(img, sigma=sigma)  #also try 5, 7
    #plt.imshow('blurred img', blurred_img)
    
    #Median filter is better than gaussian. A non-local means is even better
    median_img = ndimage.median_filter(img, sigma)
    #plt.imshow(median_img)
    
    #Edge detection
    sobel_img = ndimage.sobel(img, axis=0)  #Axis along which to calculate sobel
    #plt.imshow(sobel_img)
    
   

    #fig, ax = try_all_threshold(img, figsize=(10, 8), verbose=False)
    #plt.show()

    selected_filter = skfilt.threshold_mean

    thresh_val =selected_filter (blurred_img)
    new_mask = blurred_img > (thresh_val+(correction_factor*thresh_val))
    
    mask_orig = new_mask
    new_mask = clear_border(new_mask)
    object_labels = skmeas.label(new_mask)
    
    masked_img = img*new_mask

    return uniform_filtered_img, blurred_img, median_img, sobel_img, object_labels, mask_orig, masked_img