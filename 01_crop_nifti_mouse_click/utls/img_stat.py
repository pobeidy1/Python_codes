import statistics

from matplotlib import pyplot as plt
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

roi_names = []
roi_pixel_num = []

roi_means_list = []
roi_stdev_list = []
roi_median_list = []

roi_quantile25 = []
roi_quantile50 = []
roi_quantile75 = []
roi_coordinates_list = []

def img_stat_func(im_orig, mask):
    new_im = im_orig[mask]
    count = new_im.shape[0]

    mean = statistics.mean(new_im)
    std = statistics.stdev(new_im)

    median = np.median(new_im)

    q25 = np.quantile(new_im, .25)
    q50 = np.quantile(new_im, .50)
    q75 = np.quantile(new_im, .75)

    roi_pixel_num.append(count)
    roi_means_list.append(mean)
    roi_stdev_list.append(std)
    roi_median_list.append(median)

    roi_quantile25.append(q25)
    roi_quantile50.append(q50)
    roi_quantile75.append(q75)


# I edited here to get mask stat ino a df format
    df2 = pd.DataFrame(roi_names)

    df2["pixel num"] = roi_pixel_num
    df2["mean"] = roi_means_list
    df2["STD"] = roi_stdev_list
    df2["median"] = roi_median_list

    df2["Quantile 25"] = roi_quantile25
    df2["Quantile 50"] = roi_quantile50
    df2["Quantile 75"] = roi_quantile75

    # im_out = roi_coordinates_list
    #print(df)
    return df2, new_im