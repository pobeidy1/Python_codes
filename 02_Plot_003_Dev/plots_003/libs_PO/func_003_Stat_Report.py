from matplotlib.backends.backend_pdf import PdfPages
from scipy import stats
import pingouin as pg
import fpdf
from tabulate import tabulate
import pandas as pd
from fpdf import FPDF
import time

timestr = time.strftime("%Y%m%d_%H%M%S_")
save_results_to = 'Output/'
#save_results_to = "/home/stiladmin/Insync/peyman@grievelab.com/Google Drive - Shared with me/003_4DCARE_Trials/DATA/Python_Code003_output/"

import matplotlib.pyplot as plt


def stat101(df_1, df_2, fName):
    # diff of mean
    dataset1_mean = "Mean of dataset 1 : %.2f" % df_1.mean()
    dataset1_STD = "STD  %.2f" % df_1.std()
    dataset2_mean = "Mean of dataset 2 : %.2f " % df_2.mean()
    dataset2_STD = "STD : %.2f " % df_2.std()
    mean_dif = "The difference in means is : %.2f" % (df_1.mean() - df_2.mean())
    mean_difper = "The difference in means percentage : %.2f " % ((((df_1.mean()-df_2.mean()))/df_1.mean())*100)

    # check normality
    stat1, p1 = stats.shapiro(df_1)
    stat2, p2 = stats.shapiro(df_2)
    shap_output1 = 'Dataset 1 : Statistics=%.3f, p=%.3f' % (stat1, p1)
    shap_output2 = 'Dataset 2 : Statistics=%.3f, p=%.3f' % (stat2, p2)

    # interpret
    alpha = 0.05
    if p1 > alpha:
        outputreport_p1 = ', Sample looks Gaussian (fail to reject H0)'
    if p2 > alpha:
        outputreport_p2 = ', Sample looks Gaussian (fail to reject H0)'
    if p1 < alpha:
        outputreport_p1 = ', Sample does not look Gaussian (reject H0)'
    if p2 < alpha:
        outputreport_p2 = ', Sample does not look Gaussian (reject H0)'
    print(type(df_1))

    # variance check
    # stat1v, p1v = stats.levene(df_1)
    result = pd.concat([df_1, df_2], axis=1)
    homo_var_out = pg.homoscedasticity(result, method='bartlett').round(3)  # Bartlett's test
    #ttest
    pg_ttest_out = pg.ttest(x=df_1, y=df_2).round(2)  # , paired=True, tail='two-sided')
    # res = stats.ttest_ind(df_1, df_2, equal_var=True)
    pg_mwn_out = pg.mwu(x=df_1, y=df_2).round(2)  # , paired=True, tail='two-sided')

    #dataframe to string
    pg_ttest_out_toStr = tabulate(pg_ttest_out, headers='keys', tablefmt='plain',
                                  numalign="right")  # plain 'html' jira textile
    pg_homoVar_out_toStr = tabulate(homo_var_out, headers='keys', tablefmt='plain',
                                    numalign="right")  # plain 'html' jira textile
    pg_mwn_out_toStr = tabulate(pg_mwn_out, headers='keys', tablefmt='plain',
                                  numalign="right")  # plain 'html' jira textile

    class PDF(FPDF):
        def header(self):
            # Logo
            # self.image('logo_pb.png', 10, 8, 33)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Move to the right
            self.cell(80)
            # Title
            self.cell(90, 10, fName , 1, 0, 'C')
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', 'B', 12)

    #data to get printed in the report
    text1 = "1) Evaluating the null hypothesis:  two group means are equal or not"
    pdf.set_font('Times', '', 9)

    pdf.cell(200, 10, txt=text1, ln=1, align='r')
    pdf.cell(200, 10, txt=text1, ln=1, align='r')
    pdf.cell(200, 5, txt=dataset1_mean +"+/-"+dataset1_STD, ln=1, align='r')
    pdf.cell(200, 5, txt=dataset2_mean +"+/-"+dataset2_STD, ln=1, align='r')
    pdf.cell(200, 5, txt=mean_dif, ln=1, align='r')
    pdf.cell(200, 5, txt=mean_difper, ln=1, align='r')

    text2 = "2) Observations in two groups have an approximately normal distribution (Shapiro-Wilks Test)"
    pdf.cell(200, 10, txt=text2, ln=1, align='r')
    pdf.cell(200, 5, txt=shap_output1 + outputreport_p1, align='r')
    pdf.cell(200, 5, txt=shap_output2 + outputreport_p2, align='r')

    text3 = "3) Homogeneity of variances: variances are equal between treatment groups (Bartlett Test)"
    pdf.multi_cell(200, 10, txt=text3, align='r')
    pdf.multi_cell(200, 4, txt=pg_homoVar_out_toStr, align='r')

    text4 = "4) ttest for the two groups are sampled independently from each other from the same population"
    pdf.multi_cell(200, 10, txt=text4, align='r')
    pdf.multi_cell(200, 4, txt=pg_ttest_out_toStr, align='r')

    text5 = "5) Mann-Whitney U Test"
    pdf.multi_cell(200, 10, txt=text5, align='r')
    pdf.multi_cell(200, 4, txt=pg_mwn_out_toStr, align='r')
    # for i in range(1, 41):
    #     pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
    pdf.output(save_results_to + timestr+(str(fName)+'.pdf'), 'F')
    # create a cell
#  pdf.cell(200, 10, txt=shap_output1 + outputreport_p1, ln=1, align='r')
#  pdf.cell(200, 10, txt=shap_output2 + outputreport_p2, ln=1, align='r')
# # for i in range(len(pg_ttest_out)):
#  pdf.output('tuto1.pdf', 'F')
