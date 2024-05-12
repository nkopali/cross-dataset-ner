import pandas as pd

df1 = pd.read_csv("filtered_sentences_with_tags.csv")
df2 = pd.read_csv("biomedical_ner_dataset_100.csv")

merged = pd.concat([df1, df2], ignore_index=True)

merged.to_csv("train_merged_cosine.csv", index=False)
