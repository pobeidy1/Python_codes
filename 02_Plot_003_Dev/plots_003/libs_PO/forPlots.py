
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
import pingouin as pg

# %
SizeN=14 #size of axies 

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

# # ##---------------------------------------Scatter plot -------
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

    #mean +-SD
    m1,m2 = x1.mean(),y1.mean()
    sd1, sd2 = x1.std(),y1.std()
    m_dif=((m1-m2)/m1)
    pg_ttest_out = pg.ttest(dataset1, dataset2, paired=True).round(4)  # 
    pval = pg_ttest_out["p-val"][0]

    ax.text(x_pos, (y_pos-10), 'M+/-SD ' )
    ax.text(x_pos, (y_pos-20), 'ds1 ' + '{0:.1f}'.format(m1) + "  +/- " + '{0:.1f}'.format(sd1), size=10, style='italic', bbox={'facecolor': 'w', 'alpha': 0.009, 'pad': 5})  # ,verticalalignment='bottom',
    ax.text(x_pos, y_pos-30, 'ds2 ' + '{0:.1f}'.format(m2) + "  +/- "  + '{0:.1f}'.format(sd2), size=10, style='italic', bbox={'facecolor': 'w', 'alpha': 0.009, 'pad': 5})  # ,verticalalignment='bottom',horizontalalignment='right')
    #ax.text(x_pos, (y_pos-40), 'mean dif ' + '{0:.1f}'.format(d_dif))#+" " , size=10, style='italic', bbox={'facecolor': 'w', 'alpha': 0.009, 'pad': 5})  # ,verticalalignment='bottom',horizontalalignment='right')
    ax.text(x_pos, (y_pos-40), 'mean dif ' + '{0:.1%}'.format(m_dif) )
    ax.text(x_pos, (y_pos-50), 'p val ' + '{0:.4f}'.format(pval) )

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
    ax.set_xlabel(x_label_scatter_plot, size=SizeN, labelpad=2)
    ax.set_ylabel(y_label_scatter_plot, size=SizeN, labelpad=2)

# -------------------------------------------Bland Altman
def plot_blandaltman(x, y, x_label,y_label, agreement=1.96, xaxis="mean", confidence=.95,
                     annotate=True,
                     scatter_kws=dict(s=15, color="tab:gray", alpha=0.8,
                                      linewidth=0.5,  facecolors='none', edgecolors='k'),
                     ax=None, **kwargs):  # ,scatter_ax):
    ax = ax or plt.gca()  # to pervent new fig generation
    # figsize=(4.5, 4.5), dpi=100, ax=None):
    """
    Generate a Bland-Altman plot to compare two sets of measurements.

    Parameters
    ----------
    x, y : pd.Series, np.array, or list
        First and second measurements.
    agreement : float
        Multiple of the standard deviation to plot agreement limits.
        The defaults is 1.96, which corresponds to 95% confidence interval if
        the differences are normally distributed.
    xaxis : str
        Define which measurements should be used as the reference (x-axis).
        Default is to use the average of x and y ("mean"). Accepted values are
        "mean", "x" or "y".
    confidence : float
        If not None, plot the specified percentage confidence interval of
        the mean and limits of agreement. The CIs of the mean difference and
        agreement limits describe a possible error in the
        estimate due to a sampling error. The greater the sample size,
        the narrower the CIs will be.
    annotate : bool
        If True (default), annotate the values for the mean difference
        and agreement limits.
    scatter_kws : dict
        Additional keyword arguments passed to
        :py:func:`matplotlib.pyplot.scatter`.
    figsize : tuple
        Figsize in inches
    dpi : int
        Resolution of the figure in dots per inches.
    ax : matplotlib axes
        Axis on which to draw the plot.

    Returns
    -------
    ax : Matplotlib Axes instance
        Returns the Axes object with the plot for further tweaking.

    Notes
    -----
    Bland-Altman plots [1]_ are extensively used to evaluate the agreement
    among two different instruments or two measurements techniques.
    They allow identification of any systematic difference between the
    measurements (i.e., fixed bias) or possible outliers.

    The mean difference (= x - y) is the estimated bias, and the SD of the
    differences measures the random fluctuations around this mean.
    If the mean value of the difference differs significantly from 0 on the
    basis of a 1-sample t-test, this indicates the presence of fixed bias.
    If there is a consistent bias, it can be adjusted for by subtracting the
    mean difference from the new method.

    It is common to compute 95% limits of agreement for each comparison
    (average difference ± 1.96 standard deviation of the difference), which
    tells us how far apart measurements by 2 methods were more likely to be
    for most individuals. If the differences within mean ± 1.96 SD are not
    clinically important, the two methods may be used interchangeably.
    The 95% limits of agreement can be unreliable estimates of the population
    parameters especially for small sample sizes so, when comparing methods
    or assessing repeatability, it is important to calculate confidence
    intervals for the 95% limits of agreement.

    The code is an adaptation of the
    `PyCompare <https://github.com/jaketmp/pyCompare>`_ package. The present
    implementation is a simplified version; please refer to the original
    package for more advanced functionalities.

    References
    ----------
    .. [1] Bland, J. M., & Altman, D. (1986). Statistical methods for assessing
           agreement between two methods of clinical measurement. The lancet,
           327(8476), 307-310.

    .. [2] Giavarina, D. (2015). Understanding bland altman analysis.
           Biochemia medica, 25(2), 141-151.

    Examples
    --------
    Bland-Altman plot (example data from [2]_)

    .. plot::

        >>> import pingouin as pg
        >>> df_2dpc_mg = pg.read_dataset("blandaltman")
        >>> ax = pg.plot_blandaltman(df_2dpc_mg['A'], df_2dpc_mg['B'])
        >>> plt.tight_layout()
    """
    # Safety check
    assert xaxis in ["mean", "x", "y"]
    # Get names before converting to NumPy array
    xname = x.name if isinstance(x, pd.Series) else "x"
    yname = y.name if isinstance(y, pd.Series) else "y"
    x = np.asarray(x)
    y = np.asarray(y)
    assert x.ndim == 1 and y.ndim == 1
    assert x.size == y.size
    assert not np.isnan(x).any(), "Missing values in x or y are not supported."
    assert not np.isnan(y).any(), "Missing values in x or y are not supported."

    # Calculate mean, STD and SEM of x - y
    n = x.size
    dof = n - 1
    diff = x - y
    mean_diff = np.mean(diff)
    std_diff = np.std(diff, ddof=1)
    mean_diff_se = np.sqrt(std_diff**2 / n)
    # Limits of agreements
    high = mean_diff + agreement * std_diff
    low = mean_diff - agreement * std_diff
    high_low_se = np.sqrt(3 * std_diff**2 / n)

    # Define x-axis
    if xaxis == "mean":
        xval = np.vstack((x, y)).mean(0)
        #xlabel = f"Mean of {xname} and {yname}"
        xlabel = "Mean of ------ "

    elif xaxis == "x":
        xval = x
        xlabel = xname
    else:
        xval = y
        xlabel = yname

    # Start the plot
    # if ax is None:
    #     fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)

    # Plot the mean diff, limits of agreement and scatter
    ax.scatter(xval, diff, **scatter_kws)
    ax.axhline(mean_diff, color='k', linestyle='-', lw=1)
    ax.axhline(high, color='k', linestyle=':', lw=1)
    ax.axhline(low, color='k', linestyle=':', lw=1)

    # Annotate values
    if annotate:
        loa_range = high - low
        offset = (loa_range / 100.0) * 1.5
        trans = transforms.blended_transform_factory(
            ax.transAxes, ax.transData)
        xloc = 0.98
        ax.text(xloc, mean_diff + offset, 'Mean', ha="right", va="bottom",
                transform=trans)
        ax.text(xloc, mean_diff - offset, '%.2f' % mean_diff, ha="right",
                va="top", transform=trans)
        ax.text(xloc, high + offset, '+%.2f SD' % agreement, ha="right",
                va="bottom", transform=trans)
        ax.text(xloc, high - offset, '%.2f' % high, ha="right", va="top",
                transform=trans)
        ax.text(xloc, low - offset, '-%.2f SD' % agreement, ha="right",
                va="top", transform=trans)
        ax.text(xloc, low + offset, '%.2f' % low, ha="right", va="bottom",
                transform=trans)

    # Add 95% confidence intervals for mean bias and limits of agreement
    if confidence is not None:
        assert 0 < confidence < 1
        ci = dict()
        ci['mean'] = stats.t.interval(
            confidence, dof, loc=mean_diff, scale=mean_diff_se)
        ci['high'] = stats.t.interval(
            confidence, dof, loc=high, scale=high_low_se)
        ci['low'] = stats.t.interval(
            confidence, dof, loc=low, scale=high_low_se)
        ax.axhspan(
            ci['mean'][0], ci['mean'][1], facecolor='tab:grey', alpha=0.2)
        ax.axhspan(
            ci['high'][0], ci['high'][1], facecolor='tab:gray', alpha=0.2)
        ax.axhspan(
            ci['low'][0], ci['low'][1], facecolor='tab:gray', alpha=0.2)

    # Labels and title
    #ax.set_ylabel(f"{xname} - {yname}")
    # ax.set_xlabel(xlabel)
    ax.set_ylabel(x_label+"-"+y_label +'(mL/beat) ', size=SizeN, labelpad=2) #'Difference in flows
    ax.set_xlabel('Mean of flows (mL/beat)', size=SizeN, labelpad=2)
    #ax.set(xlim=(-1.0, 160),  autoscale_on=False)
    sns.despine(ax=ax)
    return ax
# linestyle='dashed', c='black', lw=2,
#         label='PDF Estimated via KDE')
# ax.legend(loc='best', frameon=False)


# Step 4) seprate Trianed and Expert data for AscA and MPA ino databsed with 1 column
#df_Trianed_Ao           = df_2dpc_mg[col_list[1]]
#df_Trianed_mpa          = df_2dpc_mg[col_list[3]]
#df_Expert_Ao            = df_2dpc_mg[col_list[2]]
#df_Expert_mpa           = df_2dpc_mg[col_list[4]]

