#!/bin/bash
thresholds=("0.25" "0.5" "0.75" "1")
optimizers=("carbon_opt" "water_opt" "base" "waterwise")
for optimizer in "${optimizers[@]}"; do
  for threshold in "${thresholds[@]}"; do
    # Run the command in parallel
    python3 ./main.py --optimizer="$optimizer" --path="./fig5_logs" --node_capacity=35 --trace_name="borg" --threshold="$threshold" &
  done
done
wait
