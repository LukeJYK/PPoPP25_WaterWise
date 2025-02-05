
import fire
from optimizer import carbon_opt,base, water_opt, least_load, round_robin, waterwise
from utils import get_transfer,get_carbon_intensity, get_ewif, get_wsf,get_wue,read_selected_traces, profile, get_wi
regions = ["zurich","madrid","oregon","milan","mumbai"]
utilization = {"zurich": 0, "madrid": 0, "oregon": 0, "milan": 0, "mumbai": 0}



def main(
    optimizer: str = "waterwise",
    lambda_ref: float = 0.1,
    trace_name: str = "borg",
    PUE: float = 1.2,
    lambda_carbon: float = 0.5,
    lambda_water: float = 0.5,
    time_length: int = 60*24*10,
    node_capacity: int = 35,#260
    threshold: int = 0.5,#from 0-1
    time_window: int =10,
    seed: int = 40,
    path: str = "./results/"
):
    print("."*16+"Setting the required parameters."+"."*16)
    ci = get_carbon_intensity(regions)
    ewif = get_ewif(regions)
    wue = get_wue(regions)
    wsf = get_wsf(regions)
    wi_wsf = get_wi(regions,ewif, wsf, wue, PUE)
    
    ## embodied carbon and embodied water footprint
    unit_embodied_carbon = 1633982/4/365/24/60/60
    unit_embodied_water = 2*1633982/747/4/365/24/60/60
    trace, name = read_selected_traces(which_trace=trace_name)

    latency = get_transfer()
    energy, exe_time = profile()
    #using optimizer for optimizing
    print("."*16+"Finish setting, start experiment."+"."*16)
    if optimizer == "waterwise":
        exp = waterwise.waterwise_optimizer(trace, path, name, seed,time_length, ci, wi_wsf,
                 node_capacity, energy, exe_time, unit_embodied_carbon, unit_embodied_water, 
                 latency, threshold, time_window, lambda_carbon, lambda_water, lambda_ref)
        exp.optimize_process()
    elif optimizer == "carbon_opt":
        print("using carbon-opt scheme")
        exp = carbon_opt.carbon_optimizer(trace, path, name, seed,time_length, ci, wi_wsf,
                                  node_capacity, energy, exe_time, unit_embodied_carbon, unit_embodied_water,
                                  latency, threshold, time_window, lambda_carbon, lambda_water)
        exp.optimize_process()
    elif optimizer == "base":
        print("using base")
        exp = base.base_optimizer(trace, path, name, seed,time_length, ci, wi_wsf,
                                  node_capacity, energy, exe_time, unit_embodied_carbon, unit_embodied_water,
                                  latency, threshold, time_window, lambda_carbon, lambda_water)
        exp.optimize_process()
    elif optimizer == "water_opt":
        print("using water-opt scheme")
        exp = water_opt.water_optimizer(trace, path, name, seed,time_length, ci, wi_wsf,
                                  node_capacity, energy, exe_time, unit_embodied_carbon, unit_embodied_water,
                                  latency, threshold, time_window, lambda_carbon, lambda_water)
        exp.optimize_process()
    elif optimizer == "least_load":
        print("using least_load scheme")
        exp = least_load.least_load_optimizer(trace, path, name, seed,time_length, ci, wi_wsf,
                                  node_capacity, energy, exe_time, unit_embodied_carbon, unit_embodied_water,
                                  latency, threshold, time_window, lambda_carbon, lambda_water)
        exp.optimize_process()
    elif optimizer == "round_robin":
        print("using round_robin scheme")
        exp = round_robin.robin_optimizer(trace, path, name, seed,time_length, ci, wi_wsf,
                                  node_capacity, energy, exe_time, unit_embodied_carbon, unit_embodied_water,
                                  latency, threshold, time_window, lambda_carbon, lambda_water)
        exp.optimize_process()
    else:
        raise ValueError("Invalid optimizer")
if __name__ == "__main__":
    fire.Fire(main)
