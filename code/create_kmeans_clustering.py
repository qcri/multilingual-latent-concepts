import numpy as np
import time
from memory_profiler import profile
import argparse 
from sklearn.cluster import KMeans

print("USAGE: create_kmeans_clustering.py -p <POINT_FILE> -v <VOCAB_FILE> -k <CLUSTERS> -o <OUTPUT_FOLDER>")


@profile
def kmeans_cluster(P, V, K, output_path, ref=''):
    """
    Uses the point.npy P, vocab.npy V files of a layer (generated using https://github.com/hsajjad/ConceptX/ library) to produce a clustering of <K> clusters at <output_path> named clusters-kmeans-{K}.txt
    """
    kmeans = KMeans(n_clusters=K, verbose=3, random_state=212)
    output = kmeans.fit(P)
    
    out_file =  f"{output_path}/clusters-kmeans-{K}{ref}.txt"

    clusters = {i:[] for i in range(K)}
    for v, l in zip(V, output.labels_):
       clusters[l].append(f'{v}|||{l}')

    out = ""
    for k,v in clusters.items():
        out += '\n'.join(v) + '\n'

    with open(out_file, 'w') as f2:
        f2.write(out)

    return out



parser = argparse.ArgumentParser()
parser.add_argument("--vocab-file","-v", help="output vocab file with complete path")
parser.add_argument("--point-file","-p", help="output point file with complete path")
parser.add_argument("--output-path","-o", help="output path clustering model and result files")
parser.add_argument("--cluster","-k", help="cluster number")
parser.add_argument("--count","-c", help="point count ratio", default=-1)


args2 = parser.parse_args()
vocab_file = args2.vocab_file
point_file = args2.point_file
output_path = args2.output_path
K = int(args2.cluster)
point_count_ratio = float(args2.count)

P = np.load(point_file)
V= np.load(vocab_file)

useable_count = int(point_count_ratio*len(V)) if point_count_ratio != -1 else -1

P= P[:useable_count, :]
V= V[:useable_count]

start_time = time.time()
ref = '-' + str(point_count_ratio) if point_count_ratio > 0 else ''
kmeans_cluster(P, V, K, output_path, ref)
end_time = time.time()

print(f"Runtime: {end_time - start_time}")
