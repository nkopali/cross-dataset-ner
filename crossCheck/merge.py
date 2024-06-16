#merge two csv files
import pandas as pd
import os
import sys

def merge_csv(file1, file2, output):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df = pd.concat([df1, df2], ignore_index=True)
    df.to_csv(output, index=False)

merge_csv("csv/train_bc5_gold.csv", "csv/train_ncbi_gold.csv", "train_merged.csv")