from tabulate import tabulate
import pandas as pd
import ast

# bc5_df = pd.read_csv('diff_tags_new_bc5.csv')
# ncbi_df = pd.read_csv('diff_tags_new_ncbi.csv')

# def process(df, name):
        
#     # Group by Sentence and aggregate the Gold and Pred columns
#     df = df.groupby('Sentence').agg({
#         'Gold': lambda x: list(x),
#         'Pred': lambda x: list(x)
#     }).reset_index()
#     df['Data'] = name
#     df['Error Class'] = None
#     df = df[['Data', 'Sentence', 'Gold', 'Pred']]

#     # Define functions to check FP and FN
#     def check_fp_fn(gold_list, pred_list):
#         fp = 0
#         fn = 0
#         overlap = []
#         for gold, pred in zip(gold_list, pred_list):
#             gold_tag = ast.literal_eval(gold)[1]  # Extract the tag from the tuple
#             pred_tag = ast.literal_eval(pred)[1]
#             if gold_tag == 'O' and pred_tag != 'O':
#                 fp += 1
#             elif gold_tag != 'O' and pred_tag == 'O':
#                 fn += 1
#             elif gold_tag != 'O' and pred_tag != 'O':
#                 overlap.append(ast.literal_eval(gold)[0])
#         return fp, fn, overlap

#     # Apply functions to create new columns
#     df['FP'], df['FN'], df['Overlap'] = zip(*df.apply(lambda row: check_fp_fn(row['Gold'], row['Pred']), axis=1))
    
#     # Find consecutive tags
#     consecutive_tags = []
#     for index, row in df.iterrows():
#         df_gold_tags = [ast.literal_eval(tag) for tag in row['Gold']]
#         tokens = row['Sentence'].split()
#         temp_index = -1
#         temp_tags = ""
#         temp_list = []
#         for tag in df_gold_tags:
#             tag_index = tokens.index(tag[0])
#             if temp_index == -1:
#                 temp_tags += tag[0] + " "
#                 temp_index = tag_index
#             elif tag_index == temp_index + 1:
#                 temp_tags += tag[0] + " "
#                 temp_index = tag_index
#             else:
#                 if temp_tags:
#                     temp_list.append(temp_tags.strip())
#                 temp_tags = tag[0] + " "
#                 temp_index = tag_index
#             # if row['Sentence'].startswith("To begin to address the hypothesis that abnormal"):
#             #     print(temp_index,temp_tags)
#         if temp_tags:
#             temp_list.append(temp_tags.strip())

#         consecutive_tags.append(temp_list)

#     df['Tags'] = consecutive_tags
            
    
#     df_new_gold_tags = []
#     df_new_pred_tags = []
#     for index, row  in df.iterrows():
#         # Convert the string representations to list using ast.literal_eval
#         df_gold_tags = [ast.literal_eval(tag) for tag in row['Gold']]
#         df_pred_tags = [ast.literal_eval(tag) for tag in row['Pred']]

#         temp_gold = []
#         temp_pred = []
#         # Iterate over bc5_gold_tags and bc5_pred_tags in parallel
#         for gold_tag, pred_tag in zip(df_gold_tags, df_pred_tags):
#             if gold_tag[1] == 'O':
#                 temp_gold.append("-")
#             else:
#                 if gold_tag[0] == '-':
#                     temp_gold.append(gold_tag[0]+"*")
#                 else:
#                     temp_gold.append(gold_tag[0])

#             if pred_tag[1] == 'O':
#                 temp_pred.append("-")
#             else:
#                 temp_pred.append(pred_tag[0])

#         df_new_gold_tags.append(temp_gold)
#         df_new_pred_tags.append(temp_pred)

#     df['Gold'] = df_new_gold_tags
#     df['Pred'] = df_new_pred_tags
#     return df

# bc5_df = process(bc5_df, "BC5")
# ncbi_df = process(ncbi_df, "NCBI")

# # Column headers
# headers = ["Data", "Sentence", "Gold", "Model",  'FP', 'FN', 'Overlap', 'Tags']

# pd.set_option('display.max_columns', None)

# df_combined = pd.concat([bc5_df, ncbi_df], ignore_index=True)

# # Generate LaTeX table using tabulate
# latex_table = tabulate(df_combined, headers=headers, tablefmt="latex_longtable", showindex=False, stralign='left')

# # Modify the LaTeX table to use longtable environment
# column_widths = "{|p{0.9cm}|p{2.9cm}|p{1.6cm}|p{1.6cm}|p{0.4cm}|p{0.4cm}|p{2cm}|p{2cm}|}"
# latex_table = latex_table.replace('\\begin{longtable}', '\\begin{longtable}' + column_widths)
# latex_table = latex_table.replace('{llllrrll}', '')
# latex_table = latex_table.replace('\\\\', '\\\\ \hline')


headers = ["Data", "Sentence", "Gold", "Model",  'FP', 'FN', 'Overlap', 'Tags', 'POS_Stanza']
df = pd.read_csv('pos_tagged_data.csv')
df = df[['Data', 'Sentence', 'Gold', 'Pred',  'FP', 'FN', 'Overlap', 'Tags', 'Tags_POS_Stanza']]
latex_table = tabulate(df, headers=headers, tablefmt="latex_longtable", showindex=False, stralign='left')
column_widths = "{|p{0.9cm}|p{2.9cm}|p{1.6cm}|p{1.6cm}|p{0.4cm}|p{0.4cm}|p{2cm}|p{2cm}|p{2cm}|}"
latex_table = latex_table.replace('\\begin{longtable}', '\\begin{longtable}' + column_widths)
latex_table = latex_table.replace('{llllrrlll}', '')
latex_table = latex_table.replace('\\\\', '\\\\ \hline')
with open('latex_table.txt', 'w') as f:
    f.write(latex_table)

# df_combined.to_csv('diff_tags_combined.csv', index=False)
