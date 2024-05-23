"""
Utility function to remove sentences of length longer than the specified length
Input
Author: Basel Mousi
Creation: 10 Oct 2023

Parameters
----------
encoder-input : str, 
    encoder input file 
decoder-input: str, 
    decoder input file 
length : int, optional
    Maximum sentence length

Yields
------
encoder_filtered_inputs : enocder filtered sentences file
decoder_filtered_inputs: decoder filtered sentences file
"""


import argparse 
parser = argparse.ArgumentParser()
parser.add_argument('--encoder_input', type=str, required=True)
parser.add_argument('--decoder_input', type=str, required=True)
parser.add_argument('--encoder_output_file', type=str, required=True)
parser.add_argument('--decoder_output_file', type=str, required=True)
parser.add_argument("--length", type=int, default=300)

args = parser.parse_args() 

encoder_writer = open(args.encoder_output_file, "w")
decoder_writer = open(args.decoder_output_file, "w")
count = 0
with open(args.encoder_input, "r") as encoder_reader,  open(args.decoder_input, "r") as decoder_reader: 
    for line1, line2 in zip(encoder_reader, decoder_reader): 
        if ((len(line1.strip().split()) < args.length) and (len(line2.strip().split()) < args.length)): 
            encoder_writer.write(line1) 
            decoder_writer.write(line2)
        else: 
            print ("Skipped lines: ", line1, "|||", line2)
            count +=1

encoder_writer.close()
decoder_writer.close()

print(f"[INFO] encoder filtered file is saved as: {args.encoder_output_file}")
print(f"[INFO] decoder filtered file is saved as: {args.decoder_output_file}")
print(f"[INFO] Number of skipped lines: {count}")
 




