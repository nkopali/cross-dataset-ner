import pandas as pd
import ast
from collections import Counter

# Load the CSV files
gold_df = pd.read_csv('filtered_dev_ncbi_gold_onncbi.csv')
pred_df1 = pd.read_csv('csv/val_ncbi_pred_onncbi.csv')

# Initialize a dictionary to store mismatches
sentence_df = {}

for index, gold_row in gold_df.iterrows():
    gold_tags = ast.literal_eval(gold_row['Tags'])
    pred_tags = ast.literal_eval(pred_df1.iloc[index]['Tags'])
    
    # Check for differences between gold and pred tags
    diff_tags = []
    for g_tag, p_tag in zip(gold_tags, pred_tags):
        if g_tag != p_tag:
            diff_tags.append({
                'Gold': g_tag,
                'Pred': p_tag
            })
    
    # If there's a difference, add to sentence_df
    if diff_tags:
        sentence_df[gold_row['Sentence']] = diff_tags

# Optionally, convert the dictionary to a DataFrame for better visualization
diff_sentences_df = pd.DataFrame([
    {'Sentence': sentence, 'Gold': diff['Gold'], 'Pred': diff['Pred']}
    for sentence, diffs in sentence_df.items()
    for diff in diffs
])

print(diff_sentences_df)

# Extract words from the Pred column and count occurrences
pred_words = [pred[0] for pred in diff_sentences_df['Pred']]
word_counts = Counter(pred_words)

print(word_counts)