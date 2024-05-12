import pandas as pd

df1 = pd.read_csv("csv/train_bc5_gold.csv")
df2 = pd.read_csv("csv/train_ncbi_gold.csv")
df3 = pd.read_csv("csv/train_set_not_in_bc5_first_no_o.csv")

rows_to_concatenate = df2.loc[df3["Index"]]

# merged = pd.concat([df1, df2], ignore_index=True)
merged = pd.concat([df1, rows_to_concatenate], ignore_index=True)

merged.to_csv("csv/train_merged_missing.csv", index=False)
