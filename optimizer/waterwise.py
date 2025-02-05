import sys
import pulp
sys.path.append("..")
from request import get_request
import utils
import json
import numpy as np
import random
import time
import tqdm
import os

class waterwise_optimizer():
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
                 lambda_water, 
                 lambda_future):
        self.time_length = time_length     
        self.regions = ["zurich","madrid","oregon","milan","mumbai"]
        self.ci = ci
        self.wi_wsf = wi_wsf
        self.trace = trace
        self.name = name
        self.path = path
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
        self.lambda_future = lambda_future
        self.history_obj =[]

    def optimize_process(self):
        penalty = 10
        
        sum_job = 0
        self.result_carbon ={}
        self.result_water = {}
        self.result_time = {}
        self.result_overhead = []
        for i in range(self.time_length):
            self.result_carbon[i] = []
            self.result_water[i] = []
            self.result_time[i] = []
        delayed_requests = []
    

        for j in tqdm.tqdm(range(self.time_length)): 
            start = time.time()
            lambda_carbon = self.lambda_carbon
            lambda_water = 1- lambda_carbon
            
            current_ci = {region: self.ci[region][j] for region in self.regions}
            current_wi_wsf = {region: self.wi_wsf[region][j] for region in self.regions}
            
            num_invokes = [int(self.trace[i][j]) for i in range(len(self.trace)) if int(self.trace[i][j]) !=0]
            sum_job += sum(num_invokes)
            requests_name = [self.name[i] for i in range(len(self.trace))  if int(self.trace[i][j]) !=0]
            request_name_extend = [name for name, times in zip(requests_name, num_invokes) for _ in range(times)]
            requests, prefer_requests = get_request(self.seed, request_name_extend, j,delayed_requests)

            assert(len(prefer_requests) == 0 )
            assert sum(num_invokes)+len(delayed_requests) == (len(requests)+len(prefer_requests))
            capacity_num = utils.check_capacity(self.regions,self.region_capacity, j)
            
   
            if len(requests)>sum(capacity_num.values()):
                #print("The capacity is not enough.")
                top_n_requests, delayed_requests = self.queue_requests(requests, capacity_num, j)
                request_score, request_latency = self.get_score(top_n_requests, current_ci, current_wi_wsf, lambda_carbon, lambda_water)
                x = self.run_solver(request_score, request_latency, top_n_requests, capacity_num, penalty)
                self.update_result(current_ci, current_wi_wsf, top_n_requests, x, j, lambda_carbon, lambda_water)
            else:
                request_score, request_latency = self.get_score(requests, current_ci, current_wi_wsf, lambda_carbon, lambda_water)
                x = self.run_solver(request_score, request_latency, requests, capacity_num, penalty)
                self.update_result(current_ci, current_wi_wsf, requests, x, j, lambda_carbon, lambda_water)
                delayed_requests = []
            self.result_overhead.append(time.time()-start)
    
        if not os.path.exists(f"{self.path}/waterwise/"):
            os.makedirs(f"{self.path}/waterwise/")
        with open(f"{self.path}/waterwise/carbon_{self.threshold+1}.json", "w") as file:
            json.dump(self.result_carbon, file, indent=4)
        with open(f"{self.path}/waterwise/water_{self.threshold+1}.json", "w") as file:
            json.dump(self.result_water, file, indent=4)
        with open(f"{self.path}/waterwise//time_{self.threshold+1}.json", "w") as file:
            json.dump(self.result_time, file, indent=4)
        with open(f"{self.path}/waterwise/overhead_{self.threshold+1}.json", "w") as file:
            json.dump(self.result_overhead, file, indent=4)
    
    def queue_requests(self, requests, capacity_num, time_step):
        '''
        queueing requests, because the capacity has a limitation.
        '''
        available_region = [region for region in self.regions if capacity_num[region] > 0]
        # getting the urgency score
        urgency_score = []
        for request in requests:
            avg_latency = []
            for region in available_region:
                #compute avg latency
                avg_latency.append(self.latency[request.id][request.src][region])
            urgency_score.append( (self.threshold)*np.mean(self.exe_time[request.id]) - np.mean(avg_latency)- 60*(time_step-request.start))
        request_score_pairs = list(zip(requests, urgency_score))    
        sorted_request_score_pairs = sorted(request_score_pairs, key=lambda pair: pair[1])
        top_n_requests = [pair[0] for pair in sorted_request_score_pairs[:sum(capacity_num.values())]]
        remain_requests = [pair[0] for pair in sorted_request_score_pairs[sum(capacity_num.values()):]]
        return top_n_requests, remain_requests
    
    
    def get_score(self, requests, current_ci, current_wi_wsf, lambda_carbon, lambda_water):
        '''
        Using the optimization objective to calculate the score for different requests under different scenarios.
        '''
        score = [[]for i in range(len(requests))]
        req_energy = []
        req_exe = []
        
        max_ci = max(current_ci.values())
        max_wi = max(current_wi_wsf.values())

        for i in range(len(requests)):
            req_energy.append(np.mean(self.energy[requests[i].id]))
            req_exe.append(np.mean(self.exe_time[requests[i].id]))
        
        max_water = [sig_energy*max_wi +self.unit_embodied_water*np.mean(self.exe_time[requests[index].id]) for index,sig_energy in enumerate(req_energy)]
        max_carbon = [sig_energy*max_ci+self.unit_embodied_carbon*np.mean(self.exe_time[requests[index].id])  for index,sig_energy in enumerate(req_energy)]

        assert len(req_energy) == len(max_carbon) 
        request_latency = [[] for i in range(len(requests))]
        for i in range(len(req_energy)):
            name_info = requests[i].id
            for region in self.regions:
                request_latency[i].append(self.latency[requests[i].id][requests[i].src][region])
                carbon_part =(current_ci[region]*req_energy[i]+self.unit_embodied_carbon*np.mean(self.exe_time[name_info]))
                water_part = (current_wi_wsf[region]*req_energy[i]+self.unit_embodied_water*np.mean(self.exe_time[name_info]))
                carbon_part = carbon_part/max_carbon[i]
                water_part = water_part/max_water[i]
                if len(self.history_obj) == 0:
                    score[i].append(lambda_carbon*carbon_part + lambda_water*water_part)
                else:
                    combined ={}
                    for d in self.history_obj:
                        for k, lst in d.items():
                            if k in combined:
                                combined[k].extend(lst)
                            else:
                                combined[k] = lst.copy()
                    if len(combined[region]) == 0:
                        score[i].append(lambda_carbon*carbon_part + lambda_water*water_part)
                    else:
                        
                        score[i].append(lambda_carbon*carbon_part + lambda_water*water_part +self.lambda_future*np.mean(combined[region]))
        return score, request_latency
    
    
    def run_solver(self, request_score, request_latency, request, capacity_num, penalty):
        '''
        This function is running MILP solver to solve the optimization problem. 
        '''
        prob1 = pulp.LpProblem("Request_Assignment_Problem", pulp.LpMinimize)
        x = [[pulp.LpVariable(f"x_{m}_{n}", cat="Binary") for n in range(len(self.regions))] for m in range(len(request))]
        prob1+= pulp.lpSum(request_score[m][n] * x[m][n] for m in range(len(request)) for n in range(len(self.regions)))
        for m in range(len(request)):
            prob1 += pulp.lpSum(x[m][n] for n in range(len(self.regions))) == 1
        for n in range(len(self.regions)):
            region_name = self.regions[n]
            prob1 += pulp.lpSum(x[m][n] for m in range(len(request))) <= capacity_num[region_name]
        #add sla
        for m in range(len(request)):
            for n in range(len(self.regions)):
                if request_latency[m][n]/np.mean(self.exe_time[request[m].id]) >= self.threshold:
                    prob1 += x[m][n] == 0         
        status = prob1.solve(pulp.PULP_CBC_CMD(msg=False))
        if status == pulp.LpStatusInfeasible:
            #use another solver
            prob2 = pulp.LpProblem("Request_Assignment_Problem", pulp.LpMinimize)
            x = [[pulp.LpVariable(f"x_{m}_{n}", cat="Binary") for n in range(len(self.regions))] for m in range(len(request))]
            slack = [[pulp.LpVariable(f"slack_{m}_{n}", lowBound=0) for n in range(len(self.regions))] for m in range(len(request))]
            prob2+= pulp.lpSum(request_score[m][n] * x[m][n] for m in range(len(request)) for n in range(len(self.regions)))\
                + penalty * pulp.lpSum(slack[m][n] for m in range(len(request)) for n in range(len(self.regions)))
            for m in range(len(request)):
                prob2 += pulp.lpSum(x[m][n] for n in range(len(self.regions))) == 1
            
            for n in range(len(self.regions)):
                region_name = self.regions[n]
                prob2 += pulp.lpSum(x[m][n] for m in range(len(request))) <= capacity_num[region_name]
            #add sla
            for m in range(len(request)):
                for n in range(len(self.regions)):
                        prob2 +=  slack[m][n]>= (request_latency[m][n] / np.mean(self.exe_time[request[m].id])) - self.threshold
            status = prob2.solve(pulp.PULP_CBC_CMD(msg=False))
            if status == pulp.LpStatusInfeasible:
                sys.exit("Definatly wrong!")

        return x
    
    
    
    def update_result(self, current_ci, current_wi_wsf, requests, x, time_step, lambda_carbon, lambda_water):
        '''
        Update the results and the history reference. The results will be saved.
        '''
        counts = [0] * len(self.regions)
        carbon_water_hist = {region: [] for region in self.regions}
        max_ci = max(current_ci.values())
        max_wi = max(current_wi_wsf.values())
        for m in range(len(requests)):
            for n in range(len(self.regions)):
                if pulp.value(x[m][n]) == 1: ## index out of Range???
                    dst = n 
                    # check the capacity
                    check_num = utils.check_capacity(self.regions,self.region_capacity, time_step)
                    if check_num[self.regions[dst]] == 0:
                        sys.exit("Definatly wrong! Your system broken!")
                    sample_index = random.randint(0, 99)
                    sample_energy = np.mean(self.energy[requests[m].id])
                    sample_exe_time = self.exe_time[requests[m].id][sample_index]
                    avg_exe_time = np.mean(self.exe_time[requests[m].id])
                    exe_t = (sample_exe_time + self.latency[requests[m].id][requests[m].src][self.regions[n]])/60
                    #update the capacity
                    self.region_capacity = utils.update_capacity(dst,time_step, self.region_capacity, exe_t)
                    counts[n] += 1
                    self.result_carbon[time_step].append((requests[m].seq,self.regions[n],sample_energy*current_ci[self.regions[n]]+self.unit_embodied_carbon*sample_exe_time))
                    self.result_water[time_step].append((requests[m].seq,self.regions[n],sample_energy*current_wi_wsf[self.regions[n]]+self.unit_embodied_water*sample_exe_time))
                    self.result_time[time_step].append((
                        requests[m].seq,
                        self.regions[n],
                        avg_exe_time,
                        self.latency[requests[m].id][requests[m].src][self.regions[n]]+sample_exe_time,
                        self.latency[requests[m].id][requests[m].src][self.regions[n]]+ 60*(time_step-requests[m].start) + sample_exe_time,
                        sample_exe_time
                        ))
                    carbon_water_hist[self.regions[n]].append(lambda_carbon*(sample_energy* current_ci[self.regions[n]]+self.unit_embodied_carbon*sample_exe_time)/ \
                                                (max_ci*sample_energy+self.unit_embodied_carbon*sample_exe_time) + lambda_water* \
                                                (sample_energy*current_wi_wsf[self.regions[n]]+self.unit_embodied_water*sample_exe_time)/ \
                                                (max_wi*sample_energy+self.unit_embodied_water*sample_exe_time))
                    if len(self.history_obj)==self.time_window:
                        self.history_obj.pop(0)
                        self.history_obj.append(carbon_water_hist)
                    else:
                        self.history_obj.append(carbon_water_hist)
                        
