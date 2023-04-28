"""
"""
import sys
sys.path.append(r'C:\Users\Minu Kim\Desktop\py_modules')
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
mode = "weather" #compile
submode= 'congruency_score'
root = 'C:/Users/Minu Kim/Desktop/work/SNU/220502_tonghap_exp/analysis_trial2/weather_analysis/'
"""=====================MAIN========================="""
if mode == 'compile':
    data = mm.csv_compiler((root+'raw/'))
    data.to_excel((root+'raw_compiled.xlsx'), index=False)

# # breakpoint()
if mode == "weather":
    filename= root+'raw_compiled2.xlsx'
    data = pd.read_excel(filename, header=0)
    data["weather"] = (data.valence * data.relevance)
    indiv_conditions = ["participant"]
    dependent_variable = "weather"
    rtsss = data.groupby(indiv_conditions)[dependent_variable].mean()
    rtsss = rtsss.to_frame()
    rtsss = rtsss.reset_index()
    rtsss["weather"] = round(rtsss.weather,3)

    rtsss.to_excel(root+'weather.xlsx', index=False)
    
    breakpoint()

    
#     """===RT==="""
#     dependent_variable = "rt"

#     if submode == 'overall_rt':
#         indiv_conditions = ["participant"]
#         # 전체 rt
#         data = data[(data['acc'] == 0)]
        
#         print(indiv_conditions)
#         rtsss = data.groupby(indiv_conditions)[dependent_variable].median()
#         print(rtsss)
#         rtsss = rtsss.to_frame()
#         rtsss = rtsss.reset_index()
#         rtsss.to_excel(root + "/" + submode +"_" + dependent_variable + ".xlsx", index=False)
#         plt.figure(figsize=(3.5, 5))
#         pltsss = sns.violinplot(y=dependent_variable, data=rtsss, inner=None, color=".8")
#         pltss = sns.stripplot(y=dependent_variable, data=rtsss)
#         plt.show()

#     # negative rt
#     if submode == 'negative_rt':
#         indiv_conditions = ["participant"]
#         # 전체 rt
#         data = data[(data['acc'] == 0)]
#         data = data[(data['WordType'] == "Negative")]

#         print(indiv_conditions)
#         rtsss = data.groupby(indiv_conditions)[dependent_variable].median()
#         print(rtsss)
#         rtsss = rtsss.to_frame()
#         rtsss = rtsss.reset_index()
#         rtsss.to_excel(root + "/" + submode +"_" + dependent_variable + ".xlsx", index=False)
#         plt.figure(figsize=(3.5, 5))
#         pltsss = sns.violinplot(y=dependent_variable, data=rtsss, inner=None, color=".8")
#         pltss = sns.stripplot(y=dependent_variable, data=rtsss)
#         plt.show()


#     # positive rt

#     if submode == 'positive_rt':
#         indiv_conditions = ["participant"]
#         # 전체 rt
#         data = data[(data['acc'] == 0)]
#         data = data[(data['WordType'] == "Positive")]

#         print(indiv_conditions)
#         rtsss = data.groupby(indiv_conditions)[dependent_variable].median()
#         print(rtsss)
#         rtsss = rtsss.to_frame()
#         rtsss = rtsss.reset_index()
#         rtsss.to_excel(root + "/" + submode +"_" + dependent_variable + ".xlsx", index=False)
#         plt.figure(figsize=(3.5, 5))
#         pltsss = sns.violinplot(y=dependent_variable, data=rtsss, inner=None, color=".8")
#         pltss = sns.stripplot(y=dependent_variable, data=rtsss)
#         plt.show()

#     # negative cong

#     if submode == 'negative_cong':
#         indiv_conditions = ["participant", "Condition"]
#         # 전체 rt
#         data = data[(data['acc'] == 0)]
#         data = data[(data['WordType'] == "Negative")]
#         data = data[(data['Condition'] == "Congruent")]

#         print(indiv_conditions)
#         rtsss = data.groupby(indiv_conditions)[dependent_variable].median()
#         print(rtsss)
#         rtsss = rtsss.to_frame()
#         rtsss = rtsss.reset_index()
#         rtsss.to_excel(root + "/" + submode +"_" + dependent_variable + ".xlsx", index=False)
#         plt.figure(figsize=(3.5, 5))
#         pltsss = sns.violinplot(y=dependent_variable, data=rtsss, inner=None, color=".8")
#         pltss = sns.stripplot(y=dependent_variable, data=rtsss)
#         plt.show()
        
#     # negative incong
#     if submode == 'negative_incong':
#         indiv_conditions = ["participant", "Condition"]
#         # 전체 rt
#         data = data[(data['acc'] == 0)]
#         data = data[(data['WordType'] == "Negative")]
#         data = data[(data['Condition'] == "Inongruent")]

#         print(indiv_conditions)
#         rtsss = data.groupby(indiv_conditions)[dependent_variable].median()
#         print(rtsss)
#         rtsss = rtsss.to_frame()
#         rtsss = rtsss.reset_index()
#         rtsss.to_excel(root + "/" + submode +"_" + dependent_variable + ".xlsx", index=False)
#         plt.figure(figsize=(3.5, 5))
#         pltsss = sns.violinplot(y=dependent_variable, data=rtsss, inner=None, color=".8")
#         pltss = sns.stripplot(y=dependent_variable, data=rtsss)
#         plt.show()
        
#     # negative congruency score
#     if submode == 'negative_congruency_score':
#         indiv_conditions = ["participant", "Condition"]
#         # 전체 rt
#         data = data[(data['acc'] == 0)]
#         data["rt"] = round(data.rt * 1000)
        
#         mads, mads_upper, sss = mm.sd_detector(data, ['participant', 'Condition'], 'rt', thresh=2, verbose=False)
#         # breakpoint()
#         blank=[]
#         for i, rw in data.iterrows():
#             thresh = mm.get_multi_value2('participant', rw['participant'], 'Condition', rw['Condition'], mads_upper)
    
#             # print(thresh)
#             if rw['rt'] > thresh.iloc[0]['rt_upper']:
#                 blank.append(-1)
#             elif rw['rt'] < thresh.iloc[0]['rt_lower']:
#                 blank.append(-1)
#             else:
#                 blank.append(rw['rt'])
#         data["trim_rt"] = blank
#         data = data.loc[data['trim_rt'] != -1]
        
        
#         #breakpoint()
#         data = data[(data['WordType'] == "Negative")]
#         cong_data = data[(data['Condition'] == "Congruent")]
#         incong_data = data[(data['Condition'] == "Incongruent")]

#         print(indiv_conditions)
#         cong_med = cong_data.groupby(indiv_conditions)[dependent_variable].mean()
#         incong_med = incong_data.groupby(indiv_conditions)[dependent_variable].mean()
        
#         cong_med = cong_med.to_frame()
#         cong_med = cong_med.reset_index()
#         incong_med = incong_med.to_frame()
#         incong_med = incong_med.reset_index()
        
       
#         cong_med["Incong"] = incong_med.rt
#         cong_med["score"] = incong_med.rt - cong_med.rt
#         cong_med["score"] = round(cong_med.score, 0)
#         cong_med.to_excel(root + "/" + submode +"_" + dependent_variable + ".xlsx", index=False)


#     if submode == 'congruency_score':
#         indiv_conditions = ["participant", "Condition"]
#         # 전체 rt
#         data = data[(data['acc'] == 0)]
        
        
#         data["rt"] = round(data.rt * 1000,0)
        
        
#         mads, mads_upper, sss = mm.sd_detector(data, ['participant', 'Condition'], 'rt', thresh=2, verbose=False)
#         # breakpoint()
#         blank=[]
#         for i, rw in data.iterrows():
#             thresh = mm.get_multi_value2('participant', rw['participant'], 'Condition', rw['Condition'], mads_upper)
    
#             # print(thresh)
#             if rw['rt'] > thresh.iloc[0]['rt_upper']:
#                 blank.append(-1)
#             elif rw['rt'] < thresh.iloc[0]['rt_lower']:
#                 blank.append(-1)
#             else:
#                 blank.append(rw['rt'])
#         data["trim_rt"] = blank
#         data = data.loc[data['trim_rt'] != -1]
        
        
#         # data = data[(data['WordType'] == "Negative")]
#         cong_data = data[(data['Condition'] == "Congruent")]
#         incong_data = data[(data['Condition'] == "Incongruent")]

#         print(indiv_conditions)
#         cong_med = cong_data.groupby(indiv_conditions)[dependent_variable].mean()
#         incong_med = incong_data.groupby(indiv_conditions)[dependent_variable].mean()
        
#         cong_med = cong_med.to_frame()
#         cong_med = cong_med.reset_index()
#         incong_med = incong_med.to_frame()
#         incong_med = incong_med.reset_index()
        
#         cong_med["Incong"] = incong_med.rt
#         cong_med["score"] = incong_med.rt - cong_med.rt
#         cong_med["score"] = round(cong_med.score, 0)
#         cong_med.to_excel(root + "/" + submode +"_" + dependent_variable + ".xlsx", index=False)



#     # positive cong

#     # positive incong

#     # positive congruency score

#     # release rt

#     # catch rt

#     """===ACC==="""
#     # 전체 ACC

#     # negative ACC

#     # positive ACC

#     # negative cong

#     # negative incong

#     # negative congruency score

#     # positive cong

#     # positive incong

#     # positive congruency score

#     # release acc

#     # catch acc

#     #     #data = data.loc[data['main_prac'] == "main"]
# #
# #     data = data.rename(index=str, columns={"id*": "id", "flanker_main_loop.thisTrialN": "trial_num",
# #                                                  "flanker_prac_loop.thisTrialN": "prac_num", "targ.started": "targ_time"})
# #     data = data.rename(index=str, columns={"fl_rt": "rt"})
# #     data = data.rename(index=str, columns={"fl_corr": "acc"})
# #     data["trial_num"] = data.trial_num.combine_first(data.prac_num)
# #     del data["prac_num"]
# #     data = data.dropna()
# #     data = data[(data['targ_time'] != 'None')]
# #
# #     data["rt"] = 1000 * data["rt"]
# #     data['acc'] = data['acc'].map({0: 1, 1: 0})
# #     data["rt"] = data["rt"].round(decimals=0)
# #
# #     data = data.astype({'targ_time': 'float'})
# #     data["targ_time"] = data["targ_time"].round(decimals=3)
# #     #data = data.loc[data['target'] != "neutral"]
# #     #data = data.loc[data['distractor'] != "neutral"]
# #     data['cong'] = ""
# #
# #     cong = []
# #     data = data.reset_index(drop=True)
# #
# #     for ii, jj in enumerate(data['distractor']):
# #         if data.at[ii, 'distractor'] == 'negative' and data.at[ii, 'target'] == 'negative':
# #             cong.append("cong")
# #         elif data.at[ii, 'distractor'] == 'positive' and data.at[ii, 'target'] == 'positive':
# #             cong.append("cong")
# #         elif data.at[ii, 'distractor'] == 'negative' and data.at[ii, 'target'] == 'positive':
# #             cong.append('incong')
# #         elif data.at[ii, 'distractor'] == 'positive' and data.at[ii, 'target'] == 'negative':
# #             cong.append('incong')
# #         else:
# #             cong.append('neut')
# #     data['cong'] = cong
# #     print(data)
# #    data.to_excel(root+'fl_compiled.xlsx', index=False)
# #     print("finished")


# print("end")