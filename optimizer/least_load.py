import sys
sys.path.append("..")
from request import get_request
import utils
import json
import numpy as np
import random
import os
import tqdm
class least_load_optimizer():
    def __init__(self, 
                 trace, 
                 path,
                 name,  
                 seed,
                 time_length, 
                 ci,
                 wi_wsf,
                 node_capacity, 
                 energy, 
                 exe_time, 
                 unit_embodied_carbon, 
                 unit_embodied_water, 
                 latency, 
                 threshold, 
                 time_window, 
                 lambda_carbon, 
                 lambda_water):
        self.time_length = time_length
        self.regions = ["zurich","madrid","oregon","milan","mumbai"]
        
        self.ci = ci
        self.wi_wsf = wi_wsf
        self.trace = trace
        self.name = name
        self.seed = seed   
        self.energy = energy
        self.exe_time = exe_time
        self.region_capacity = {region: [0 for _ in range(node_capacity)] for region in self.regions}
        self.unit_embodied_carbon = unit_embodied_carbon
        self.unit_embodied_water = unit_embodied_water
        self.latency = latency
        self.threshold = threshold
        self.time_window = time_window
        self.lambda_carbon = lambda_carbon
        self.lambda_water = lambda_water
        self.path = path

    def optimize_process(self):
        sum_job = 0
        result_carbon ={}
        result_water = {}
        result_time = {}
        for i in range(self.time_length):
            result_carbon[i] = []
            result_water[i] = []
            result_time[i] = []

        delayed_requests = []

        for j in tqdm.tqdm(range(self.time_length)): 
            current_ci = {region: self.ci[region][j] for region in self.regions}
            current_wi_real = {region: self.wi_wsf[region][j] for region in self.regions}
            num_invokes = [int(self.trace[i][j]) for i in range(len(self.trace)) if int(self.trace[i][j]) !=0]
            sum_job += sum(num_invokes)
            requests_name = [self.name[i] for i in range(len(self.trace))  if int(self.trace[i][j]) !=0]
            request_name_extend = [name for name, times in zip(requests_name, num_invokes) for _ in range(times)]
            requests, prefer_requests = get_request(self.seed, request_name_extend, j,delayed_requests)
      
            assert(len(prefer_requests) == 0 )
            assert sum(num_invokes)+len(delayed_requests) == (len(requests)+len(prefer_requests))

            capacity_num = utils.check_capacity(self.regions,self.region_capacity, j)
            if sum(capacity_num.values())>=len(requests):
                for req in requests:
                    capacity_num = utils.check_capacity(self.regions,self.region_capacity, j)
                    #find least loaded region
                    region = max(capacity_num, key=capacity_num.get)
                    sample_index = random.randint(0, 99)
                    sample_energy = self.energy[req.id][sample_index]
                    sample_exe_time = self.exe_time[req.id][sample_index]
                    result_carbon[j].append((req.seq,region,sample_energy*current_ci[region]+self.unit_embodied_carbon*sample_exe_time))
                    result_water[j].append((req.seq,region, sample_energy*current_wi_real[region]+self.unit_embodied_water*sample_exe_time))
                    result_time[j].append((
                                req.seq,
                                region,
                                np.mean(self.exe_time[req.id]),
                                sample_exe_time+(self.latency[req.id][req.src][region]+(j-req.start)*60)
                                ))
                            #update:
                    exe_t = sample_exe_time/60
                    self.region_capacity = utils.update_capacity(self.regions.index(region),j, self.region_capacity, exe_t)
                    #update capacity
                    
                delayed_requests = []
                
            else:
                ongoing_requests = requests[:sum(capacity_num.values())]
                delayed_requests = requests[sum(capacity_num.values()):]
                for req in ongoing_requests:
                    capacity_num = utils.check_capacity(self.regions,self.region_capacity, j)
                    region = max(capacity_num, key=capacity_num.get)
                    sample_index = random.randint(0, 99)
                    sample_energy = self.energy[req.id][sample_index]
                    sample_exe_time = self.exe_time[req.id][sample_index]
                    result_carbon[j].append((req.seq,region,sample_energy*current_ci[region]+self.unit_embodied_carbon*sample_exe_time))
                    result_water[j].append((req.seq,region, sample_energy*current_wi_real[region]+self.unit_embodied_water*sample_exe_time))
                    result_time[j].append((
                                req.seq,
                                region,
                                np.mean(self.exe_time[req.id]),
                                sample_exe_time+(self.latency[req.id][req.src][region]+(j-req.start)*60)
                                ))
                            #update:
                    exe_t = sample_exe_time/60
                    self.region_capacity = utils.update_capacity(self.regions.index(region),j, self.region_capacity, exe_t)
           
            
        if not os.path.exists(f"{self.path}/least_load/"):
            os.makedirs(f"{self.path}/least_load/")
        with open(f"{self.path}/least_load/carbon.json", "w") as file:
            json.dump(result_carbon, file, indent=4)
        with open(f"{self.path}/least_load/water.json", "w") as file:
            json.dump(result_water, file, indent=4)
        with open(f"{self.path}/least_load/time.json", "w") as file:
            json.dump(result_time, file, indent=4)

