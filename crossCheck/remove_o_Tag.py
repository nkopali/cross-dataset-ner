import pandas as pd
import ast

df = pd.read_csv("csv/train_set_not_in_bc5_first.csv")

df["Tag"] = df["Tag"].apply(ast.literal_eval)

df["Tag"] = df["Tag"].apply(lambda x: [t for t in x if t[1] != "O"])

df = df[df["Tag"].map(len) > 0]
print(df)
print(len(df))

df.to_csv("csv/train_set_not_in_bc5_first_no_o.csv", index=False)
