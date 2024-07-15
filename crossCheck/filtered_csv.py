import pandas as pd
import ast
from decompose import decompose

# Load the CSV files
train_df = pd.read_csv('csv/train_bc5_gold.csv')
dev_df = pd.read_csv('csv/dev_bc5.csv')

# dev = pd.read_csv('csv/test_bc5_gold.csv')
print("Train", train_df.shape)
print("Dev", dev_df.shape)
# print("Test", dev.shape)

# Extract entities from train_df, excluding 'O' entities
def extract_entities(df):
    train_entities = []
    train_tag_words = []
    for tags in df['Tags']:
        for word, entity in ast.literal_eval(tags):
            if entity != 'O':
                train_entities.append((word, entity))
                train_tag_words.append(word)
    return train_entities, train_tag_words

train_entities, train_tag_words = extract_entities(train_df)
# print("Train entities len: ", len(train_entities))
# dev_entities = extract_entities(dev_df)
# print("Dev entities len: ", len(dev_entities))
# intersection_entities = train_entities.intersection(dev_entities)
# print("Intersection len: ", len(intersection_entities))

# Function to check if a sentence contains any of the train entities
def contains_train_entity(tags):
    for word, entity in ast.literal_eval(tags):
        if entity != 'O':
            if (word, entity) not in train_entities and word not in train_tag_words:
                return False
        # if (word, entity) in train_entities:
        #     return True
    return True

# Filter dev_df to include only rows where the entity is found in train_entities
filtered_dev_df = dev_df[dev_df['Tags'].apply(contains_train_entity)]

# Save the filtered sentences to a new CSV file
filtered_dev_df.to_csv('filtered_dev_bc5_gold_onbc5.csv', index=False)

print(filtered_dev_df.shape)
decompose("filtered_dev_bc5_gold_onbc5.csv")
