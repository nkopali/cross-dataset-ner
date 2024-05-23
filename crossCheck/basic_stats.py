import pandas as pd
from ast import literal_eval

def read_csvs(file):
    """
    Read the CSV files and return the dataframes.
    """
    df = pd.read_csv(file)

    df["Tags"] = df["Tags"].apply(literal_eval)

    return df

def basic_analysis(df, dataset_name):
    print(f'Basic analysis for {dataset_name} dataset:')
    # Calculate average words in sentence
    avg_words_per_sentence = df['Sentence'].apply(lambda x: len(x.split())).mean()
    print(f'Average words per sentence: {avg_words_per_sentence:.2f}')

    # Calculate average length of words
    avg_word_length = df['Sentence'].apply(lambda x: sum(len(word) for word in x.split()) / len(x.split())).mean()
    print(f'Average length of words: {avg_word_length:.2f}')

    # Calculate average number of characters in an entity
    def count_entity_chars(tags):
        entity_chars = 0
        for tag in tags:
            if tag[1]!= 'O':  # Only count entities (B, I)
                entity_chars += len(tag[0])
        return entity_chars
    
    # Calculate average number of entities in a sentence
    def count_entities(tags):
        entities = 0
        for tag in tags:
            if tag[1]!= 'O':  # Only count entities (B, I)
                entities += 1
        return entities

    avg_entity_chars = df['Tags'].apply(count_entity_chars).mean()
    print(f'Average number of characters in an entity: {avg_entity_chars:.2f}')

    avg_entity_sentence = df['Tags'].apply(count_entities).mean()
    print(f'Average number of entities in a sentence: {avg_entity_sentence:.2f}')

# Read the CSV file
df1 = read_csvs('csv/train_bc5_gold.csv')
df2 = read_csvs('csv/train_ncbi_gold.csv')

basic_analysis(df1, 'BC5 dataset')
print("**********")
basic_analysis(df2, 'NCBI dataset')





