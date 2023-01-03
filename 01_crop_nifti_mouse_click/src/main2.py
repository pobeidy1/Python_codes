# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 23:59:50 2023

@author: pobe4699
"""

# -*- coding: utf-8 -*-
"""
Serarch subforders for nifti file 
Load and display an slice 
Crop the image using mouse click 
Return the final, cropped image at the end 

@author: pobe4699
"""

img_folder_num ="folder_04"
#clear all variable if you are using Spyder
#from IPython import get_ipython;
#get_ipython().magic('reset -sf')
import pickle

import sys
import os
from matplotlib.pyplot import savefig
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
from utls.img_stat import img_stat_func

from scipy import ndimage as nd
from skimage.morphology import reconstruction

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import cv2
import pandas as pd




def loadfiles():
    # Select file: Go to this function to further filter which file to select
    magnitude_fNames, qsm_fNames = open_multi_file_full_path(file_extension)
    
    #Load selected files: This function will load the same nifti from two time point spesific to this experiment
    magnitude_timepoint_01, magnitude_timepoint_02  = load2corresponding_files(magnitude_fNames, 0)
    qsm_timepoint_01, qsm_timepoint_02              = load2corresponding_files(qsm_fNames, 0)

    return magnitude_timepoint_01, magnitude_timepoint_02,qsm_timepoint_01, qsm_timepoint_02


def take_an_slice(file, slice_nbr):
    # from file1 or 
    slice_nbr       = slice_nbr
    image_rot       = ndimage.rotate(np.take(file, slice_nbr, 2), -90)
    image_rot       = np.fliplr( image_rot)
    vmin            = 10
    vmax            = 1500
    an_slice        = image_rot
    print('Image size : ', an_slice.shape)
    return an_slice

def process_timepoints_magnitude_vs_qsm(magnitude_img,qsm_img,slice_number_list,img_folder_num,timepoint):
    timepoint= str(timepoint)

    for i in slice_number_list:
        an_slice_file1_mag  = take_an_slice(magnitude_img, i)  # Select an Slice, e.g. 80
        an_slice_file1_qsm  = take_an_slice(qsm_img, i)  # Select an Slice, e.g. 80

        # Interactively select mag img to draw mask
        # cropped_image = click_to_crop_img(an_slice)
        df_mag_im, mask_mag_im  = draw_multi_ROIs_get_Stat(an_slice_file1_mag)
        # apply the mask to qsm img
        df2_qsm_im, mask_qsm_im = img_stat_func(an_slice_file1_qsm, mask_mag_im)
        savefig(f' {img_folder_num}_mask_timepoint_ {timepoint} _fNum_ {str(i)} .png', format='png', dpi=100)  #

        df_mag_im.to_csv (f' {img_folder_num}_mask_timepoint_ {timepoint} _fNum_ {str(i)} _mag.csv', encoding='utf-8', index=False)
        df2_qsm_im.to_csv(f' {img_folder_num}_mask_timepoint_ {timepoint} _fNum_ {str(i)} _qsm.csv', encoding='utf-8', index=False)

        open_file = open (f' {img_folder_num}_mask_timepoint_ {timepoint} _fNum_ {str(i)} .pckl', "wb")
        pickle.dump([df_mag_im, df2_qsm_im, mask_mag_im, mask_qsm_im], open_file)
        open_file.close()

if __name__ == "__main__":

    file_extension = 'nii'                # Define the file extention

    # Load the file with given extention
    magnitude_timepoint_01, magnitude_timepoint_02,qsm_timepoint_01, qsm_timepoint_02 = loadfiles()

    # mask magnitude im and apply the mask to qsm img
    #todo : mask bright qsm regions out
    magnitude_img       = magnitude_timepoint_01
    qsm_img             = qsm_timepoint_01
    slice_number_list   = [108,109,110,111,112]
    timepoint           = 1 # manually change this
    img_folder_num      = 4
    # Inputs: magnitude_img, qsm_img, slice_number_list, img_folder_num
    process_timepoints_magnitude_vs_qsm (magnitude_img,qsm_img,slice_number_list,img_folder_num,timepoint)
