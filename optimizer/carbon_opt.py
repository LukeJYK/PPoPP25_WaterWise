import sys
import pulp
sys.path.append("..")
from request import get_request
import tqdm
import json
import numpy as np
import math
import os
class carbon_optimizer():
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
        self.node_capacity = node_capacity
        self.path =path

    def optimize_process(self):
        allowance = self.threshold
        #init slot for every available nodes across regions
        avail_slot = [{"zurich": self.node_capacity,  "madrid": self.node_capacity, "oregon":self.node_capacity, "milan": self.node_capacity, "mumbai": self.node_capacity} for _ in range(self.time_length)]
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
            num_invokes = [int(self.trace[i][j]) for i in range(len(self.trace)) if int(self.trace[i][j]) !=0]
            sum_job += sum(num_invokes)
            requests_name = [self.name[i] for i in range(len(self.trace))  if int(self.trace[i][j]) !=0]
            request_name_extend = [name for name, times in zip(requests_name, num_invokes) for _ in range(times)]
            requests, prefer_requests = get_request(self.seed, request_name_extend,j,delayed_requests)
            #sort it based on exe time
            req_exe = []
            ci_lst = []
            for region in self.regions:
                ci_lst.append(self.ci[region][j])
            for request in requests:
                req_exe.append(request.start)
            request_score_pairs = list(zip(requests, req_exe))  
            sorted_request_score_pairs = sorted(request_score_pairs, key=lambda pair: pair[1], reverse=False)
            after_sort_req = [pair[0] for pair in sorted_request_score_pairs]
            
            for sig_req in after_sort_req:
                end_time_region = {"zurich": [j,0],  "madrid": [j,0], "oregon":[j,0], "milan": [j,0], "mumbai": [j,0]}
                allow_time = (allowance)*np.mean(self.exe_time[sig_req.id])
                for region in self.regions:
                    end_time = math.floor(j+ (allow_time-self.latency[sig_req.id][sig_req.src][region])/60)
                    if end_time >= self.time_length:
                        end_time = self.time_length-1
                    end_time_region[region][1] = end_time
                min_intensity = float('inf')
                best_location = None
                best_time = None
                for location in self.ci:
                    period = end_time_region[location]
                    for time in range(period[0], period[1] + 1):
                        if avail_slot[time][location] > 0:
                            intensity =self.ci[location][time]
                            if intensity < min_intensity:
                                min_intensity = intensity
                                best_location = location
                                best_time = time
                
                if best_location is None:
                    if sig_req not in delayed_requests:
                    
                    #print(avail_slot[j])
                        delayed_requests.append(sig_req)
                    continue
                else: 
                    if sig_req in delayed_requests:
                        delayed_requests.remove(sig_req)
                    result_carbon[j].append((best_location,np.mean(self.energy[sig_req.id])*min_intensity+self.unit_embodied_carbon*np.mean(self.exe_time[sig_req.id])))
                    result_water[j].append((best_location,np.mean(self.energy[sig_req.id])*self.wi_wsf[best_location][best_time]+self.unit_embodied_water*np.mean(self.exe_time[sig_req.id])))
                    result_time[j].append((best_location, np.mean(self.exe_time[sig_req.id]), np.mean(self.exe_time[sig_req.id])+60*(best_time -sig_req.start)+self.latency[sig_req.id][sig_req.src][best_location]))
                #update
                finish_time = math.floor(best_time+np.mean(self.exe_time[sig_req.id])/60 +self.latency[sig_req.id][sig_req.src][best_location]/60)
                if finish_time >= self.time_length:
                    finish_time = self.time_length-1
                update_period = [best_time, finish_time]
                for k in range(update_period[0], update_period[1]+1):
                    avail_slot[k][best_location] -= 1

        if not os.path.exists(f"{self.path}/carbon_opt/"):
            os.makedirs(f"{self.path}/carbon_opt/")
        with open(f"{self.path}/carbon_opt/carbon_{self.threshold+1}.json", "w") as file:
            json.dump(result_carbon, file, indent=4)
        with open(f"{self.path}/carbon_opt/water_{self.threshold+1}.json", "w") as file:
            json.dump(result_water, file, indent=4)
        with open(f"{self.path}/carbon_opt/time_{self.threshold+1}.json", "w") as file:
            json.dump(result_time, file, indent=4)