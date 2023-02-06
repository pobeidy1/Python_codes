from pathlib import Path
import os 
import tkinter as tk ; from tkinter import filedialog
from skimage import io, img_as_float, img_as_ubyte, exposure
from pathlib import Path

def opentif_tS (make_dir):

    root = tk.Tk()
    root.withdraw()
    
    #-----------open file dialog---------------
    #import skimage.io for tiff
    path_to_file = filedialog.askopenfilename()
    img_ori_16bit = io.imread(path_to_file,plugin='tifffile')       
    #as_gray=True make float
    img_ori_8bit= img_as_ubyte(img_ori_16bit)
    img_ori_float= img_as_float(img_ori_16bit)
    
        
    path = Path(path_to_file) 
    fName= path.name
    fDirectory = path.parent.absolute()
    
    path_to_newFolder = os.path.join(fDirectory, fName[:-4])   
    #parent_dir = fDirectory.__str__() # convert windowsPath to str
    fullpath = path_to_newFolder # fix this later, currentlt naZQA
    if make_dir == 1: #make a directory based on file name if () contain 1
        os.mkdir(path_to_newFolder)  #make a directory based on file name    
        pass
    
    fullpath = os.path.join(path_to_newFolder, fName)

    return fullpath, fName, fDirectory,  path_to_newFolder, path_to_file, img_ori_16bit, img_ori_8bit, img_ori_float