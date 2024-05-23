#!/bin/bash -l


#SBATCH -p cpu-all

top_n_translations="" 
matching_threshold=""
size_threshold=""
types=""
cluster_file_path1=""
cluster_file_path2=""
dictionary_file_path=""

python -u "code/alignClusters.py" $cluster_file_path1 $cluster_file_path2 $dictionary_file_path $top_n_translations $matching_threshold $size_threshold $types
