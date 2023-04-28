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

from matplotlib import rcParams
cwd = os.getcwd()
bad_list = []
temp_list = []

mm.pd_print_all()

"""================ SET YOUR VARIABLES ==================="""
mode = 'congruency'  # bs, all_groups, congruency
dv = "bins"  # acc, rt, bins
do_corr = False

acc_filename = r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\boat_acc.xlsx'
rt_filename = r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\boat_trimmed_after.xlsx'
path_of_survey = 'C:/Users/Minu Kim/Dropbox/survey_efa/online_exp_survey/total_survey.xlsx'

"""=====================Processing rturacy========================="""
acc_data = pd.read_excel(acc_filename, header=0)
rt_data = pd.read_excel(rt_filename, header=0)

if dv == 'rt':
    data = rt_data
elif dv == 'acc':
    data = acc_data

if mode == 'bs' and dv == "acc":
    save = r"C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features"
    iv = ["id"]
    data = data.groupby(iv)[dv].mean()
    data = data.to_frame()
    data = data.reset_index()
    data["para_ov_pe"] = round(data.acc*100, 2)
    data = data.sort_values(by=['id']).reset_index(drop=True)
    data = data.drop('acc', axis=1)

    data.to_excel(str(cwd) + "/features/boat_bs_acc.xlsx", index=False)

    final = data
    # os.system("start EXCEL.EXE para_overall_acc.xlsx")

elif mode == 'bs' and dv =="rt":
    save = r"C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features"

    # indipendent variable
    iv = ["id"]#outlier rejection
    # grouping
    after=data.copy()
    after = after.groupby(iv)[dv].mean()
    after = after.to_frame()
    after = after.reset_index()
    after["scpara_ov_rt"] = round(after["rt"], 0)
    after = after.sort_values(by=['id']).reset_index(drop=True)
    after = after.drop('rt', axis=1)
    after.to_excel(str(cwd) + "/features/boat_bs_rt.xlsx", index=False)
    final = after
    # os.system("start EXCEL.EXE for_bs_rt.xlsx")

elif mode =='congruency' and dv == "acc":
    save = r"C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features"

    iv = ["id", "cong"]
    grand_conditions = ["cong"]
    data_cong = data[(data['cong'] == "pos_cong") | (data['cong'] == "neg_cong")]
    data_incong = data[(data['cong'] == "pos_incong") | (data['cong'] == "neg_incong")]

    cong = data_cong.groupby("id")[dv].mean()
    cong = cong.to_frame()
    cong = cong.reset_index()
    cong['acc'] = round(cong['acc'] * 100, 2)

    incong = data_incong.groupby("id")[dv].mean()
    incong = incong.to_frame()
    incong = incong.reset_index()
    incong['acc'] = round(incong['acc'] * 100, 2)

    congruency = pd.DataFrame()
    congruency["id"] = cong.id
    congruency["boat_cong_acc"] = cong.acc
    congruency["boat_incong_acc"] = incong.acc
    congruency["boat_congruency_acc"] = round((incong.acc - cong.acc), 2)
    congruency = congruency.sort_values(by=['id']).reset_index(drop=True)
    final = congruency

    congruency.to_excel(str(cwd) + "/features/boat_congruency_acc.xlsx", index=False)
    # os.system("start EXCEL.EXE for_congruency_acc.xlsx")

    # input = congruency.congruency_acc

elif mode =='congruency' and dv == "rt":
    save = r"C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features"
    "Select Factors"
    iv = ["id", "cong"]

    # data.to_excel(str(cwd) + "/for_cong.xlsx", index=False)
    data_cong = data[(data['cong'] == "pos_cong") | (data['cong'] == "neg_cong")]
    data_incong = data[(data['cong'] == "pos_incong") | (data['cong'] == "neg_incong")]

    cong = data_cong.groupby("id")[dv].mean()
    cong = cong.to_frame()
    cong = cong.reset_index()

    incong = data_incong.groupby("id")[dv].mean()
    incong = incong.to_frame()
    incong = incong.reset_index()

    congruency = pd.DataFrame()
    congruency["id"] = cong.id
    congruency["boat_cong_rt"] = round(cong.rt, 0)
    congruency["boat_incong_rt"] = round(incong.rt, 0)

    congruency["boat_congruency_rt"] = round((incong.rt - cong.rt), 0)
    congruency = congruency.sort_values(by=['id']).reset_index(drop=True)
    final = congruency

    congruency.to_excel(str(cwd) + "/features/boat_congruency_rt.xlsx", index=False)
    # os.system("start EXCEL.EXE for_congruency_rt.xlsx")

elif mode == 'congruency' and dv == "bins":
    save = r"C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features"
    blank = pd.DataFrame()

    ids = acc_data.id.unique()
    ids = ids.tolist()

    for i, j in enumerate(ids):

        ## step 1 - calculate mean rt for congruent
        id_data = rt_data[rt_data['id'] == j]
        cong_data = id_data[(id_data['cong'] == 'neg_cong') | (id_data['cong'] == 'post_cong')]
        cong_rt = cong_data.rt.mean()
        cong_rt = round(cong_rt, 0)

        ## step 2 - subtract mean rt for congruent from trial rt for incongruent.
        incong_data = id_data[(id_data['cong'] == 'neg_incong') | (id_data['cong'] == 'post_incong')]
        incong_data["rt"] = incong_data.rt - cong_rt

        temp = [blank, incong_data]
        blank = pd.concat(temp)

    ## step 3 - Binning into 10 percentiles.
    blank["bin"] = pd.qcut(blank.rt, 10, labels=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    ## step 4 - add 20 for each inaccurate trail

    id_list = []
    score_list = []
    for i, j in enumerate(ids):

        indiv_blank = blank[blank['id'] == j]

        bin_score = sum(indiv_blank.bin)

        id_acc_data = acc_data[acc_data['id'] == j]

        acc_incong = id_acc_data[(id_acc_data['cong'] == 'pos_incong') & (id_acc_data['cong'] == 'neg_incong')]
        acc_incong = acc_incong[acc_incong['acc'] == 1]

        # pos_cong = pos_data[pos_data['cong'] == 'cong']
        # pos_cong = pos_cong[pos_cong['acc'] == 1]

        count = acc_incong.acc.sum()
        print(count)
        bin_score = bin_score + (count * 20)

        id_list.append(j)
        score_list.append(bin_score)

    final = pd.DataFrame(list(zip(id_list, score_list)), columns=["id","score"])

    final = final.sort_values(by=['id']).reset_index(drop=True)
    final.to_excel(str(cwd) + "/features/boat_congruency_bin.xlsx", index=False)
    # os.system("start EXCEL.EXE cong_bin.xlsx")

if do_corr == True:
    survey_data = pd.read_excel(path_of_survey, header=0)
    survey_iv = ["age", "gender", "phq9", "phq_so", "phq_af", "cesd", "cesd_da", "cesd_pa", "cesd_so", "cesd_ip",
                 "stai_s", "state_pos", "state_neg", "stai_t", "trait_pos", "trait_neg"]
    bs = ["610ea9a7e88bfe6cab826680", "608d247fc141c8230ce3ebdc", "5d71640e8a1bff0001d88e70"]
    survey_data = survey_data.sort_values(by=['id']).reset_index(drop=True)
    #Combine Survey Data and Scores
    survey_data["score"] = final.score


    # remove undesired data
    # survey_data = survey_data[survey_data["age"] < 50]
    survey_data = survey_data[~survey_data["id"].isin(bs)]
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

        # if i == 'age':
        #     x = ''
        #     r_val2 = pg.corr(survey_data.score.tolist(), survey_data[i], alternative="two-sided")
        #     p_val = r_val2["p-val"][0]
        #     r_val = r_val2["r"][0]
        #     if p_val < .05:
        #         x = "*"
        #     print(i, round(r_val, 2), round(p_val, 2), x)
        #
        # elif i != 'age':
        #     if p_val < .05:
        #         asdf = "partial"
        #         x = ''
        #         partco = pg.partial_corr(data=survey_data, x=i, y='score', covar='age').round(3)
        #         p_val2 = partco["p-val"][0]
        #         r_val2 = partco["r"][0]
        #         if p_val2 < .05:
        #             x = "*"
        #         print(i, round(r_val2, 2), round(p_val2, 2), x, asdf)
        #     elif p_val >= .05:
        #         asdf = "whole"
        #         x = ''
        #         r_val2 = pg.corr(survey_data.score.tolist(), survey_data[i], alternative="two-sided")
        #         p_val2 = r_val2["p-val"][0]
        #         r_val2 = r_val2["r"][0]
        #         if p_val2 < .05:
        #             x = "*"
        #         print(i, round(r_val2, 2), round(p_val2, 2), x, asdf)

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