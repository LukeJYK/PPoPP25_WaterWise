import sys
sys.path.append("..")
from request import get_request
import utils
import json
import numpy as np
import random
import tqdm
import os
class base_optimizer():
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
        utilization = {"zurich": 0, "madrid": 0, "oregon": 0, "milan": 0, "mumbai": 0}
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

            start_time = []
            for request in requests:
                start_time.append(request.start)
            #sort the requests based on the start time
            request_score_pairs = list(zip(requests, start_time))  
            sorted_request_score_pairs = sorted(request_score_pairs, key=lambda pair: pair[1])
            sorted_requests = [pair[0] for pair in sorted_request_score_pairs]
            remain_requests= []
            for sig_req in sorted_requests:
                dst = sig_req.src
                capacity_num = utils.check_capacity(self.regions,self.region_capacity, j)
                if capacity_num[dst]>0:
                    sample_index = random.randint(0, 99)
                    sample_energy = self.energy[sig_req.id][sample_index]
                    sample_exe_time = self.exe_time[sig_req.id][sample_index]
                    result_carbon[j].append((sig_req.seq,dst,sample_energy*current_ci[dst]+self.unit_embodied_carbon*sample_exe_time))
                    result_water[j].append((sig_req.seq,dst,sample_energy*current_wi_real[dst]+self.unit_embodied_water*sample_exe_time))
                    result_time[j].append((
                        sig_req.seq,
                        dst,
                        np.mean(self.exe_time[sig_req.id]),
                        sample_exe_time+(self.latency[sig_req.id][sig_req.src][dst]+(j-sig_req.start)*60)
                         ))
                    #update:
                    exe_t = sample_exe_time/60
                    self.region_capacity = utils.update_capacity(self.regions.index(dst),j, self.region_capacity, exe_t)
                    utilization[dst] += 1
                    
                else:
                    remain_requests.append(sig_req)
            delayed_requests = remain_requests
        if not os.path.exists(f"{self.path}/base/"):
            os.makedirs(f"{self.path}/base/")
        with open(f"{self.path}/base/carbon.json", "w") as file:
            json.dump(result_carbon, file, indent=4)
        with open(f"{self.path}/base/water.json", "w") as file:
            json.dump(result_water, file, indent=4)
        with open(f"{self.path}/base//time.json", "w") as file:
            json.dump(result_time, file, indent=4)


