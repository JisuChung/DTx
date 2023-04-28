"""
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

bad_list = []
temp_list = []
mm.pd_print_all()

cwd = os.getcwd()
# print(cwd)

# print(a)
# pd.options.display.float_format = '{:,.0f}'.format

# print(file_N)
"""=====================Variables===================="""
mode = "boat"
skip_main_compiler = False

"""=====================MAIN========================="""
if skip_main_compiler == False:
    root = 'C:/Users/Minu Kim/Desktop/work/SNU/220502_tonghap_exp/analysis_clean_up/'
    data = mm.csv_compiler((root+'boat_raw/'))
    data.to_excel((root+'boat_raw_compiled.xlsx'), index=False)

if mode == "boat":
    fl_data = data.loc[:, ("id*", "distractor", "target", "main_prac", "set", "fl_corr", "fl_rt",
                           "flanker_main_loop.thisTrialN", "flanker_prac_loop.thisTrialN", "targ.started")]
    #fl_data = fl_data.loc[fl_data['main_prac'] == "main"]

    fl_data = fl_data.rename(index=str, columns={"id*": "id", "flanker_main_loop.thisTrialN": "trial_num",
                                                 "flanker_prac_loop.thisTrialN": "prac_num", "targ.started": "targ_time"})
    fl_data = fl_data.rename(index=str, columns={"fl_rt": "rt"})
    fl_data = fl_data.rename(index=str, columns={"fl_corr": "acc"})
    fl_data["trial_num"] = fl_data.trial_num.combine_first(fl_data.prac_num)
    del fl_data["prac_num"]
    fl_data = fl_data.dropna()
    fl_data = fl_data[(fl_data['targ_time'] != 'None')]

    fl_data["rt"] = 1000 * fl_data["rt"]
    fl_data['acc'] = fl_data['acc'].map({0: 1, 1: 0})
    fl_data["rt"] = fl_data["rt"].round(decimals=0)

    fl_data = fl_data.astype({'targ_time': 'float'})
    fl_data["targ_time"] = fl_data["targ_time"].round(decimals=3)
    #fl_data = fl_data.loc[fl_data['target'] != "neutral"]
    #fl_data = fl_data.loc[fl_data['distractor'] != "neutral"]
    fl_data['cong'] = ""

    cong = []
    fl_data = fl_data.reset_index(drop=True)
    for ii, jj in enumerate(fl_data['distractor']):
        if fl_data.at[ii, 'target'] == 'negative' and fl_data.at[ii, 'distractor'] == 'negative':
            cong.append("neg_cong")
        elif fl_data.at[ii, 'target'] == 'negative' and fl_data.at[ii, 'distractor'] == 'positive':
            cong.append('neg_incong')
        elif fl_data.at[ii, 'target'] == 'negative' and fl_data.at[ii, 'distractor'] == 'neutral':
            cong.append('neg_base')
        elif fl_data.at[ii, 'target'] == 'positive' and fl_data.at[ii, 'distractor'] == 'positive':
            cong.append("pos_cong")
        elif fl_data.at[ii, 'target'] == 'positive' and fl_data.at[ii, 'distractor'] == 'negative':
            cong.append('pos_incong')
        elif fl_data.at[ii, 'target'] == 'positive' and fl_data.at[ii, 'distractor'] == 'neutral':
            cong.append('pos_base')
        elif fl_data.at[ii, 'target'] == 'neutral' and fl_data.at[ii, 'distractor'] == 'neutral':
            cong.append('neut_base')
        elif fl_data.at[ii, 'target'] == 'neutral' and fl_data.at[ii, 'distractor'] == 'negative':
            cong.append('neut_neg')
        elif fl_data.at[ii, 'target'] == 'neutral' and fl_data.at[ii, 'distractor'] == 'positive':
            cong.append('neut_pos')

    fl_data['cong'] = cong

    fl_data.to_excel(root+'boat_compiled.xlsx', index=False)


    # outlier trimm
    data = fl_data.copy()
    data = data[data['main_prac'] == 'main']
    data_rt = data[data['acc'] == 0]

    fl_data = fl_data.reset_index(drop=True)
    iv = ["id", "target", "distractor"] # outlier rejection
    dv = 'rt'
    mad_cutoff = 3


    tail = 'twotail'
    mean_group = mm.mad_detector(data_rt, iv, dv, mad_cutoff)
    before, after = mm.remove_outlier(mean_group, data, iv, dv, tail)

    data.to_excel(root + 'boat_acc.xlsx', index=False)
    after.to_excel(root+'boat_trimmed_after.xlsx', index=False)

    print("finished")