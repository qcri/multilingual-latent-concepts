#!/bin/bash -l

conda activate neurox_pip

scriptDir=""   # path to ConceptX script directory
inputPath=""       # path to where the sentences are stored
encoder_input="" # Encoder sentences   
decoder_input=""  # Decoder sentences

# Filtering parameters; set the layer according to the layer that you want to extract for
sentence_length=300 
minfreq=0 
maxfreq=15
delfreq=10000000 
layer=0
# define the path/or huggingface identifier of the model
model=""
model_class=""
# Define the path of the NeuroX modified directory 
NEUROX_PATH=""

# Define the mapping for the filetering
mapping=""

encoder_working_file=$encoder_input.tok.sent_len
decoder_working_file=$decoder_input.tok.sent_len

cp ${inputPath}/$encoder_input $encoder_input.tok
cp ${inputPath}/$decoder_input $decoder_input.tok


# Do sentence length filtering and keep sentences max length of {sentence_length}
python "code/parallel_sentence_length.py" --encoder_input $encoder_input.tok --decoder_input $decoder_input.tok --encoder_output_file $encoder_working_file --decoder_output_file  $decoder_working_file --length ${sentence_length}

PYTHONPATH=$NEUROX_PATH python -u -m neurox.data.extraction.transformers_extractor "${model},${model},${model_class}" ${encoder_working_file}  ${decoder_working_file} activations.json --output_type json --seq2seq_component both --decompose_layers --filter_layers ${layer}

# Create a dataset file with word and sentence indexes
python ${scriptDir}/create_data_single_layer.py --text-file ${encoder_working_file} --activation-file encoder-activations-layer${layer}.json --output-prefix ${encoder_working_file} 
python ${scriptDir}/create_data_single_layer.py --text-file ${decoder_working_file} --activation-file decoder-activations-layer${layer}.json --output-prefix ${decoder_working_file}


# Filter number of tokens to fit in the memory for clustering. Input file will be from step 4

python -u "code/parallel_frequency_filter_data.py" --src-dataset ${encoder_working_file}-dataset.json --src-sentences ${encoder_working_file}-sentences.json --tgt-dataset ${decoder_working_file}-dataset.json --tgt-sentences ${decoder_working_file}-sentences.json --mapping $mapping --output-src-file-prefix ${encoder_working_file}  --output-tgt-file-prefix ${decoder_working_file} --minimum-frequency ${minfreq} --maximum-frequency ${maxfreq} --delete-frequency ${delfreq}


# Extract vectors
python -u ${scriptDir}/extract_data.py --input-file ${encoder_working_file}_min_${minfreq}_max_${maxfreq}_del_${delfreq}-dataset.json --output-vocab-file encoder-processed-vocab-filtered.npy --output-point-file encoder-processed-point-filtered.npy

python -u ${scriptDir}/extract_data.py --input-file ${decoder_working_file}_min_${minfreq}_max_${maxfreq}_del_${delfreq}-dataset.json --output-vocab-file decoder-processed-vocab-filtered.npy --output-point-file decoder-processed-point-filtered.npy

