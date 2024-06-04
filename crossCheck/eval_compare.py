import pandas as pd
import ast

gold_df = pd.read_csv('filtered_dev_bc5_gold.csv')
pred_df = pd.read_csv('csv/val_bc5_filtered_pred.csv')

diff_sentences = []
gold_sentences = []

for index, gold_row  in gold_df.iterrows():
    gold_tags = ast.literal_eval(gold_row['Tags'])
    pred_tags = ast.literal_eval(pred_df.iloc[index]['Tags'])
    # for index, tag in enumerate(tags_gold):
    #     print(tag)
    #     print(tags_pred[index])
    
    # Check if there's any tag different between gold and pred
    has_difference = False
    for g_tag, p_tag in zip(gold_tags, pred_tags):
        if g_tag != p_tag:
            has_difference = True
            break
    
    if has_difference:
        diff_sentences.append({
            'Sentence': pred_df.iloc[index]['Sentence'],
            'Tags': pred_df.iloc[index]['Tags']
        })
        gold_sentences.append({
            'Sentence': gold_row['Sentence'],
            'Tags': gold_row['Tags']
        })


diff_df = pd.DataFrame(diff_sentences)
gold_df = pd.DataFrame(gold_sentences)

diff_df.to_csv('filtered_diff_sentences.csv', index=False)
gold_df.to_csv('filtered_diff_sentences_gold.csv', index=False)
