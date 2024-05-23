
import argparse 
from collections import defaultdict
from pathlib import Path
from typing import List


def cluster_read(fname):
    """
    Given a txt file containing the latent concepts of a corresponding layer, The
    function loads all data in the file and returns it in form of lists. These lists 
    will be then used to create mappings between clusters, words, and sentences 

    Parameters
    ----------
    fname : str
        Path to where the latent concepts data is stored for a corresponding
        layer (Usually saved in a .txt file).

    Returns
    -------

    words: List
        A list of words corresponding to latent concepts of the passed data.
        Each word will be associated with a latent concept (also called a cluster)
    words_idx: List
        A list of word indices corresponding to occurance location of each word
        in the sentences.
    cluster_idx: List
        A list of cluster ids corresponding to the data passed. Each layer will
        have a group of clusters and each cluster contains a group of words
    sent_idx: List
        A list of sentence ids corresponding to which sentences the concept appears in
    """
    words = []
    words_idx = []
    cluster_idx = []
    sent_idx = []
    with open(fname) as f:
        for line in f:
            line = line.rstrip('\r\n')
            parts = line.split("|||")
            words.append(parts[0])
            cluster_idx.append(int(parts[4]))
            words_idx.append(int(parts[3]))
            sent_idx.append(int(parts[2]))
    return words, words_idx, sent_idx, cluster_idx


def get_words_to_sentence_ids_mapping(fname):
    """ 
    Given a path to a clusters file, the function returns a dictionary 
    where each key is a cluster id and each value is a list of tuples. 
    Each tuple in the list contains the word and the sentence id where the word occured 

    sample: {"c212": [("Hello", 0), ("Hola", 20) etc.]}

    Parameters
    ----------
    fname : str
        Path to where the latent concepts data is stored for a corresponding
        layer (Usually saved in a .txt file).

    Returns
    -------

    data: Dict 
        A dictionary containing the cluster data as described above.

    """

    data = defaultdict(list)
    words, words_idx, sent_idx, cluster_idx = cluster_read(fname)
    for i, elem in enumerate(cluster_idx):
        cluster = "c" + str(cluster_idx[i])
        # we need the sentence id to separate languages later on
        data[cluster].append((words[i], sent_idx[i]))
    return data


def count_sentences_according_to_threshold(lst, sent_threshold):
    lower_than_threshold = 0
    higher_than_threshold = 0
    for elem in lst:
        if elem[1] > sent_threshold:
            higher_than_threshold += 1
        else:
            lower_than_threshold += 1
    return lower_than_threshold, higher_than_threshold


def get_overlapping_clusters(path_to_clusters, sentences_threshold, clusters_threshold):

    cluster_to_words = get_words_to_sentence_ids_mapping(path_to_clusters)
    overlapping_clusters = []
  
    for cluster in cluster_to_words:
        words_sentIDS = cluster_to_words[cluster]
        lower_than_threshold, higher_than_threshold = count_sentences_according_to_threshold(
            words_sentIDS, sentences_threshold)
        lower_than_threshold_perct = (
            lower_than_threshold / len(words_sentIDS)) * 100
        higher_than_threshold_perct = (
            higher_than_threshold / len(words_sentIDS)) * 100
        if (lower_than_threshold_perct > clusters_threshold) and (higher_than_threshold_perct > clusters_threshold):
            overlapping_clusters.append(cluster)


    return overlapping_clusters







def main(): 
    parser = argparse.ArgumentParser()

    parser.add_argument("--cluster_file", help="Path to the cluster path for which we want to analyze the metrics")
    parser.add_argument("--output_path", help="Output path to store the overlapping clusters")
    parser.add_argument("--clusters_threshold", help="Threshold that we are considering for the overlap metric")
    parser.add_argument("--sentences_threshold", help="Threshold at which sentences are split into languages")
    args = parser.parse_args()

    threshold = args.sentences_threshold

    overlapping_clusters = get_overlapping_clusters(args.cluster_file, threshold, float(args.clusters_threshold))

    
    
    print(overlapping_clusters)
    # Save the overlapping clusters to a json file
    with open(args.output_path, 'w') as f:
        for cluster in overlapping_clusters:
            f.write(cluster + "\n")
    



if __name__=="__main__": 
    main()