'''
This code is used to generate the discrete expert walking data,
which includes the velocity, acceleration, direction, and gait pattern.

The data is saved in the folder 'expert_demonstration/expert/' with the name of the data source.
The plots of the continuous data and the histogram of the binned data are saved in the folder 
'expert_demonstration/expert/plot/walking_dynamic_parameters/'.

The data source can be 'all' or 'one insect'.
'''

import os
import sys
sys.path.append("./") # add the root directory to the python path
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from plot_expert import *
import yaml


def get_cont_data(subject:str, trim=False, trim_len:int=0):
    with open("configs/trail_details.json", "r") as f:
        trail_details = json.load(f)
    insect_name = trail_details[f"T{subject}"]["insect_name"]
    insect_number = trail_details[f"T{subject}"]["insect_number"]
    id_1 = trail_details[f"T{subject}"]["id_1"]
    id_2 = trail_details[f"T{subject}"]["id_2"]
    id_3 = trail_details[f"T{subject}"]["id_3"]
    vel_path = os.path.join("expert_data_builder/stick_insect", insect_name,
                                                    f"{insect_number}_{id_1}_{id_2}_{id_3}_vel.csv")
    direction_path = os.path.join("expert_data_builder/stick_insect", insect_name,
                                                    f"{insect_number}_{id_1}_{id_2}_{id_3}_direction.csv")
    gait_path = os.path.join("expert_data_builder/stick_insect", insect_name,
                                                    f"{insect_number}_{id_1}_{id_2}_{id_3}_gait.csv")
    # the first value of vel and the last value of gait are not valid
    vel = pd.read_csv(vel_path, header=[0], index_col=None).to_numpy()[1:-1]
    direction = pd.read_csv(direction_path, header=[0], index_col=None).to_numpy()[1:-1]
    gait = pd.read_csv(gait_path, header=[0], index_col=None).to_numpy()[1:-1]
    if trim:
        vel = vel[:-trim_len]
        direction = direction[:-trim_len]
        gait = gait[:-trim_len]
    return vel, direction, gait

def calculate_acceleration(vel):
    # frequency = 200 Hz
    acc = np.diff(vel, axis=0) / 0.005
    return acc

def load_antenna_dist(subject:str):
    with open("configs/trail_details.json", "r") as f:
        trail_details = json.load(f)
    insect_name = trail_details[f"T{subject}"]["insect_name"]
    insect_number = trail_details[f"T{subject}"]["insect_number"]
    id_1 = trail_details[f"T{subject}"]["id_1"]
    id_2 = trail_details[f"T{subject}"]["id_2"]
    id_3 = trail_details[f"T{subject}"]["id_3"]
    antenna_path = os.path.join("expert_data_builder/stick_insect", insect_name,
                                                    f"{insect_number}_{id_1}_{id_2}_{id_3}_antenna_dist.csv")
    antenna = pd.read_csv(antenna_path, header=[0], index_col=None).to_numpy()
    return antenna


with open('configs/irl.yml') as file:
    v = yaml.load(file, Loader=yaml.FullLoader)

# # When the data source is [all]
# # Load the dataset
# data_source = str(v['data_source'])
# No1, No2, No3 = v[data_source]['No1'], v[data_source]['No2'], v[data_source]['No3']
# No13, No14, No15 = v[data_source]['No13'], v[data_source]['No14'], v[data_source]['No15']
# No25, No26, No27 = v[data_source]['No25'], v[data_source]['No26'], v[data_source]['No27']
# # Get the continuous data
# vel_01, direction_01, gait_01 = get_cont_data(No1)
# vel_02, direction_02, gait_02 = get_cont_data(No2)
# vel_03, direction_03, gait_03 = get_cont_data(No3)
# acc_01, acc_02, acc_03 = calculate_acceleration(vel_01), calculate_acceleration(vel_02), calculate_acceleration(vel_03)
# vel_13, direction_13, gait_13 = get_cont_data(No13)
# vel_14, direction_14, gait_14 = get_cont_data(No14)
# vel_15, direction_15, gait_15 = get_cont_data(No15)
# acc_13, acc_14, acc_15 = calculate_acceleration(vel_13), calculate_acceleration(vel_14), calculate_acceleration(vel_15)
# if data_source == 'C00':
#     vel_25, direction_25, gait_25 = get_cont_data(No25, trim=True, trim_len=800)
#     vel_26, direction_26, gait_26 = get_cont_data(No26, trim=True, trim_len=2200)
#     vel_27, direction_27, gait_27 = get_cont_data(No27, trim=True, trim_len=1600)
#     acc_25, acc_26, acc_27 = calculate_acceleration(vel_25), calculate_acceleration(vel_26), calculate_acceleration(vel_27)
# else:
#     vel_25, direction_25, gait_25 = get_cont_data(No25)
#     vel_26, direction_26, gait_26 = get_cont_data(No26)
#     vel_27, direction_27, gait_27 = get_cont_data(No27)
#     acc_25, acc_26, acc_27 = calculate_acceleration(vel_25), calculate_acceleration(vel_26), calculate_acceleration(vel_27)
# vel = np.concatenate((vel_01[1:], vel_02[1:], vel_03[1:], vel_13[1:], vel_14[1:], vel_15[1:], vel_25[1:], vel_26[1:], vel_27[1:]), axis=0)
# direction = np.concatenate((direction_01[1:], direction_02[1:], direction_03[1:], direction_13[1:], direction_14[1:], direction_15[1:], direction_25[1:], direction_26[1:], direction_27[1:]), axis=0)
# gait = np.concatenate((gait_01[1:], gait_02[1:], gait_03[1:], gait_13[1:], gait_14[1:], gait_15[1:], gait_25[1:], gait_26[1:], gait_27[1:]), axis=0)
# acc = np.concatenate((acc_01, acc_02, acc_03, acc_13, acc_14, acc_15, acc_25, acc_26, acc_27), axis=0)
# print("flatten trajectory length: ", len(acc))


# When the data source is [one insect]
# Load the dataset
data_source = str(v['data_source'])
No1, No2, No3 = v[data_source]['No1'], v[data_source]['No2'], v[data_source]['No3']
# Get the continuous data
if data_source == 'MedauroideaC00':
    vel_01, direction_01, gait_01 = get_cont_data(No1, trim=True, trim_len=800)
    vel_02, direction_02, gait_02 = get_cont_data(No2, trim=True, trim_len=2200)
    vel_03, direction_03, gait_03 = get_cont_data(No3, trim=True, trim_len=1600)
    acc_01, acc_02, acc_03 = calculate_acceleration(vel_01), calculate_acceleration(vel_02), calculate_acceleration(vel_03)
else:
    vel_01, direction_01, gait_01 = get_cont_data(No1)
    vel_02, direction_02, gait_02 = get_cont_data(No2)
    vel_03, direction_03, gait_03 = get_cont_data(No3)
    acc_01, acc_02, acc_03 = calculate_acceleration(vel_01), calculate_acceleration(vel_02), calculate_acceleration(vel_03)
vel = np.concatenate((vel_01[1:], vel_02[1:], vel_03[1:]), axis=0)
direction = np.concatenate((direction_01[1:], direction_02[1:], direction_03[1:]), axis=0)
gait = np.concatenate((gait_01[1:], gait_02[1:], gait_03[1:]), axis=0)
acc = np.concatenate((acc_01, acc_02, acc_03), axis=0)
print("length of T"+No1+", T"+No2+", T"+No3+": ", len(acc_01), len(acc_02), len(acc_03))
print("length of faltten trajectory:", len(acc))


# bin the data
vel_start, vel_end, vel_step = v[data_source]['vel_bin_params']
direction_start, direction_end, direction_step = v[data_source]['direction_bin_params']
acc_start, acc_end, acc_step = v[data_source]['acc_bin_params']
vel_bin_edges = np.arange(vel_start, vel_end, vel_step) # the end value should be 1 unit larger
vel_binned = np.digitize(vel, vel_bin_edges, right=True)
direction_bin_edges = np.arange(direction_start, direction_end, direction_step)
direction_binned = np.digitize(direction, direction_bin_edges, right=True)
acc_bin_edges = np.arange(acc_start, acc_end, acc_step)
acc_binned = np.digitize(acc, acc_bin_edges, right=True)
# print binned group
direction_bin_group = np.unique(direction_binned)
vel_bin_group = np.unique(vel_binned)
acc_bin_group = np.unique(acc_binned)
print("direction binned group: ", direction_bin_group)
print("vel binned group: ", vel_bin_group)
print("acc binned group: ", acc_bin_group)
plot_bins_histogram(vel_binned, title='Discrete Velocity Data Distribution', xlabel='Velocity', bin_step=5, savename=data_source+'_histogram_vel')
plot_bins_histogram(direction_binned, title='Discrete Direction Data Distribution', xlabel='Direction', bin_step=5, savename=data_source+'_histogram_direction')
plot_bins_histogram(acc_binned, title='Discrete Acceleration Data Distribution', xlabel='Acceleration', bin_step=250, savename=data_source+'_histogram_acc')

# Load grouped gait combinations (6 types)
grouped_gait_combinations = v['grouped_gait_combinations']
# Combine the first six columns into a string for each row to represent the gait pattern
gait_data = pd.DataFrame(gait)
gait_data['Gait Pattern'] = gait_data.iloc[:, :6].astype(str).agg(''.join, axis=1)
# Categorize each gait pattern based on the possible combinations
gait_data['Category'] = gait_data['Gait Pattern'].map(grouped_gait_combinations).astype(int)
# Display the categorized data
print(gait_data[['Gait Pattern', 'Category']])

# Combine velocity, direction, and gait pattern into a single DataFrame for analysis
analysis_df = pd.DataFrame({
        'Velocity Bin': vel_binned.flatten(),
        'Acceleration Bin': acc_binned.flatten(),
        'Direction Bin': direction_binned.flatten(),
        'Gait Category': gait_data['Category']
    })

save = True
if save:
    save_path = 'expert_demonstration/expert/'+data_source+'.csv'
    analysis_df.to_csv(save_path, index=False, header=True)

# data curve visualization (for slides)
plot_data_curve(vel_03, direction_03, acc_03, data_source)