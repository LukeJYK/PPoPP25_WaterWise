#!/bin/bash

optimizers_with_path1=("least_load" "round_robin")
path1="./other_logs"
node_capacity1=35

optimizers_with_path2=("waterwise" "base" "carbon_opt" "water_opt")
path2_util5="./util5"
path2_util25="./util25"
node_capacity2_util5=75
node_capacity2_util25=20
threshold=0.5
trace_name="borg"

for optimizer in "${optimizers_with_path1[@]}"; do
    python3 ./main.py --optimizer="$optimizer" --path="$path1" --node_capacity="$node_capacity1" --trace_name="$trace_name" &
done

for optimizer in "${optimizers_with_path2[@]}"; do
    python3 ./main.py --optimizer="$optimizer" --path="$path2_util5" --node_capacity="$node_capacity2_util5" --trace_name="$trace_name" --threshold="$threshold" &
done

for optimizer in "${optimizers_with_path2[@]}"; do
    python3 ./main.py --optimizer="$optimizer" --path="$path2_util25" --node_capacity="$node_capacity2_util25" --trace_name="$trace_name" --threshold="$threshold" &
done

wait
