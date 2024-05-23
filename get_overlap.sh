#!/bin/bash -l


#SBATCH -p cpu-all





clusters_path=""
output_path=""
clusters_threshold=""
sentences_threshold=""

python -u "code/get_overlapping_clusters.py" --cluster_file $clusters_path --output_path $output_path --clusters_threshold $clusters_threshold --sentences_threshold $sentences_threshold
