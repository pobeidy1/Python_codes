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



from libs_PO.func_003_Bland_Altman import plot_blandaltman
from libs_PO.func_003_Scatter_Plot import scatter2x_plot_fitted_Reg
from libs_PO.func_003_Stat_Report import stat101
#from libs_PO.forPlots import scatter2x_plot_fitted_Reg
#from libs_PO.forPlots import plot_blandaltman

import pandas as pd
import time 
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig, subplot, figure

timestr = time.strftime("%Y%m%d_%H%M%S_")

# Part 3) upload the csv file, from pathlib import Path

folder_path = "Input/"  #"/home/stiladmin/iapl_matlab/papers/003_4DCARE_Trials/python_scripts/Input/"
#folder_path = "/home/stiladmin/iapl_matlab/papers/003_4DCARE_Trials/python3/Input/"
#folder_path = "/home/stiladmin/Insync/peyman@grievelab.com/Google Drive - Shared with me/003_4DCARE_Trials/DOCS/Figures"
#folder_path = "/home/stiladmin/iapl_matlab/temp/" 
#folder_path = '/home/stiladmin/iapl_matlab/papers/003_4DCARE_Trials/apython3/Input/'
save_results_to = "Output/"  #'/home/stiladmin/iapl_matlab/papers/003_4DCARE_Trials/python_scripts/Output/'
#save_results_to = "/home/stiladmin/Insync/peyman@grievelab.com/Google Drive - Shared with me/003_4DCARE_Trials/DATA/Python_Code003_output/"


def main():  #2DPC MG vs SMG

    df = pd.read_csv(folder_path + 'Final_20_added_JL_PO_data.csv') #2DPC SMG vs MG  2DPC_4Dflow_SMGvsMG
    #df = pd.read_csv(folder_path + 'temp.csv') #2DPC SMG vs MG  2DPC_4Dflow_SMGvsMG
    # get the list(data) of column header
    col_list = list(df.columns)
    dataset1, dataset2 = df[col_list[10]], df[col_list[28]]
    dataset3, dataset4 = df[col_list[13]], df[col_list[31]]

    fig_w, fig_h, fig_dpi = 8, 8, 300
    f = plt.figure(figsize=(fig_w, fig_h), dpi=fig_dpi)
    f.suptitle('2DPC: SMG vs. MG ')
    FName = "003_4DCARE_trial_2DPC_SMG_vs_MG"

    # ------------Plot s1----------------------
    plt.subplot(2, 2, 1)
    scatter_Title = 'AscA'  # 'Expert vs. Trained Observer'
    x_label_scatter_plot = 'SMG: Flow (mL/beat)'
    y_label_scatter_plot = 'MG: Flow (mL/beat)'

    scatter2x_plot_fitted_Reg(dataset1, dataset2, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)
    # ------------Plot 2----------------------
    plt.subplot(2, 2, 2)
    scatter_Title = 'MPA'  # 'Expert vs. Trained Observer'
    x_label_scatter_plot = 'SMG: Flow (mL/beat)'
    y_label_scatter_plot = 'MG: Flow (mL/beat)'
    scatter2x_plot_fitted_Reg(dataset3, dataset4, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)

    # ------------Plot 3----------------------
    plt.subplot(2, 2, 3)
    plt.title("AscA")
    x_label = 'SMG '
    y_label = 'MG '

    plot_blandaltman(dataset1, dataset2, x_label, y_label)

    # ------------Plot 4----------------------
    plt.subplot(2, 2, 4)
    plt.title("MPA")
    plot_blandaltman(dataset3, dataset4, x_label, y_label)

    plt.tight_layout()

    savefig(save_results_to + timestr + FName + '.png', format='png', dpi=300)  #

    stat101(dataset1, dataset2, FName+"_AscA")
    stat101(dataset3, dataset4, FName+"_MPA")



def main1(): # 2DPC MG test retest

    df = pd.read_csv(folder_path + '2DPC_4Dflow_SMGvsMG.csv') #load the data

    # assign each col pair, one need to check this everytime
    col_list = list(df.columns) # get the list(data) of column header # print(col_list)
    dataset1, dataset2 = df[col_list[22]], df[col_list[28]]
    dataset3, dataset4 = df[col_list[25]], df[col_list[31]]

    fig_w, fig_h, fig_dpi = 6, 6, 100
    f = plt.figure(figsize=(fig_w, fig_h), dpi=fig_dpi)
    f.suptitle('2DPC: MG Test vs. Retest')
    FName= "2DCD_MG_Test_Retest"


    # Plot--------------------------------------------------the scatter plot
    plt.subplot(2, 2, 1)
    scatter_Title = 'AscA'  # 'Expert vs. Trained Observer'
    x_label_scatter_plot = 'Flow (mL/beat)'
    y_label_scatter_plot = 'Flow (mL/beat)'
    scatter2x_plot_fitted_Reg(dataset1, dataset2, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)

    # Plot------------------------------------------------- 2nd scatter plot
    plt.subplot(2, 2, 2)
    scatter_Title = 'MPA'  # 'Expert vs. Trained Observer'
    scatter2x_plot_fitted_Reg(dataset3, dataset4, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)

    # Plot-------------------------------------------------Bland Altman plot 1
    plt.subplot(2, 2, 3)
    plt.title("AscA")
    x_label = 'Test '
    y_label = 'Retest '

    plot_blandaltman(dataset1, dataset2, x_label, y_label)

    # Plot the Bland Altman plot
    plt.subplot(2, 2, 4)
    plt.title("MPA")

    plot_blandaltman(dataset3, dataset4, x_label, y_label)

    plt.tight_layout()

    timestr = time.strftime("%Y%m%d_%H%M%S_")
    savefig(save_results_to+timestr+FName +'.png',format='png', dpi=300) #

    stat101(dataset1, dataset2, FName + "_AscA")
    stat101(dataset3, dataset4, FName + "_MPA")


def main2(): # 4D Flow MG test retest
    df = pd.read_csv(folder_path + '2DPC_4Dflow_SMGvsMG.csv')
    # get the list(data) of column header
    col_list = list(df.columns)
    dataset1, dataset2 = df[col_list[34]], df[col_list[40]]
    dataset3, dataset4 = df[col_list[37]], df[col_list[43]]

    fig_w = 6;fig_h = 6;fig_dpi = 100
    f = plt.figure(figsize=(fig_w, fig_h), dpi=fig_dpi)
    f.suptitle('4D-flow: MG Test vs. Retest')
    FName= "4DFLOW_MG_Test_Retest"

    # ------------Plot 3----------------------
    plt.subplot(2, 2, 1)
    scatter_Title = 'AscA'  # 'Expert vs. Trained Observer'
    x_label_scatter_plot = 'Flow (mL/min)'
    y_label_scatter_plot = 'Flow (mL/min)'
    scatter2x_plot_fitted_Reg(dataset1, dataset2, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)

    # ------------Plot 4----------------------
    plt.subplot(2, 2, 2)
    scatter_Title = 'MPA'  # 'Expert vs. Trained Observer'
    scatter2x_plot_fitted_Reg(dataset3, dataset4, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)

    # ------------Plot 5----------------------
    ## Bland Altman plot 1
    plt.subplot(2, 2, 3)
    plt.title("AscA")
    x_label = 'Test '
    y_label = 'Retest '

    plot_blandaltman(dataset1, dataset2, x_label, y_label)

    # Plot the Bland Altman plot
    plt.subplot(2, 2, 4)
    plt.title("MPA")

    plot_blandaltman(dataset3, dataset4, x_label, y_label)
    plt.tight_layout()
    savefig(save_results_to+timestr+FName+'.png', format='png', dpi=300) #

    stat101(dataset1, dataset2, FName + "_AscA")
    stat101(dataset3, dataset4, FName + "_MPA")

def main3():  # All the 200 cases

    df = pd.read_csv(folder_path + '/20211227_200_cases_2DPC&4DFlow_AG_test.csv')
    col_list = list(df.columns)  # get the list(data) of column header # print(col_list)
    dataset1, dataset2 = df[col_list[5]], df[col_list[29]]
    dataset3, dataset4 = df[col_list[18]], df[col_list[32]]

    fig_w, fig_h, fig_dpi = 6, 6, 100
    f = plt.figure(figsize=(fig_w, fig_h), dpi=fig_dpi)
    f.suptitle('2DPC vs 4D flow')# n=%.2f) % 184#len(df)
    FName = "all_2DPC_vs_4D_flow"

    plt.subplot(2, 2, 1)
    scatter_Title = 'AscA'  # 'Expert vs. Trained Observer'
    x_label_scatter_plot = '2DPC flow (mL/beat)'
    y_label_scatter_plot = '4D-flow flow (mL/beat)'
    scatter2x_plot_fitted_Reg(dataset1, dataset2, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)

    plt.subplot(2, 2, 2)
    scatter_Title = 'MPA'  # 'Expert vs. Trained Observer'
    scatter2x_plot_fitted_Reg(dataset3, dataset4, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)

    #Bland Altman plot 1
    plt.subplot(2, 2, 3)
    plt.title("AscA")
    x_label = '2DPC '
    y_label = '4D-flow '

    plot_blandaltman(dataset1, dataset2, x_label, y_label)

    # Plot the Bland Altman plot
    plt.subplot(2, 2, 4)
    plt.title("MPA")

    plot_blandaltman(dataset3, dataset4, x_label, y_label)
    plt.tight_layout()
    savefig(save_results_to + timestr + FName + '.png', format='png', dpi=300)  #

    stat101(dataset1, dataset2, FName + "_AscA")
    stat101(dataset3, dataset4, FName + "_MPA")


def main4():  #4DFlow MG vs SMG
    #
    df = pd.read_csv(folder_path + '2DPC_4Dflow_SMGvsMG.csv')
    # get the list(data) of column header
    col_list = list(df.columns)
    dataset1, dataset2 = df[col_list[16]], df[col_list[34]]
    dataset3, dataset4 = df[col_list[19]], df[col_list[37]]

    fig_w, fig_h, fig_dpi = 6, 6, 100
    f = plt.figure(figsize=(fig_w, fig_h), dpi=fig_dpi)
    f.suptitle('4D-flow: SMG vs. MG ')
    FName = "4Dflow_SMG_vs_MG"

    # ------------Plot 1----------------------
    plt.subplot(2, 2, 1)
    scatter_Title = 'AscA'  # 'Expert vs. Trained Observer'
    x_label_scatter_plot = 'SMG: Flow (mL/beat)'
    y_label_scatter_plot = 'MG: Flow (mL/beat)'

    scatter2x_plot_fitted_Reg(dataset1, dataset2, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)

    # ------------Plot 2----------------------
    plt.subplot(2, 2, 2)
    scatter_Title = 'MPA'  # 'Expert vs. Trained Observer'
    scatter2x_plot_fitted_Reg(dataset3, dataset4, scatter_Title,
                              x_label_scatter_plot, y_label_scatter_plot)  # ,scatter_ax)

    # ------------Plot 3----------------------
    plt.subplot(2, 2, 3)
    plt.title("AscA")
    x_label = 'SMG '
    y_label = 'MG '

    plot_blandaltman(dataset1, dataset2, x_label, y_label)

    # ------------Plot 4----------------------
    plt.subplot(2, 2, 4)
    plt.title("MPA")
    plot_blandaltman(dataset3, dataset4, x_label, y_label)

    plt.tight_layout()

    savefig(save_results_to + timestr + FName + '.png', format='png', dpi=300)  #

    stat101(dataset1, dataset2, FName+"_AscA")
    stat101(dataset3, dataset4, FName+"_MPA")


if __name__ == "__main__":
    main()   # 2DPC MG vs SMG
    #main1()  # 2DPC MG test retest
    #main2()  # 4D Flow MG test retest
    #main3()  # All the 200 cases
    #main4()  # 4DFlow MG vs SMG
 
