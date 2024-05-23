#!/bin/bash -l

conda activate neurox_pip

scriptDir=""   # path to ConceptX script directory
inputPath=""       # path to the directory where sentence files are saved
encoder_input=""       # Encoder Sentences
decoder_input=""      # Decoder Sentences
model=""     # Model that we want to do the extraction for
model_class=""
NEUROX_PATH=""

sentence_length=300   # maximum sentence length
minfreq=0 
maxfreq=15
delfreq=10000000 
layers_of_interest="0,1,3,6,9,12" # define layers of interest 


#specify according to where you want your activations to be saved. Keep a clear structure

encoder_working_file=$encoder_input.tok.sent_len
decoder_working_file=$decoder_input.tok.sent_len

cp ${inputPath}/$encoder_input $encoder_input.tok
cp ${inputPath}/$decoder_input $decoder_input.tok


# Do sentence length filtering and keep sentences max length of {sentence_length}
python "code/parallel_sentence_length.py" --encoder_input $encoder_input.tok --decoder_input $decoder_input.tok --encoder_output_file $encoder_working_file --decoder_output_file  $decoder_working_file --length ${sentence_length}


# Calculate vocabulary size
python ${scriptDir}/frequency_count.py --input-file ${encoder_working_file} --output-file ${encoder_working_file}.words_freq
python ${scriptDir}/frequency_count.py --input-file ${decoder_working_file} --output-file ${decoder_working_file}.words_freq


# Extract layer-wise activations
PYTHONPATH=$NEUROX_PATH python -u -m neurox.data.extraction.transformers_extractor "${model},${model},${model_class}" ${encoder_working_file}  ${decoder_working_file} activations.json --output_type json --seq2seq_component both --decompose_layers --filter_layers "$layers_of_interest"

# Create a dataset file with word and sentence indexes
layers_of_interest="0 1 3 6 9 12"
for j in $layers_of_interest 
do
    python ${scriptDir}/create_data_single_layer.py --text-file ${encoder_working_file} --activation-file encoder-activations-layer${j}.json --output-prefix "${encoder_working_file}_${j}" 
    python ${scriptDir}/create_data_single_layer.py --text-file ${decoder_working_file} --activation-file decoder-activations-layer${j}.json --output-prefix "${decoder_working_file}_${j}"
    python ${scriptDir}/frequency_filter_data.py --input-file ${encoder_working_file}_${j}-dataset.json --frequency-file ${encoder_working_file}.words_freq --sentence-file "${encoder_working_file}_${j}-sentences.json" --minimum-frequency $minfreq --maximum-frequency $maxfreq --delete-frequency ${delfreq} --output-file "${encoder_working_file}_${j}"

    python ${scriptDir}/frequency_filter_data.py --input-file "${decoder_working_file}_${j}-dataset.json" --frequency-file "${decoder_working_file}.words_freq" --sentence-file "${decoder_working_file}_${j}-sentences.json" --minimum-frequency $minfreq --maximum-frequency $maxfreq --delete-frequency ${delfreq} --output-file "${decoder_working_file}_${j}"
    python -u ${scriptDir}/extract_data.py --input-file ${encoder_working_file}_${j}_min_${minfreq}_max_${maxfreq}_del_${delfreq}-dataset.json --output-vocab-file encoder-processed-vocab-${j}.npy --output-point-file encoder-processed-point-${j}.npy
    python -u ${scriptDir}/extract_data.py --input-file ${decoder_working_file}_${j}_min_${minfreq}_max_${maxfreq}_del_${delfreq}-dataset.json --output-vocab-file decoder-processed-vocab-${j}.npy --output-point-file decoder-processed-point-${j}.npy

done

rm -r *-dataset.json
rm -r *-labels.json
rm -r *activations*.json