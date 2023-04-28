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
mode = "st2"
skip_main_compiler = False

"""=====================MAIN========================="""
if skip_main_compiler == False:
    root = 'C:/Users/Minu Kim/Desktop/work/SNU/220502_tonghap_exp/analysis_clean_up/'
    data = mm.csv_compiler((root+'para_raw'))
    data.to_excel((root+'para_compiled.xlsx'), index=False)

if mode == "st2":


    st2_data = data.loc[:, ("id*","distractor", "main_prac", "target", "set", "st_corr", "st_rt", "st_ans",
                            "st2_main_loop.thisTrialN", "st2_prac_loop.thisIndex", "st_back.started", "st_res")]

    st2_data = st2_data.rename(index=str, columns={"id*": "id","st2_main_loop.thisTrialN": "trial_num",
                                                   "st2_prac_loop.thisIndex": "prac_num",
                                                   "st_back.started": "targ_time",
                                                   "target": "parachute",
                                                   "distractor": "face"})
    st2_data = st2_data.rename(index=str, columns={"st_rt": "rt"})
    st2_data = st2_data.rename(index=str, columns={"st_corr": "acc"})
    # st2_data = st2_data.rename(index=str, columns={"st2_main_loop.ran": "st2_ran"})
    # st2_data = st2_data.loc[st2_data['main_prac'] == "main"]
    # st2_data = st2_data.loc[st2_data['st2_ran'] == 1]
    st2_data["trial_num"] = st2_data.trial_num.combine_first(st2_data.prac_num)
    del st2_data["prac_num"]

    st2_data["rt"] = round(1000 * st2_data["rt"],0)
    st2_data['acc'] = st2_data['acc'].map({0: 1, 1: 0})
    st2_data["targ_time"] = st2_data["targ_time"].round(decimals=3)
    st2_data = st2_data.dropna()
    st2_data = st2_data[st2_data['main_prac'] == 'main']


    conditions = [(st2_data["face"] == "positive") & (st2_data["st_ans"] == "None"),
                  (st2_data["face"] == "negative") & (st2_data["st_ans"] == "None"),
                  (st2_data["face"] == "positive") & (st2_data["st_ans"] == "k"),
                  (st2_data["face"] == "negative") & (st2_data["st_ans"] == "k"),
                  ]
    values = ["ntg_pos", "ntg_neg", "tg_pos", "tg_neg"]

    st2_data['new_conditions'] = np.select(conditions, values, default='none')
    
    st2_data.to_excel(root+'para_compiled.xlsx', index=False)

    # outlier trimm
    st2_data_acc = st2_data[st2_data['st_ans'] != 'k']
    st2_data_rt = st2_data_acc[st2_data_acc['acc'] == 0]


    iv = ["id", "face"] # outlier rejection
    dv = 'rt'
    mad_cutoff = 3
    tail = 'twotail'
    mean_group = mm.mad_detector(st2_data_rt, iv, dv, mad_cutoff)
    before, after = mm.remove_outlier(mean_group, st2_data, iv, dv, tail)
    st2_data_acc.to_excel(root + 'para_acc.xlsx', index=False)
    after.to_excel(root+'para_trimmed_after.xlsx', index=False)

