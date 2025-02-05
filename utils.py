from pathlib import Path
import os
import json
import numpy as np
import pandas as pd
regions = ["zurich","madrid","oregon","milan","mumbai"]

def profile():
    energy = {}
    exe_time = {}
    funcs = ["graph","memory", "cache","serving","media","black","canneal","dedup","netdedup","swaptions"]
    for fun in funcs:
        with open(f'{Path(__file__).parents[0]}/profile_data/{fun}_energy.json', 'r') as file1:
            data1 = json.load(file1)
        energy[fun] = [data_engergy/3600/1000 for data_engergy in data1]
        with open(f'{Path(__file__).parents[0]}/profile_data/{fun}_time.json', 'r') as file2:
            data2 = json.load(file2)
        exe_time[fun] = [data_time for data_time in data2]
    return energy, exe_time

def get_transfer():
    with open('./data/transfer.json', 'r') as file:
        data = json.load(file)
    return data

def get_wsf(regions):
    with open(f'{Path(__file__).parents[0]}/data/region_mix_2023.json', 'r') as file:
        region_data = json.load(file)
    return {region: region_data[region]["wsf"] for region in regions}

def get_carbon_intensity(regions):
    region_ci = {}
    for region in regions:
        region_ci[region] =  []
        with open(f'{Path(__file__).parents[0]}/data/ci/{region}.txt', 'r') as file:
            for line in file:      
                num = float(line.strip()) 
                for _ in range(60):
                    region_ci[region].append(num)
    return region_ci

def get_wue(regions):
    region_wue = {}
    for region in regions:
        region_wue[region] =  []
      
        with open(f'{Path(__file__).parents[0]}/data/wet_bulb/{region}.txt', 'r') as file:
            for line in file:      
                num = float(line.strip()) 
                s=3
                tw = (num*9/5)+32
                factor = s/(s-1)
                wue = factor*(6*(10**-5)*tw**3-0.01*tw**2+0.61*tw-10.4)
                if region!="mumbai":
                    for _ in range(60):
                        region_wue[region].append(wue)
                else:
                    for _ in range(180):
                        region_wue[region].append(wue)
    return region_wue

def get_ewif(regions):
    region_ewif = {}
    for region in regions:
        region_ewif[region] =  []
        with open(f'{Path(__file__).parents[0]}/data/ewif/{region}.txt', 'r') as file:
            for line in file:      
                num = float(line.strip()) 
                for _ in range(60):
                    region_ewif[region].append(num)
    return region_ewif

def read_selected_traces(which_trace):
    app_lst = ["black", "cache","canneal","dedup","graph","memory","serving","media","netdedup","swaptions"]
    directory_path = f"{Path(__file__).parents[0]}/{which_trace}_trace/"
    all_trace = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            df = pd.read_csv(file_path,header=None)
            column_data = df.iloc[:, 0].tolist()
            all_trace.append(column_data)
    return all_trace, app_lst

def check_capacity(regions, capacity, time):
    cap = {}
    for region in regions:
        cap[region] = 0
        for avail_time in capacity[region]:
            if avail_time <= time:
                cap[region] += 1
    return cap

def get_wi(regions,ewif, wsf, wue, pue):
    length = len(ewif[regions[0]])
    wi = {}
    for region in regions:
        wi[region] = []
        for i in range(length):
            wi[region].append((wue[region][i]+pue*ewif[region][i])*(1+wsf[region])) 
    return wi
            



                
def update_capacity(dst, current_time, region_capacity_data, exe_time):
    dst_region = regions[dst]
    for index, avail_time in enumerate(region_capacity_data[dst_region  ]):
        if avail_time <= current_time:
            region_capacity_data[dst_region][index] = current_time + exe_time
            break
        else:
            continue
    return region_capacity_data