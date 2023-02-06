
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

def scatter2x_plot_fitted_Reg(dataset1, dataset2, scatter_Title, x_label_scatter_plot, y_label_scatter_plot, ax=None, **kwargs):
    ax = ax or plt.gca()

    x1 = dataset1.values.reshape(-1, 1)
    y1 = dataset2.values.reshape(-1, 1)

    # facecolors='none', edgecolors='r'
    linear_regressor = LinearRegression()  # create object for the class
    reg = linear_regressor.fit(x1, y1)      # perform linear regression
    reg = LinearRegression().fit(x1, y1)
    R_squr = reg.score(x1, y1)
    Y_pred = linear_regressor.predict(x1)  # make predictions

    domi_a = reg.coef_[0]
    ax.plot(x1, Y_pred, color='k', linewidth=0.5)


    x_pos = 10#x1.min()  # -X_percentage
    forxpos = (y1[-1] / 100) * 38
    y_pos = y1[-1]+forxpos#y1.max()+5
    ax.text(x_pos, y_pos, 'Slope =' + '{0:.2f}'.format(domi_a[0]) + "  R\u00b2 =" + '{0:.2f}'.format(R_squr), size=10, style='italic',
            bbox={'facecolor': 'w', 'alpha': 0.009, 'pad': 5})  # ,verticalalignment='bottom', horizontalalignment='right')
    # plot the smoothed timeseries with intervals
    ax.scatter(x1, y1, s=20, linewidth=0.5,  facecolors='none',
               edgecolors='k', label='Mean intensity')  # alpha= 0.98,
    #mean +-SD
    m1,m2 = dataset1.mean(),dataset1.mean()
    sd1, sd2 = dataset1.std(),dataset1.std()
    m_dif=((((m1-m2))/m1)*100)

     ax.text(x_pos, y_pos-4, '{0:.f}'.format(m1) + "  +\-" + '{0:.1f}'.format(sd1), size=10, style='italic',
                bbox={'facecolor': 'w', 'alpha': 0.009, 'pad': 5})  # ,verticalalignment='bottom',
    ax.text(x_pos, y_pos-8, '{0:.f}'.format(m2) + "  +\-" + '{0:.1f}'.format(sd2), size=10, style='italic',
                bbox={'facecolor': 'w', 'alpha': 0.009, 'pad': 5})  # ,verticalalignment='bottom',
 horizontalalignment='right')
    ax.text(x_pos, y_pos-12, 'mean dif =' + '{0:.f}'.format(d_dif) , size=10, style='italic',
                bbox={'facecolor': 'w', 'alpha': 0.009, 'pad': 5})  # ,verticalalignment='bottom',
 horizontalalignment='right')

        # plot the smoothed timeseries with intervals
        ax.scatter(x1, y1, s=20, linewidth=0.5,  facecolors='none',
                   edgecolors='k', label='Mean intensity')  # alpha= 0.98,

    x = np.linspace(0, 250, 250)
    plt.plot(x, x, 'k--', lw=0.5)  # identity line
    forxlim=(y1[-1]/100)*50
    plt.xlim(0, y1[-1]+forxlim)
    plt.ylim(0, y1[-1]+forxlim)
    plt.title(scatter_Title)

    ax.grid(False)
    ax.set_xlabel(x_label_scatter_plot, size=8, labelpad=2)
    ax.set_ylabel(y_label_scatter_plot, size=8, labelpad=2)
    plt.tight_layout()

