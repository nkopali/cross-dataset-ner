import pandas as pd
from sentence_transformers import SentenceTransformer, util
import numpy as np
from ast import literal_eval
from collections import Counter

df1 = pd.read_csv('csv/train_merged_all.csv')

model = SentenceTransformer('gsarti/biobert-nli')

# Convert the string representation of tuples in the 'Tags' column back to actual tuples
df1['Tags'] = df1['Tags'].apply(literal_eval)

# Initialize a counter for all entities (excluding those tagged as 'O')
entity_counter = Counter()

# Iterate over the rows in the dataframe
for _, row in df1.iterrows():
    for entity, tag in row['Tags']:
        # Check if the tag is not 'O' (indicating it's an entity)
        if tag != 'O':
            entity_counter[entity] += 1

# Display the 10 most common entities
most_common_entities = entity_counter.most_common(20)
print(most_common_entities)

target_entities = ['syndrome', 'disease', 'deficiency', 'cancer', 'dystrophy', 'breast', 'ovarian', 'renal', 'DM', 'disorder', 'pain', 'ALD', 'DMD', 'toxicity', 'APC']

# Initialize a list to hold sentences that contain these entities
matching_sentences = []

# Iterate over the sentences in the dataframe
for _, row in df1.iterrows():
    sentence = row['Sentence']
    # Check if any of the target entities is in the sentence
    if any(entity in sentence for entity in target_entities):
        matching_sentences.append(sentence)

# selected_sentences = df1['Sentence'].head(5).tolist()

# Encode the selected sentences to get their embeddings
embeddings = model.encode(matching_sentences)

# Compute the average of the embeddings
reference_embedding = np.mean(embeddings, axis=0)

kept_rows = []

for index, row in df1.iterrows():
    sentence_embedding = model.encode(row['Sentence'])
    
    cosine_similarity = util.pytorch_cos_sim(sentence_embedding, reference_embedding)

    if cosine_similarity > 0.7:
        # If above the threshold, add it to the kept sentences
        kept_rows.append(row)

    # print(sentence_embedding)
            
# Convert the kept rows into a DataFrame
df_kept = pd.DataFrame(kept_rows)

# If you want to reset the index of the new DataFrame
df_kept.reset_index(drop=True, inplace=True)

# Optional: Save the filtered sentences and their tags to a new CSV file
df_kept.to_csv('filtered_sentences_with_tags.csv', index=False)