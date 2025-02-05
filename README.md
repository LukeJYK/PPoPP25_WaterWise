# WaterWise: Co-optimizing Carbon- and Water-Footprint Toward Environmentally Sustainable Cloud Computing


## Description
The carbon and water footprint of large-scale computing systems poses serious environmental sustainability risks. In this study, we discover that, unfortunately, carbon and water sustainability are at odds with each other – and, optimizing one alone hurts the other. Toward that goal, we introduce, WaterWise, a novel job scheduler for parallel workloads that intelligently co-optimizes carbon and water footprint to improve the sustainability of geographically distributed data centers. 

## Artifact Dependencies and Setup Process
There are no memory or CPU limitations. Our evaluation was conducted on a 5-core CPU with 16 GB. Python version 3.8.11 is used, and the required packages are listed in `requirements.txt`. Install all required packages using:
```bash
pip install -r requirements.txt
```
After installation, you are ready to run the trace simulation and experiments.


## Data and Directory Introduction
-   **Traces**: In this work, we use the Google Borg ([https://github.com/google/cluster-data](https://github.com/google/cluster-data)) trace and Alibaba VM Cloud Trace ([https://github.com/alibaba/clusterdata](https://github.com/alibaba/clusterdata)) for experiments. The dataset includes ten days of data with over 230,000 jobs. The traces can be found under `./borg_trace` and `./alibaba_trace`.
-   **Carbon, Water, and Energy Data**: Wet bulb temperature is obtained from a public dataset ([https://meteologix.com/no](https://meteologix.com/no)). Carbon intensity and Energy Water Intensity Factor (EWIF) are calculated using data from Electricity Map ([https://app.electricitymaps.com/map/24h](https://app.electricitymaps.com/map/24h)). Energy data is measured using AWS m5.metal instances and is stored in `./profile_data`. All regions are assumed to have 35 nodes (for a total of 35 × 5 = 175 nodes).
-   **Output Logs**: All output logs include information about the carbon and water footprints of executing specific jobs. After running experiments, the results will be saved in the designated output directory.
-   **Scripts and Code**:
    -   `utils.py`: Contains helper functions for running the main function (`main.py`).
    -   `./optimizer`: Includes all designed optimizers.
    -   Shell scripts in the project are used to reproduce the results.


## Running WaterWise and Verifying Results
To run WaterWise, use the following command:
```bash
python3 ./main.py --optimizer=<OPTIMIZER> \
  --path=<PATH> --node_capacity=<NUM> \ 
  --trace_name=<TRACE> --PUE=<NUM> \ 
  --lambda_carbon=<NUM> --lambda_water=<NUM> \ 
  --lambda_ref=<NUM> --seed=<NUM> \ 
  --time_window=<NUM> --threshold=<NUM> \ 
  --time_length=<NUM>
```
-   `optimizer`: Specifies the optimizer to use with WaterWise.
-   `path`: Specifies the directory where the results are saved.
-   `node_capacity`: Influences the utilization of the clusters. In our experiments, it is set to 35.
-   `trace_name`: Specifies the trace to use (`Borg` or `Alibaba`).
-   `PUE`: Power Usage Effectiveness (set to 1.2 in the paper).
-   `lambda_carbon` and `lambda_water`: Control the weights for carbon and water optimization. Ensure the sum is 1.
-   `lambda_ref`: Controls the influence of historical data on the optimization process.
-   `seed`: Sets the random seed for reproducibility.
-   `time_window`: In our setting, it is set to 10.
-   `threshold`: Controls delay tolerance.
-   `time_length`: Specifies the simulation length in minutes. For example, for 10 days, set `time_length = 24 * 60 * 10`.