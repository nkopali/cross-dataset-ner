import pandas as pd
import ast

# Load the CSV files
train_df = pd.read_csv('csv/train_bc5_gold.csv')
test_df = pd.read_csv('csv/test_ncbi_gold.csv')
print(train_df.shape)
print(test_df.shape)

# Extract entities from train_df, excluding 'O' entities
def extract_entities(df):
    train_entities = set()
    for tags in df['Tags']:
        for word, entity in ast.literal_eval(tags):
            if entity != 'O':
                train_entities.add((word, entity))
    return train_entities

train_entities = extract_entities(train_df)
print("Train entities len: ", len(train_entities))
test_entities = extract_entities(test_df)
print("Test entities len: ", len(test_entities))
intersection_entities = train_entities.intersection(test_entities)
print("Intersection len: ", len(intersection_entities))

# Function to check if a sentence contains any of the train entities
def contains_train_entity(tags):
    for word, entity in ast.literal_eval(tags):
        if (word, entity) in train_entities:
            return True
    return False

# Filter test_df to include only rows where the entity is found in train_entities
filtered_test_df = test_df[test_df['Tags'].apply(contains_train_entity)]

# Save the filtered sentences to a new CSV file
filtered_test_df.to_csv('filtered_test_ncbi_gold.csv', index=False)

print(filtered_test_df.shape)
