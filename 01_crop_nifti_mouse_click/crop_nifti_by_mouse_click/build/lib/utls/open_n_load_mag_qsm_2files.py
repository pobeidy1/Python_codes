# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 23:22:03 2022

@author: pobe4699
"""


import os
import glob

from tkinter import filedialog
from tkinter import *
import nibabel as nib



def open_multi_file_full_path(file_extension):  # path_to_data,
    # inputs:
    # technically you can use any file extention (I used this for image formats and cvs, json etc..)

    root = Tk()
    root.withdraw()
    
    path = filedialog.askdirectory()
    # get data file names, all the file extention
    os.chdir(path)
    
    all_fNames0 = glob.glob(path + '/**/*.{}'.format(file_extension), recursive=True)
    print("Total number of file:", len(all_fNames0))
    
    # add simple filter in the string e.g. *mag_MEGRE multi echo & mag_T2starw 
    
    all_mag_fNames = glob.glob(path + '/**/*mag_MEGRE.{}'.format(file_extension), recursive=True)
    all_qsm_fNames = glob.glob(path + '/**/*scaled_qsm_000_twopass_average.{}'.format(file_extension), recursive=True)

    return all_mag_fNames, all_qsm_fNames




def load2corresponding_files(path,i):  # open the files
    
    #I needed to find a matching file in diffrent folder, you perhaps dont need this part
    #just sue from "file1" onwards
    number_of_files = len(path)
    half_num_of_files = int(number_of_files / 2)

    file_num_t1 = list(range(0, half_num_of_files))
    file_num_t2 = list(range(half_num_of_files, number_of_files))
   
    i = i
    j = i + 1
    wanted_1st_fNum = file_num_t1[i]
    wanted_2nd_fNum = file_num_t2[j]

    file1 = nib.load(path[wanted_1st_fNum]).get_fdata()
    print("file 1:", path[wanted_1st_fNum][19:])

    file2 = nib.load(path[wanted_2nd_fNum]).get_fdata()
    print("file 2:", path[wanted_2nd_fNum][19:])

    return file1, file2

