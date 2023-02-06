# to use this function add to your run function : 
#from libs_PO.func_003_Bland_Altman import plot_blandaltman

# PO added   the RPC coefficient of reproducibilit
#PO: Extract this from part of the analysis done in the following paper
# References
#    ----------
#    .. [1] Bland, J. M., & Altman, D. (1986). Statistical methods for assessing
#           agreement between two methods of clinical measurement. The lancet,
#           327(8476), 307-310.
#
#    .. [2] Giavarina, D. (2015). Understanding bland altman analysis.
#           Biochemia medica, 25(2), 141-151.
#
# last modified: 27.01.2022

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
    (average difference Ã‚Â± 1.96 standard deviation of the difference), which
    tells us how far apart measurements by 2 methods were more likely to be
    for most individuals. If the differences within mean Ã‚Â± 1.96 SD are not
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
    SizeN = 10
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
    rpc = std_diff*1.96 #return the coefficient of reproducibilit(1.96 times the standard deviation of the differnces).
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
    ax.axhline(rpc, color='k', linestyle='--', lw=1.5) #PO: line for coefficient of reproducibility

    # Annotate values
    if annotate:
        loa_range = high - low
        offset = (loa_range / 100.0) * 1.5
        trans = transforms.blended_transform_factory(
            ax.transAxes, ax.transData)
        xloc = 0.98
        xloc2=0.24
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
        ax.text(xloc2, rpc + offset, 'RPC %.1f' % rpc, ha="right", va="bottom",
                transform=trans)                                          #PO: line for coefficient of reproducibilit

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

