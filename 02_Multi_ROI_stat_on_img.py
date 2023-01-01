import statistics
from roipoly import MultiRoi
import logging

import numpy as np
from matplotlib import pyplot as plt
import warnings
import pandas as pd

warnings.filterwarnings('ignore')
 

logging.basicConfig(format='%(levelname)s ''%(processName)-10s : %(asctime)s '
                           '%(module)s.%(funcName)s:%(lineno)s %(message)s',
                    level=logging.INFO)

# Create image
img = np.ones((100, 100)) * range(0, 100)

print(type(img))


# read an existing image
image_file = 'ex_im_for_01_Multi_ROI.png'
#img = plt.imread(image_file)

# img=img[:,:,0]
# Show the image
fig = plt.figure()
plt.imshow(img, interpolation='nearest', cmap="Greys")
plt.title("Click on the button to add a new ROI")

# Draw multiple ROIs
multiroi_named = MultiRoi(roi_names=['ROI1', 'ROI2'])

# Draw all ROIs
plt.imshow(img, interpolation='nearest', cmap="Greys")

roi_names = []
roi_pixel_num = []

roi_means_list = []
roi_stdev_list = []
roi_median_list = []

roi_quantile25 = []
roi_quantile50 = []
roi_quantile75 = []



for name, roi in multiroi_named.rois.items():
    roi.display_roi()
    roi.display_mean(img)
    roi_names.append(name)

    ## I edited here to get mask stat
    mask = roi.get_mask(img)
    new_im = img[mask]
    count =  new_im.shape[0]

    mean = statistics.mean(new_im)
    std  = statistics.stdev(new_im)

    median  = np.median(new_im)

    q25  = np.quantile(new_im, .25)
    q50  = np.quantile(new_im, .50)
    q75  = np.quantile(new_im, .75)

    roi_pixel_num.append(count)
    roi_means_list.append(mean)
    roi_stdev_list.append(std)
    roi_median_list.append(median)

    roi_quantile25.append(q25)
    roi_quantile50.append(q50)
    roi_quantile75.append(q75)
    

plt.legend(roi_names, bbox_to_anchor=(1.2, 1.05))
plt.show()

# I edited here to get mask stat ino a df format

df = pd.DataFrame(roi_names)

df["pixel num"]   = roi_pixel_num
df["mean"]        = roi_means_list
df["STD"]         = roi_stdev_list
df["median"]      = roi_median_list

df["Quantile 25"] = roi_quantile25
df["Quantile 50"] = roi_quantile50
df["Quantile 75"] = roi_quantile75
