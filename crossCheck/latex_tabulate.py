from tabulate import tabulate
import pandas as pd
import ast

bc5_df = pd.read_csv('diff_tags_new_bc5.csv')
ncbi_df = pd.read_csv('diff_tags_new_ncbi.csv')

def process(df, name):
        
    # Group by Sentence and aggregate the Gold and Pred columns
    df = df.groupby('Sentence').agg({
        'Gold': lambda x: list(x),
        'Pred': lambda x: list(x)
    }).reset_index()
    df['Dataset'] = name
    df['Error Class'] = None
    df = df[['Dataset', 'Sentence', 'Gold', 'Pred','Error Class']]

    df_new_gold_tags = []
    df_new_pred_tags = []
    for index, row  in df.iterrows():
        # Convert the string representations to list using ast.literal_eval
        df_gold_tags = [ast.literal_eval(tag) for tag in row['Gold']]
        df_pred_tags = [ast.literal_eval(tag) for tag in row['Pred']]

        temp_gold = []
        temp_pred = []
        # Iterate over bc5_gold_tags and bc5_pred_tags in parallel
        for gold_tag, pred_tag in zip(df_gold_tags, df_pred_tags):
            if gold_tag[1] == 'O':
                temp_gold.append("-")
            else:
                temp_gold.append(gold_tag[0])

            if pred_tag[1] == 'O':
                temp_pred.append("-")
            else:
                temp_pred.append(pred_tag[0])

        df_new_gold_tags.append(temp_gold)
        df_new_pred_tags.append(temp_pred)

    df['Gold'] = df_new_gold_tags
    df['Pred'] = df_new_pred_tags
    return df

bc5_df = process(bc5_df, "BC5")
ncbi_df = process(ncbi_df, "NCBI")

# Column headers
headers = ["Dataset", "Sentence", "Gold Prediction", "Model Prediction", 'Error Class']

pd.set_option('display.max_columns', None)

df_combined = pd.concat([bc5_df, ncbi_df], ignore_index=True)
# print(df_combined.head())
# print(df_combined.tail())

# Generate LaTeX table using tabulate
latex_table = tabulate(df_combined, headers=headers, tablefmt="latex_longtable", showindex=False, stralign='left')

# Modify the LaTeX table to use longtable environment
column_widths = "{|p{1.2cm}|p{5cm}|p{2.5cm}|p{2.5cm}|p{1cm}|}"
latex_table = latex_table.replace('\\begin{longtable}', '\\begin{longtable}' + column_widths)
latex_table = latex_table.replace('\\\\', '\\\\ \hline')
# print(latex_table)

with open('latex_table.txt', 'w') as f:
    f.write(latex_table)

df_combined.to_csv('diff_tags_combined.csv', index=False)
