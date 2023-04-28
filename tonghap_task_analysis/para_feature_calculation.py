# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 10:52:30 2021

@author: cogmi
"""
import sys
sys.path.append(r'C:\Users\Minu Kim\Documents\GitHub')
import os
from os import sep
import pandas as pd
import numpy as np
import minu_modules as mm
import matplotlib.pyplot as plt
import seaborn as sns
import math
import pingouin as pg
from pingouin import multivariate_normality

cwd = os.getcwd()
bad_list = []
temp_list = []

mm.pd_print_all()

"""================ SET YOUR VARIABLES ==================="""
mode = 'facilitation' # bs, facilitation
dv = "far"  # rt, far

accurate, inaccurate = [0, 1]

acc_data = r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\para_acc.xlsx'
rt_data= r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\para_trimmed_after.xlsx'
path_of_survey = 'C:/Users/Minu Kim/Dropbox/survey_efa/online_exp_survey/total_survey.xlsx'

do_corr = False

"""=====================Processing rturacy========================="""
data = pd.read_excel(acc_data, header=0)
data_rt_after = pd.read_excel(rt_data, header=0)
## RT라면 기본적으로 제거해야 함.

if mode != 'bs':
    bs = []
else:
    bs = []
# data=data[~data['id'].isin(bs)]

if dv == 'rt':
    data_a = data[data['acc'] == accurate]
    mm.check_remove(data, data_a)
    data = data_a
    del data_a
else: pass

# Overall false alarm rate
if mode == 'bs' and dv == "far":# this is false alarm rate
    save = r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features'
    iv = ["id"]
    print(iv)
    data = data.groupby(iv)['acc'].mean()
    data = data.to_frame()
    data = data.reset_index()
    data["para_ov_far"] = round(data.acc * 100, 2)

    data = data.sort_values(by=['id']).reset_index(drop=True)
    final = data
    data = data.drop('acc', axis=1)
    data.to_excel(str(cwd) + "/features/para_bs_far.xlsx", index=False)
    # os.system("start EXCEL.EXE para_bs_far.xlsx")

# Overall RT
elif mode == 'bs' and dv =="rt":
    save = r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features'

    data = data_rt_after
    # outlier rejection
    iv = ["id"]
    print(iv)
    data = data.groupby(iv)[dv].mean()
    data = data.to_frame()
    data = data.reset_index()
    data["para_ov_rt"] = round(data["rt"], 0)
    data = data.sort_values(by=['id']).reset_index(drop=True)
    final = data
    data = data.drop('rt', axis=1)
    data.to_excel(str(cwd) + "/features/para_bs_rt.xlsx", index=False)
    # os.system("start EXCEL.EXE for_st2_bs_rt.xlsx")

# negativity bias (negative facilitation) in RT
elif mode == 'facilitation' and dv == "rt":
    save = r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features'

    data = data_rt_after
    # Select Factors
    iv = ["id", "face"]

    # data.to_excel(str(cwd) + "/for_cong.xlsx", index=False)
    data_negative = data[data['face'] == "negative"]
    data_positive = data[data['face'] == "positive"]

    data_negative = data_negative.groupby(iv)[dv].mean()
    data_negative = data_negative.to_frame()
    data_negative = data_negative.reset_index()

    data_positive = data_positive.groupby(iv)[dv].mean()
    data_positive = data_positive.to_frame()
    data_positive = data_positive.reset_index()

    nb = pd.DataFrame()
    nb["id"] = data_negative.id
    nb["para_neg_target_rt"] = round(data_negative.rt, 0)
    nb["para_pos_target_rt"] = round(data_positive.rt, 0)

    nb["para_nb_rt"] = round((data_negative.rt - data_positive.rt), 0)
    # nb["para_nb_rt"] = round(nb["nb_rt"], 0)

    final = nb
    final = final.sort_values(by=['id']).reset_index(drop=True)

    final.to_excel(str(cwd) + "/features/para_nb_rt.xlsx", index=False)
    # os.system("start EXCEL.EXE for_nb_rt.xlsx")

# negativity bias (negative facilitation) in false alarm rate
elif mode == 'facilitation' and dv == "far":
    save = r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features'

    # data = data[data["trial_targ"] == 0]
    # Select Factors
    iv = ["id", "face"]

    # data.to_excel(str(cwd) + "/for_cong.xlsx", index=False)
    data_negative = data[data['face'] == "negative"]
    data_positive = data[data['face'] == "positive"]

    data_negative = data_negative.groupby(iv)['acc'].mean()
    data_negative = data_negative.to_frame()
    data_negative = data_negative.reset_index()


    data_positive = data_positive.groupby(iv)['acc'].mean()
    data_positive = data_positive.to_frame()
    data_positive = data_positive.reset_index()

    nb = pd.DataFrame()
    nb["id"] = data_negative.id
    nb["para_neg_target_far"] = round(data_negative.acc*100, 2)
    nb["para_pos_target_far"] = round(data_positive.acc*100, 2)

    nb["para_nb_far"] = round(((data_negative.acc - data_positive.acc)*100),2)
    # nb["score"] = round(nb.nb_acc*100, 2)
    final = nb
    final = final.sort_values(by=['id']).reset_index(drop=True)

    final.to_excel(str(cwd) + "/features/para_nb_far.xlsx", index=False)
    # os.system("start EXCEL.EXE for_nb_far.xlsx")


if do_corr == True:
    survey_data = pd.read_excel(path_of_survey, header=0)
    # survey_iv = ["age", "gender", "phq9", "cesd", "stai_s", "stai_t",
    #              "dep_f1", "dep_f2", "dep_f3", "dep_f4", "dep_f5", "dep_f6",
    #              "state_f1", "state_f2", "trait_f1", "trait_f2"]

    survey_iv = ["age", "gender", "phq9", "phq_so", "phq_af", "cesd", "cesd_da", "cesd_pa", "cesd_so", "cesd_ip",
                 "stai_s", "state_pos", "state_neg", "stai_t", "trait_pos", "trait_neg"]

    bad_sub = ["610ea9a7e88bfe6cab826680", "608d247fc141c8230ce3ebdc", "5d71640e8a1bff0001d88e70"]
    survey_data = survey_data.sort_values(by=['id']).reset_index(drop=True)
    # Combine Survey Data and Scores
    survey_data["score"] = final.score

    # remove undesired data
    # survey_data = survey_data[survey_data["age"] < 50]
    survey_data = survey_data[~survey_data["id"].isin(bad_sub)]
    # survey_data, remove = mm.correlation_mad_rejection(survey_data, "score", 3, verbose=False)
    # print(remove.id)
    # PLOT HISTOGRAM OF SCORE DISTRIBUTION.
    # THE PLOT SHOULD IDEALLY LOOK LIKE A NORMAL DISTRIBUTION WITHOUT OUTLIERS.
    plt.clf()
    ax = sns.distplot(a=survey_data["score"], hist=True, kde=False, rug=False)
    plt.show()

    ## DO CORRELATIONS
    print(mode, dv)
    for i in survey_iv:
        if i == 'age' or i == "gender":

            ddd = pd.concat([survey_data[i], survey_data["score"]], axis=1).reset_index()
            ktest = multivariate_normality(ddd, alpha=.05)
            norm_p = ktest.pval
            if ktest.pval > .05: # normality assumed
                cor_method = "pearson"
                p_meth = 'pe'
            else: # normality violated
                cor_method = "spearman"
                p_meth = 'sp'
            x = ''
            r_val2 = pg.corr(survey_data.score.tolist(), survey_data[i], alternative="two-sided", method = cor_method)
            p_val = r_val2["p-val"][0]
            r_val = r_val2["r"][0]
            if p_val < .05:
                x = "*"
            print(i, round(r_val, 3), round(p_val, 3), x , p_meth)

        else:
            ddd = pd.concat([survey_data[i], survey_data["score"]], axis=1).reset_index()
            ktest = multivariate_normality(ddd, alpha=.05)
            norm_p = ktest.pval
            if ktest.pval > .05: # normality assumed
                cor_method = "pearson"
                p_meth = 'pe'
            else: # normality violated
                cor_method = "spearman"
                p_meth = 'sp'

            asdf = "part"
            x = ''
            partco = pg.partial_corr(data=survey_data, x=i, y='score', covar=['age', 'gender'], method = cor_method).round(3)
            p_val2 = partco["p-val"][0]
            r_val2 = partco["r"][0]
            if p_val2 < .05:
                x = "*"
            print(i, round(r_val2, 3), round(p_val2, 3), x, asdf, p_meth)

            # if p_val < .05:
            #     asdf = "partial"
            #     x = ''
            #     partco = pg.partial_corr(data=survey_data, x=i, y='score', covar='age').round(3)
            #     p_val2 = partco["p-val"][0]
            #     r_val2 = partco["r"][0]
            #     if p_val2 < .05:
            #         x = "*"
            #     print(i, round(r_val2, 3), round(p_val2, 3), x, asdf)
            # elif p_val >= .05:
            #     asdf = "whole"
            #     x = ''
            #     r_val2 = pg.corr(survey_data.score.tolist(), survey_data[i], alternative="two-sided")
            #     p_val2 = r_val2["p-val"][0]
            #     r_val2 = r_val2["r"][0]
            #     if p_val2 < .05:
            #         x = "*"
            #     print(i, round(r_val2, 3), round(p_val2, 3), x, asdf)

        # ### Plotting ###
        plt.figure(figsize=(3, 3))
        plt.clf()
        reg_x = survey_data.loc[:, [i]]
        reg_y = survey_data.loc[:, ['score']]
        ax = sns.regplot(x=reg_x, y=reg_y, ci=68, truncate=False)
        plt.tight_layout()

        savename = save + mode +"_"+ dv+"_" + str(i) + ".png"
        fig_save_name = savename
        plt.savefig(fig_save_name)

breakpoint()