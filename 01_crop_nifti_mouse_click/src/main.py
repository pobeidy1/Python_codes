func# -*- coding: utf-8 -*-
"""
Serarch subforders for nifti file 
Load and display an slice 
Crop the image using mouse click 
Return the final, cropped image at the end 

@author: pobe4699
"""
#clear all variable if you are using Spyder
from IPython import get_ipython;
get_ipython().magic('reset -sf')

import sys
import os
import pickle
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

# now we can import the module in the parent
# directory.
from utls.open_n_load_mag_qsm_2files import open_multi_file_full_path
from utls.whole_brain_mask import filter_img_func
from utls.click_n_crop import click_to_crop_img
from utls.open_n_load_mag_qsm_2files import load2corresponding_files
from utls.open_n_load_mag_qsm_2files import open_multi_file_full_path
from utls.a03_Multi_ROI_on_img_As_Func import draw_multi_ROIs_get_Stat

from scipy import ndimage as nd
from skimage.morphology import reconstruction

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import cv2




def loadfiles():
    all_filtered_mag_fNames_full_path, all_filtered_qsm_fNames_full_path = open_multi_file_full_path(
        file_extension)       # path_to_data

    title = 'Susceptibility MAP t1 vs t2'
    file1, file2 = load2corresponding_files(
        all_filtered_mag_fNames_full_path, 0)
    return file1, file2


def take_an_slice(file1, slice_nbr=108):
    s_nbr = slice_nbr
    image_rot = ndimage.rotate(np.take(file1, slice_nbr, 2), 270)
    vmin = 10
    vmax = 1500
    an_slice = image_rot
    print('Image size : ', an_slice.shape)
    return an_slice


def diplay2figs(item1, item2):
    fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
    ax = axes.ravel()
    ax[0] = plt.subplot(1, 2, 1)
    ax[1] = plt.subplot(1, 2, 2)

    ax[0].imshow(item1, cmap=plt.cm.gray)
    ax[0].axis('off')

    ax[1].imshow(item2, cmap=plt.cm.gray)
    ax[1].axis('off')
    plt.show()


def im_countour_fun(masked_img):
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    from skimage import data, img_as_float
    from skimage.segmentation import (morphological_chan_vese,
                                      morphological_geodesic_active_contour,
                                      inverse_gaussian_gradient,
                                      checkerboard_level_set)

    def store_evolution_in(lst):
        """Returns a callback function to store the evolution of the level sets in
        the given list.
        """

        def _store(x):
            lst.append(np.copy(x))

        return _store

    # Morphological ACWE
    #image = img_as_float(data.camera())
    image = masked_img
    # Initial level set
    init_ls = checkerboard_level_set(image.shape, 6)
    # List with intermediate results for plotting the evolution
    evolution = []
    callback = store_evolution_in(evolution)
    ls = morphological_chan_vese(image, 35, init_level_set=init_ls, smoothing=0,
                                 iter_callback=callback)

    fig, ax = plt.subplots(figsize=(10, 6))
    #ax = axes.flatten()

    plt.imshow(image, cmap="gray")
    time.sleep(0.0004)

    ax.set_axis_off()
    plt.contour(ls, [0.5], colors='r')
    ax.set_title(
        "Morphological ACWE segmentation, Frame number =", fontsize=12)
#    ax.pause(0.04)
    return fig

def storeData(item):
    # initializing data to be stored in db
    # Omkar = {'key' : 'Omkar', 'name' : 'Omkar Pathak',
    # 'age' : 21, 'pay' : 40000}
    # Jagdish = {'key' : 'Jagdish', 'name' : 'Jagdish Pathak',
    # 'age' : 50, 'pay' : 50000}

    # # database
    # db = {}
    # db['Omkar'] = Omkar
    # db['Jagdish'] = Jagdish

    # Its important to use binary mode
    dbfile = open('examplePickle', 'ab')

    # source, destination
    pickle.dump(item, dbfile)
    dbfile.close()

def maskIT(img):
    mask = filter_img_func(cropped_image, select_method='threshold_mean', automated="on")    # import pickle

    # open_file = open('test.pckl', "wb")
    # pickle.dump([cropped_image,an_slice,mask], open_file)
    # open_file.close()
    #print(type(mask))

    from skimage.segmentation import clear_border

    clear_border_mask = clear_border(mask)

    mask2=nd.binary_erosion(clear_border_mask).astype(int)
   # diplay2figs(mask,mask2)

    from skimage import morphology
    mask1_Fv = morphology.remove_small_objects(mask2, 500)
    open_img = nd.binary_opening(mask1_Fv)

   # close_img = nd.binary_closing(open_img)

    diplay2figs(mask,open_img)
    #mask1_countour = im_countour_fun(mask1_Fv)
#mask1_countour = im_countour_fun(filled_mask1)
    return open_img


if __name__ == "__main__":

    file_extension = 'nii'                          # Define the file extention
    # Load the file with given extention
    
    file1, file2 = loadfiles()
    an_slice = take_an_slice(file2, slice_nbr=108)    # Select an Slice, e.g. 80
    # Intractivly selct an crop the image,
    cropped_image = click_to_crop_img(an_slice)
    df = draw_multi_ROIs_get_Stat(cropped_image)
    # Press "q" twice to get the cropped
    # image back
    # Pause befor closing all the images
    plt.pause(0.000000004)
    plt.close('all')
    
    mask = maskIT(cropped_image)

    #storeData(cropped_image)
    #mask = filter_img_func(cropped_image, select_method='threshold_mean', automated="on")
    import pickle

    open_file = open('test.pckl', "wb")
    pickle.dump([cropped_image,an_slice,mask], open_file)
    open_file.close()
    #print(type(mask))



    # mask2=nd.binary_erosion(clear_border_mask).astype(int)

    #from skimage import morphology
    #mask1_Fv = morphology.remove_small_objects(mask2, 1000)
    #open_img = nd.binary_opening(mask2)

    #close_img = nd.binary_closing(open_img)
   # mask = maskIT(cropped_image)
    # diplay2figs(mask,mask1_Fv)
    mask1_countour = im_countour_fun(mask)
