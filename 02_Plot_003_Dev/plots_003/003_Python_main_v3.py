# -*- coding: utf-8 -*-
a=1
if a ==1:
    print ("ok")
script_discription= """Created on 01/01/2022

Description: 
This  Python code works as part of paper-flow and generates 
4 plots to compare the AscA and MPA measurements from any paired 
experiments. 

INPUT: 
Required CSV file

The initial parts are the functions  for 

#histogram       : hist_plot_2histImposed_fitted
Scatter plot    : scatter2x_plot_fitted_Reg
Bland Altman    : plot_blandaltman

NOTE:
The code use two functions seating in HelperFunctions folder 

Depending on the dataset you are interestead to analyse, user might need to change 
the path in each function(def) or the number for the col_list[?!] 

OUTPUTS
The outputs include png files and pdf for figures and stats

@author: PO last edited 24/01/2022
"""
#$ pip install -r requirements.txt
# #---------Data--------

# Part 1) import required libraries including the customs made one



# from libs_PO.func_003_Bland_Altman import plot_blandaltman
# from libs_PO.func_003_Scatter_Plot import scatter2x_plot_fitted_Reg
from libs_PO.func_003_Stat_Report import stat101
from libs_PO.forPlots import scatter2x_plot_fitted_Reg
from libs_PO.forPlots import plot_blandaltman

import pandas as pd
import time 
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig, subplot, figure

timestr = time.strftime("%Y%m%d_%H_")#%M%S

# Part 3) upload the csv file, from pathlib import Path

folder_path = "Input/"  #"/home/stiladmin/iapl_matlab/papers/003_4DCARE_Trials/python_scripts/Input/"
#folder_path = "/home/stiladmin/iapl_matlab/papers/003_4DCARE_Trials/python3/Input/"
#folder_path = "/home/stiladmin/iapl_matlab/temp/" 
#folder_path = '/home/stiladmin/iapl_matlab/papers/003_4DCARE_Trials/apython3/Input/'
save_results_to = "Output/"  #'/home/stiladmin/iapl_matlab/papers/003_4DCARE_Trials/python_scripts/Output/'
#save_results_to = "/home/stiladmin/Insync/peyman@grievelab.com/Google Drive - Shared with me/003_4DCARE_Trials/DATA/Python_Code003_output/"

#from pandas import filter

# f1.isnull().sum().sum()

df = pd.read_csv(folder_path + '20220302_00_PO_SMG_measurements.csv') #2DPC SMG vs MG  2DPC_4Dflow_SMGvsMG
col_list = list(df.columns)

#df = df[ "asca_fdc_trial_forward_flow_PO","asca_forward_flow_SMG","asca_forward_flow_PO"]

df_SMG          = df [["study_id_SMG",  'asca_forward_flow_SMG',           'asca_reverse_flow_SMG',          'mpa_forward_flow_SMG',          'mpa_reverse_flow_SMG']]
df_PO           = df [["study_id_SMG",  'asca_forward_flow_PO',            'asca_reverse_flow_PO',           'mpa_forward_flow_PO',           'mpa_reverse_flow_PO']]
df_FDC_PO       = df [["study_id_SMG",  'asca_fdc_forward_flow_PO',        'mpa_fdc_reverse_flow_PO',        'mpa_fdc_forward_flow_PO',       'asca_fdc_reverse_flow_PO']]
df_FDC_TRIAL_PO = df [["study_id_SMG",  'asca_fdc_trial_forward_flow_PO',  'asca_fdc_trial_reverse_flow_PO', 'mpa_fdc_trial_forward_flow_PO', "mpa_fdc_trial_reverse_flow_PO"]]

# SUBTRACT EACH VALUE FROM THE MEAN OF THE COLUMN RETURN THE STIL ID NUMBER FOR THAT RAW
SMG_mean= df_SMG.mean()
PO_mean = df_PO.mean()

dataset1, dataset2 = df["asca_fdc_trial_forward_flow_PO"], df["asca_forward_flow_SMG"]
dataset3, dataset4 = df["asca_fdc_trial_forward_flow_PO"], df["asca_forward_flow_SMG"]
dataset5, dataset6 = df["asca_fdc_trial_forward_flow_PO"], df["asca_forward_flow_SMG"]
dataset7, dataset8 = df["asca_fdc_trial_forward_flow_PO"], df["asca_forward_flow_SMG"]

subTitleLeft  = '2DPC ff flow: MG rep1 vs rep2'
subTitleRight = '4D flow ff flow: MG rep1 vs rep2 '
FName = "003_4DCARE_trial_2DPC_ff_MG_rep1rep2"


def main():  # MG: 2DPC rep1 vs rep2 and 4Dflow rep1 vs rep2

    # get the list(data) of column header
    # col_list = list(df.columns)
    fig_w, fig_h, fig_dpi = 18, 12, 100
    f = plt.figure(figsize=(fig_w, fig_h), dpi=fig_dpi)
    f.suptitle(subTitleLeft + 70 * ' ' + subTitleRight, y=0.97, size=16)
    #FName = "003_4DCARE_trial_2DPC_ff_MG_rep1rep2"

    # ------------Plot s1----------------------
    plt.subplot(2, 4, 1)
    scatter_Title = 'AscA'  # 'Expert vs. Trained Observer'
    x_label_scatter_plot = 'ds1: Flow (mL/beat)'
    y_label_scatter_plot = 'ds2: Flow (mL/beat)'

    scatter2x_plot_fitted_Reg(dataset1, dataset2, scatter_Title,
                              x_label_scatter_plot,
                              y_label_scatter_plot)  # ,scatter_ax)
    # ------------Plot 2----------------------
    plt.subplot(2, 4, 2)
    scatter_Title = 'MPA'  # 'Expert vs. Trained Observer'
    scatter2x_plot_fitted_Reg(dataset3, dataset4, scatter_Title,
                              x_label_scatter_plot,
                              y_label_scatter_plot)  # ,scatter_ax)

    # ------------Plot s----------------------
    plt.subplot(2, 4, 3)
    scatter_Title = 'AscA'  # 'Expert vs. Trained Observer'

    scatter2x_plot_fitted_Reg(dataset5, dataset6, scatter_Title,
                              x_label_scatter_plot,
                              y_label_scatter_plot)  # ,scatter_ax)
    # ------------Plot 2----------------------
    plt.subplot(2, 4, 4)
    scatter_Title = 'MPA'  # 'Expert vs. Trained Observer'
    scatter2x_plot_fitted_Reg(dataset7, dataset8, scatter_Title,
                              x_label_scatter_plot,
                              y_label_scatter_plot)  # ,scatter_ax)

    # ------------Plot 3----------------------
    plt.subplot(2, 4, 5)
    plt.title("AscA")
    x_label = 'ds1 '
    y_label = 'ds2'

    plot_blandaltman(dataset1, dataset2, x_label, y_label)

    # ------------Plot 4----------------------
    plt.subplot(2, 4, 6)
    plt.title("MPA")
    plot_blandaltman(dataset3, dataset4, x_label, y_label)

    # ------------Plot 3----------------------
    plt.subplot(2, 4, 7)
    plt.title("AscA")
    plot_blandaltman(dataset5, dataset6, x_label, y_label)

    # ------------Plot 4----------------------
    plt.subplot(2, 4, 8)
    plt.title("MPA")
    plot_blandaltman(dataset7, dataset8, x_label, y_label)
    plt.subplots_adjust(wspace=0.3, hspace=0.4, top=0.87, bottom=0.1)

    # plt.tight_layout()

    savefig(save_results_to + timestr + FName + '.png', format='png', dpi=100)  #

    # stat101(dataset1, dataset2, FName + "_2D_MG_AscA")
    # stat101(dataset3, dataset4, FName + "_2D_MG_MG_MPA")
    # stat101(dataset5, dataset6, FName + "_4D_MG_AscA")
    # stat101(dataset7, dataset8, FName + "_4D_MG_MPA")


if __name__ == "__main__":
    main()   # 2DPC MG vs SMG

 
