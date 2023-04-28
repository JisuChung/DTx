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
mode = "fish"
skip_main_compiler = False

"""=====================MAIN========================="""
if skip_main_compiler == False:
    root = 'C:/Users/Minu Kim/Desktop/work/SNU/220502_tonghap_exp/analysis_clean_up/'
    data = mm.csv_compiler((root+'fish_raw'))
    data.to_excel((root+'fish_compiled.xlsx'), index=False)

if mode == "fish":

    fish_data = data.loc[:, ("participant", "Condition", "CorrectResp", "FishType", "Round", "Response", "Response_4",
                             "Word", "WordCategory", "WordList", "WordReputation", "WordType", "WordValence", "slider.rt", "slider_4.rt")]

    fish_data = fish_data.rename(index=str, columns={"participant": "id",
                                                     "slider.rt": "rt",
                                                     "slider_4.rt": "rt2"})

    # fish_data = fish_data.loc[fish_data['st2_ran'] == 1]
    fish_data["rt"] = fish_data["rt"].combine_first(fish_data["rt2"])
    fish_data = fish_data.drop('rt2', axis=1)

    fish_data["Response"] = fish_data["Response"].combine_first(fish_data["Response_4"])
    fish_data = fish_data.drop('Response_4', axis=1)

    fish_data["rt"] = round(1000 * fish_data["rt"], 0)
    fish_data = fish_data.loc[fish_data['Round'] != "practice"]
    fish_data = fish_data.dropna()


    fish_data['acc'] = fish_data.apply(lambda row: 0 if row['CorrectResp'] == row['Response'] else 1, axis=1)

    conditions = [(fish_data["WordType"] == "Positive") & (fish_data["CorrectResp"] == "ScrollUp"),
                  (fish_data["WordType"] == "Positive") & (fish_data["CorrectResp"] == "ScrollDown"),
                  (fish_data["WordType"] == "NonTarget") & (fish_data["CorrectResp"] == "ScrollUp"),
                  (fish_data["WordType"] == "NonTarget") & (fish_data["CorrectResp"] == "ScrollDown"),
                  (fish_data["WordType"] == "Negative") & (fish_data["CorrectResp"] == "ScrollUp"),
                  (fish_data["WordType"] == "Negative") & (fish_data["CorrectResp"] == "ScrollDown"),
                  (fish_data["WordType"] == "Neutral") & (fish_data["CorrectResp"] == "ScrollUp"),
                  (fish_data["WordType"] == "Neutral") & (fish_data["CorrectResp"] == "ScrollDown"),
                  ]
    values = ["pos_u", "pos_d", "ntg_u", "ntg_d", "neg_u", "neg_d", "neu_u", "neu_d"]

    fish_data['new_conditions'] = np.select(conditions, values, default='none')

    fish_data.to_excel(root+'fish_compiled.xlsx', index=False)

    # outlier trimm

    fish_data_rt = fish_data[fish_data["acc"] == 0]

    iv = ["id", "new_conditions"] # outlier rejection
    dv = 'rt'
    mad_cutoff = 3
    tail = 'twotail'
    mean_group = mm.mad_detector(fish_data_rt, iv, dv, mad_cutoff)
    before, after = mm.remove_outlier(mean_group, fish_data, iv, dv, tail)
    fish_data.to_excel(root + 'fish_acc.xlsx', index=False)
    after.to_excel(root+'fish_trimmed_after.xlsx', index=False)

