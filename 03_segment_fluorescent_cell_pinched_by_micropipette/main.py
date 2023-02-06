# -*- coding: utf-8 -*-
"""
Make a folder to store the data 

I have coped the image with imagej
Part A) load tiff
Part B) run bunch of filters and decide which has higher SNR, to be selected for masking
Part C) apply the recangular mask by geting the user to draw the mask on brightfiled image
Part D) apply the small mask next to nozole, by using the nossel as guide
Part E) apply the premieter mask

in easch step store the data in csv file 

install
pip install opencv-python
pip install scikit-image

"""
#clear all variable
from IPython import get_ipython;   
get_ipython().magic('reset -sf')

import cv2
import os
import matplotlib.pyplot as plt
import skimage.filters as skfilt
from skimage.filters import try_all_threshold 


#%%    

#read the file and use the file name to create a folder
#put the new files gernerated into the new folder 
import pey_py_utls

fullpath, fName, fDirectory,  path_to_newFolder, path_to_file, img_ori_16bit, img_ori_8bit, img_ori_float = opentif_tS (0)

filename = fName
path =path_to_newFolder
fullpath = os.path.join(path, filename)
#%%
_, frame_data = cv2.imreadmulti(path_to_file, [], -1)

Im_frame01 = frame_data[int(len(frame_data)/2)+1]
plt.imshow(Im_frame01)

fig, ax = try_all_threshold(Im_frame01, figsize=(10, 8), verbose=False)
plt.show()

selected_filter = skfilt.threshold_mean
#%%

#Select foreground and bkg

from matplotlib.widgets import RectangleSelector


def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    print(" The button you used were: %s %s" % (eclick.button, erelease.button))


def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)


fig, current_ax = plt.subplots()                 # make a new plotting 
current_ax.imshow(Im_frame01)
current_ax.title.set_text('Select foreground ROI and press q')
print("\n      click  -->  release")

# drawtype is 'box' or 'line' or 'none'
toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
plt.connect('key_press_event', toggle_selector)
plt.show()

plt.pause(10)

plt.close('all')

fig, current_ax = plt.subplots()                 # make a new plotting 
current_ax.imshow(Im_frame01)
current_ax.title.set_text('Select backgound ROI then press q')
print("\n      click  -->  release")

# drawtype is 'box' or 'line' or 'none'
toggle_selector.RS_bkg = RectangleSelector(current_ax, line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
plt.connect('key_press_event', toggle_selector)
plt.show()


#%%
from matplotlib.widgets import RectangleSelector
from skimage.measure import label, regionprops, regionprops_table
from scipy import ndimage

img = [] # some array of images
frames = [] # for storing the generated images

fig, ax = plt.subplots()

m=0 # fix frame name not to be from i but m  

for i in range(0,(len(img_ori_16bit)*2),2):
    
    im1 = frame_data[i]    
    #im1 = wiener(im1) #***---->>>  enhance the signal if needed****

    uniform_filtered_img, blurred_img, median_img, sobel_img, object_labels, mask_orig, masked_img = filteringIm_fun(im1,2,0.4)
     
    thresh_val = selected_filter (blurred_img)
    new_mask = blurred_img > (thresh_val+(0.4*thresh_val))
    
    mask_orig = new_mask
    #new_mask = clear_border(new_mask)
    object_labels = skmeas.label(new_mask)
    
    masked_img = im1*new_mask
   
    #------->>>>The active contour model is a method to fit open or closed splines to lines or edges in an image
   
    #mark where the mask sits
    ax.cla()
    
    ax.imshow(frame_data[i])
    plt.contour(new_mask[:300, :300], [0.5], linewidths=2,colors='y')
    ax.set_title("frame {}".format(m+1))

    fig.set_size_inches(8, 3)
    ax.axis('off') #Turn off *all* ticks
    m=m+1
    plt.pause(0.000000004)
    
    
    fig.savefig(fullpath+'_'+str(i)+'.svg', format='svg', dpi=300)
    
filename   = fullpath+'_'+str(i)
vars_list  = [img_ori_16bit, fullpath] 
save_vars_pickle (filename,vars_list)