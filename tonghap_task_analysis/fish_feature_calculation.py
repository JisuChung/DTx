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
mode = 'bs' # bs, facilitation
dv = "rt"  # rt, acc

accurate, inaccurate = [0, 1]

acc_data = r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\fish_acc.xlsx'
rt_data= r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\fish_trimmed_after.xlsx'
path_of_survey = 'C:/Users/Minu Kim/Dropbox/survey_efa/online_exp_survey/total_survey.xlsx'

"""=====================Processing rturacy========================="""
data = pd.read_excel(acc_data, header=0)
data_rt_after = pd.read_excel(rt_data, header=0)
## RT라면 기본적으로 제거해야 함.


# Overall false alarm rate
if mode == 'bs' and dv == "acc":# this is false alarm rate
    save = r'C:\Users\Minu Kim\Desktop\work\SNU\220502_tonghap_exp\analysis_clean_up\features'
    iv = ["id"]
    print(iv)

    data = data.groupby(iv)['acc'].mean()
    data = data.to_frame()
    data = data.reset_index()
    data["fish_ov_pe"] = round((data.acc * 100), 2)
    data = data.sort_values(by=['id']).reset_index(drop=True)
    final = data
    data = data.drop('acc', axis=1)

    data.to_excel(str(cwd) + "/features/fish_bs_pe.xlsx", index=False)
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
    data["fish_ov_rt"] = round(data["rt"], 0)
    data = data.sort_values(by=['id']).reset_index(drop=True)
    final = data
    data = data.drop('rt', axis=1)
    data.to_excel(str(cwd) + "/features/fish_bs_rt.xlsx", index=False)
    # os.system("start EXCEL.EXE for_st2_bs_rt.xlsx")

breakpoint()