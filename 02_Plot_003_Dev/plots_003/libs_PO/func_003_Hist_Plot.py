
import pandas as pd
import os
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LinearRegression
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.transforms as transforms
from matplotlib.pyplot import savefig, subplot, figure
import time
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np



# # ##---------------------------------------Histogram plot -------
# def hist_plot_2histImposed_fitted(dataset1, dataset2, histTitle, histXlabel, ax=None, **kwargs):
#     ax = ax or plt.gca()

#     # kernel density estimation (KDE) , non-parametric way
#     dataset1.plot.kde(ax=ax, color='k', lw=1.5,
#                       bw_method=0.95, title=histTitle)
#     # to estimate the probability density function (PDF)
#     mean_dataset1 = dataset1.mean()
#     mean_dataset2 = dataset2.mean()
#     std_dataset1 = dataset1.std()
#     std_dataset2 = dataset2.std()

#     dataset1.plot.hist(density=True, color='k', lw=1.5, histtype='step',
#                        stacked=True, fill=False,  alpha=0.85, ax=ax)  # legend=legend_notes,

#     dataset2.plot.kde(ax=ax, color='k', lw=1,
#                       bw_method=0.95, linestyle='dashed')
#     dataset2.plot.hist(density=True,  color='k', lw=1, histtype='step', stacked=True,
#                        fill=False, alpha=0.8, linestyle='dashed', ax=ax)  # legend=legend_notes,

#     # ax.grid(axis='y')
#     ax.set_facecolor('w')
#     ax.set_xlabel(histXlabel, size=10, labelpad=2)
#     ax.set_ylabel('Probability', size=10, labelpad=2)
#     # annotate text
#     x_pos = 0.05  # dataset1.min()+10#20#dataset1[0]#-X_percentage
#     y_pos = 0.67  # dataset1.max()-0.01#0.02#dataset1[0]
#     plt.text(x_pos, y_pos, 'Mean $\pm$ STD \n' + '{0:.1f}'.format(mean_dataset1) + "  $\pm$" + '{0:.1f}'.format(std_dataset1)+"(-)\n"
#              + '{0:.1f}'.format(mean_dataset2) + "  $\pm$" + '{0:.1f}'.format(std_dataset2)+"(--)", size=10, style='italic',
#              bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 4}, verticalalignment='bottom', horizontalalignment='left', transform=ax.transAxes)
#     #hist_ax.legend(loc='center', bbox_to_anchor=(0.5, -0.50), borderaxespad=0, frameon=False, shadow=False, ncol=2)
#     # return ax.boxplot(data, **kwargs)
#     # plt.show()
#     plt.tight_layout()

