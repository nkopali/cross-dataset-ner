import pandas as pd
import ast

gold_df = pd.read_csv('filtered_dev_ncbi_gold_onbc5.csv')
pred_df1 = pd.read_csv('csv/val_ncbi_pred_onbc5.csv')
# pred_df1 = pd.read_csv('csv/val_ncbi_pred_onncbi.csv')

diff_sentences = []
gold_sentences = []
diff_tags = []

for index, gold_row  in gold_df.iterrows():
    gold_tags = ast.literal_eval(gold_row['Tags'])
    pred_tags = ast.literal_eval(pred_df1.iloc[index]['Tags'])
    
    # Check if there's any tag different between gold and pred
    has_difference = False

    for g_tag, p_tag in zip(gold_tags, pred_tags):
        if g_tag != p_tag:
            has_difference = True
            diff_tags.append({
                'Sentence': gold_row['Sentence'] ,
                'Gold': g_tag,
                'Pred': p_tag,
                # 'word' : g_tag[0]
            })
            # break

    
    # if has_difference:
    #     diff_sentences.append({
    #         'Sentence': pred_df.iloc[index]['Sentence'],
    #         'Tags': pred_df.iloc[index]['Tags']
    #     })
    #     gold_sentences.append({
    #         'Sentence': gold_row['Sentence'],
    #         'Tags': gold_row['Tags']
    #     })



diff_tags_df = pd.DataFrame(diff_tags)

diff_tags_df.to_csv('diff_tags_new_bc5.csv', index=False)


