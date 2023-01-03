"""Test if the old example still works
(commit 80737fa9d66d839e52b40d7cadcf02e143a86b4a)"""
from scipy import ndimage, stats, signal  # scipy provides scientific computing functions
import numpy as np  # numpy provides efficient matrix implementation in python
# matplotlib provides plot functions similar to MATLAB
import matplotlib.pyplot as plt
from skimage import io, color  # skimage is an image processing library
import pylab as pl
from roipoly import roipoly
import cv2
import statistics as stat

import warnings
warnings.filterwarnings('ignore')

# create image
#img = pl.ones((100, 100)) * range(0, 100)
# print(type(img))

# read an existing image
#img= cv2.imread('ex_im_for_01_Multi_ROI',1)
image_file = 'ex_im_for_01_Multi_ROI.png'
img = pl.imread(image_file)

# fig, ax = plt.subplots()
# ax.imshow(image)
# ax.axis('off')

# plt.title('matplotlib.pyplot.imread() function Example',
# fontweight ="bold")
# plt.show()

img = img[:, :, 0]
# show the image
pl.imshow(img, interpolation='nearest', cmap="Greys")
pl.colorbar()
pl.title("left click: line segment         right click: close region")

# let user draw first ROI
ROI1 = roipoly(roicolor='r')  # let user draw first ROI

# show the image with the first ROI
pl.imshow(img, interpolation='nearest', cmap="Greys")
pl.colorbar()
ROI1.displayROI()
pl.title('draw second ROI')

# let user draw second ROI
ROI2 = roipoly(roicolor='b')  # let user draw ROI

# show the image with both ROIs and their mean values
pl.imshow(img, interpolation='nearest', cmap="Greys")
pl.colorbar()
[x.displayROI() for x in [ROI1, ROI2]]
#[x.displayMean(img) for x in [ROI1, ROI2]]
pl.title('The two ROIs')

print(type(ROI1))
#data = [7,5,4,9,12,45]
# print(stat.mean(data))

# Load neccessary python modules

#grayIm = color.rgb2gray(img)
plt.figure()
io.imshow(img)
histCount, edge, tmp = plt.hist(grayIm.flatten(), bins=100)
