# -*- coding: utf-8 -*-
"""
Serarch subforders for nifti file 
Load and display an slice 
Crop the image using mouse click 
Return the final, cropped image at the end 

@author: pobe4699
"""

import os
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

# from ..utls.open_n_load_mag_qsm_2files import load2corresponding_files
from .utls.click_n_crop import click_to_crop_img
from .utls.open_n_load_mag_qsm_2files import open_multi_file_full_path

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


def loadfiles():
    all_filtered_mag_fNames_full_path, all_filtered_qsm_fNames_full_path = open_multi_file_full_path(
        file_extension)  # path_to_data

    title = 'Susceptibility MAP t1 vs t2'
    file1, file2 = load2corresponding_files(all_filtered_mag_fNames_full_path, 0)
    return file1, file2


def take_an_slice(file1, slice_nbr=80):
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


if __name__ == "__main__":
    file_extension = 'nii'  # Define the file extention
    # Load the file with given extention
    file1, file2 = loadfiles()
    an_slice = take_an_slice(file1, slice_nbr=80)  # Select an Slice, e.g. 80
    # Intractivly selct an crop the image,
    cropped_image = click_to_crop_img(an_slice)
    # Press "q" twice to get the cropped
    # image back
    # Pause befor closing all the images
    plt.pause(0.000000004)
    plt.close('all')
    storeData(cropped_image)
    # Saving the objects:
