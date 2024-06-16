import pandas as pd
import ast

gold_df = pd.read_csv('filtered_dev_ncbi_gold_onncbi.csv')
pred_df = pd.read_csv('csv/val_ncbi_pred_onncbi.csv')

diff_sentences = []
gold_sentences = []
diff_tags = []

for index, gold_row  in gold_df.iterrows():
    gold_tags = ast.literal_eval(gold_row['Tags'])
    pred_tags = ast.literal_eval(pred_df.iloc[index]['Tags'])
    
    # Check if there's any tag different between gold and pred
    has_difference = False

    for g_tag, p_tag in zip(gold_tags, pred_tags):
        if g_tag != p_tag:
            has_difference = True
            diff_tags.append({
                'Sentence': index +2 ,
                'Gold': g_tag,
                'Pred': p_tag,
                # 'word' : g_tag[0]
            })
            break
    
    # if has_difference:
    #     diff_sentences.append({
    #         'Sentence': pred_df.iloc[index]['Sentence'],
    #         'Tags': pred_df.iloc[index]['Tags']
    #     })
    #     gold_sentences.append({
    #         'Sentence': gold_row['Sentence'],
    #         'Tags': gold_row['Tags']
    #     })


# diff_df = pd.DataFrame(diff_sentences)
# gold_df = pd.DataFrame(gold_sentences)
diff_tags_df = pd.DataFrame(diff_tags)

# diff_df.to_csv('diff_sentences.csv', index=False)
# gold_df.to_csv('diff_sentences_gold2.csv', index=False)
diff_tags_df.to_csv('diff_tags_ncbi_filtered_onncbi.csv', index=False)


# train_df = pd.read_csv('csv/train_bc5_gold.csv')
# train_entities = []

# for tags in train_df['Tags']:
#     for word, entity in ast.literal_eval(tags):
#             for word2 in diff_tags_df['word']:
#                 if word2 == word:
#                     train_entities.append({
#                         'word': word,
#                         'entity': entity
#                     })
#                     print(word, entity)
#                     break
