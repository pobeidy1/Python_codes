import sys
import os

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

import pickle

a = 3; b = [11,223,435];
pickle.dump([a,b], open("trial.p", "wb"))

c,d = pickle.load(open("trial.p","rb"))

print(c,d) ## To verify

print("done")
