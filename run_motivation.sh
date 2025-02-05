#!/bin/bash


optimizers=("carbon_opt" "water_opt" "base")
thresholds=(0.01 0.1 1 10)

# Loop through each combination of optimizer and threshold
for optimizer in "${optimizers[@]}"; do
  for threshold in "${thresholds[@]}"; do
    python3 ./main.py --path="./motivations" --time_length=1440 --optimizer="$optimizer" --threshold="$threshold"
  done
done
