# multilingual-latent-concept-analysis
Code associated with the ACL24 paper titled, "Exploring Alignment in Shared Cross-Lingual Spaces" 

# Setup 

1. Clone the repo and create a conda environment

```
git clone https://github.com/qcri/multilingual-latent-concept-analysis.git
cd multilingual-latent-concept-analysis
conda env create -f environment.yml
```
2. Clone the ConceptX Repo

```
git clone https://github.com/hsajjad/ConceptX.git
```

To extract the activations, we are going to rely on a modified version of the [NeuroX library](https://github.com/fdalvi/NeuroX). The modified version is included in this repository.

# Running Activation Extraction For Concept Alignment Experiment

To extract the activations for the concept alignment experiment, run the `activation_extraction_with_filtering.sh` script. From within the script you need to specify some variables. Here's a summary of what needs to be modified

```
scriptDir: Path to the cloned ConceptX repository
inputPath: Path to the directory where data files are stored
encoder_input: name of file containing sentences to pass to the encoder of the model 
decoder_input: name of file containing sentences to pass to the decoder of the model
layer: Layer that you want to do the extraction for. 
model: model that we want to do the extraction for
model_class: class that we will use to load the model. e.g. MT5ForConditionalGeneration
NEUROX_PATH: path to the modified version of NeuroX 
mapping: FastAlign mapping used for filtering
```

# Running Activation Extraction For Concept Ovelap Experiment

To extract the activations for the concept overlap experiment, run the `activation_extraction_without_filtering.sh` script. From within the script you need to specify some variables from within the code. These varaibles are almost the same as the ones that you specified for the concept alignment experiment. 

# Clustering Representations 

To cluster the representations obtained from the extraction step, run the `clustering.sh` script. You need to pass the following variables

```
vocab_file: vocab file obtained from the activation extraction step
point_file: point file obtained from the activation extraction step
output_path: path to where we want to save the obtained cluster file
clusters: Number of clusters to cluster the representations into 
```

# Aligning Clusters

To calculate cluster alignment between two cluster files, run the `get_alignment.sh` script. You need to specify the following

```
top_n_translations: top N translations to consider
matching_threshold: The matching threshold
size_threshold: The size threshold
types: The number of types to consider
cluster_file_path1: Path to first cluster file
cluster_file_path2: Path to the second cluster file
dictionary_file_path: path to dictionary mapping words from the language of the first cluster file to the language of the second cluster
file
```
# Getting Overlapping Clusters 

To get overlapping clusters in one cluster file, run the `get_overlap.sh` script. You need to specify the following 


```
clusters_path: Path to where the clusters are saved
output_path: Path to where we want to save the overlapping clusters
clusters_threshold: Threshold to consider that the concept is overlapping between two languages
sentences_threshold: Threshold at which the sentences are split into two different languages
```