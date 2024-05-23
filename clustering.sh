#!/bin/bash -l

#SBATCH -J sample-clustering-script 
#SBATCH -o sample-clustering-script.out
#SBATCH --mem=80GB    # amount of memory
#SBATCH -p cpu-all

conda activate neurox_pip
vocab_file=$1 # specify the path to the vocab file from the activation extraction step
point_file=$2 # specify the path to the point file from the activation extraction step
output_path=$3 # specify the path to the output file 
clusters=$4 # specify the number of clusters
python -u code/create_kmeans_clustering.py -v $vocab_file -p $point_file -o $output_path -k $clusters
