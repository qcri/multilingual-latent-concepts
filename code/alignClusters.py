import sys

# Check if the correct number of command line arguments is provided
if len(sys.argv) != 8:
    print(sys.argv)
    print("Usage: python script.py cluster_file1.txt cluster_file2.txt dictionary_file.txt top_n_target_phrases")
    sys.exit(1)

# Get the cluster file paths, dictionary file path, and top N target phrases from the command line arguments
cluster_file_path1 = sys.argv[1]
cluster_file_path2 = sys.argv[2]
dictionary_file_path = sys.argv[3]
top_n_target_phrases = int(sys.argv[4])
match_percentage = float(sys.argv[5])
size_threshold = float(sys.argv[6])
no_types = float(sys.argv[7])

# Read and parse the dictionary file considering top N target phrases for each source phrase
dictionary = {}
with open(dictionary_file_path, 'r') as dict_file:
    for line in dict_file:
        parts = line.strip().split('->')
        source_phrase = parts[0].strip()
        target_parts = parts[1].strip().split(': Probability = ')
        prob_and_count = target_parts[1].strip().split(', Count = ')
        target_phrase = target_parts[0].strip()
        probability = float(prob_and_count[0])
        count = int(prob_and_count[1])
        #print (source_phrase, target_phrase, probability, count)
        #input()
        # Consider only the top N target phrases for each source phrase
        if source_phrase in dictionary and len(dictionary[source_phrase]) < top_n_target_phrases:
            dictionary[source_phrase].append((target_phrase, probability))
        elif source_phrase not in dictionary:
            dictionary[source_phrase] = [(target_phrase, probability)]


# Initialize dictionaries to store clusters for both sets
clusters1 = {}
clusters2 = {}

# Function to update clusters based on the cluster file
def update_clusters(file_path, clusters):
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line based on "|||"
            parts = line.strip().split('|||')
            
            # Extract word and cluster number
            word = parts[0].strip()
            cluster_number = int(parts[-1].strip())
            
            # Check if the cluster number is already in the dictionary
            if cluster_number in clusters:
                # If yes, add the word to the existing cluster
                clusters[cluster_number].add(word)
            else:
                # If not, create a new cluster with the word
                clusters[cluster_number] = {word}

# Update clusters for both sets
update_clusters(cluster_file_path1, clusters1)
update_clusters(cluster_file_path2, clusters2)


# Check for alignment between source and target clusters
aligned_clusters = {}
for source_cluster_number, source_words in clusters1.items():
    aligned_clusters[source_cluster_number] = set()
    match_list = []
    for target_cluster_number, target_words in clusters2.items():
        aligned_word_count = 0
        total_words_in_source_cluster = len(source_words)
        for source_word in source_words:
            if source_word in dictionary:
                for target_translation, translation_probability in dictionary[source_word]:
                    if target_translation in target_words: #and translation_probability > 0.5:
                        aligned_word_count += 1
                        match_tup = (source_word, target_translation)
                        match_list.append(match_tup)
                        break
        if aligned_word_count / total_words_in_source_cluster > match_percentage and len(clusters1[source_cluster_number]) > no_types and len(clusters1[source_cluster_number])/len(clusters2[target_cluster_number]) > size_threshold:
            aligned_clusters[source_cluster_number].add(target_cluster_number)
            print (match_list)
            print ("Source Cluster", source_cluster_number, "Target Cluster", target_cluster_number)
            print ("Source Cluster Size", len(clusters1[source_cluster_number]), "Target Cluster Size", len(clusters2[target_cluster_number]))
            print (aligned_word_count, total_words_in_source_cluster)
            #input()

# Print aligned clusters
print("Aligned Clusters:", len (aligned_clusters))
for source_cluster, target_clusters in aligned_clusters.items():
    if target_clusters:
        print(f"Source Cluster {source_cluster} is aligned to Target Clusters: {', '.join(map(str, target_clusters))}")

    
