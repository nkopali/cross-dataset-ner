import pandas as pd
import ast


def combine(filepath1, filepath2):
    df1 = pd.read_csv(filepath1)
    df2 = pd.read_csv(filepath2)

    # print("BC5CDR length: ", len(df1))
    # print("NCBI length: ", len(df2))
    # print("=====================================")

    df1['Tags'] = df1['Tags'].apply(ast.literal_eval)
    df2['Tags'] = df2['Tags'].apply(ast.literal_eval)


    df1['Tags'] = df1['Tags'].apply(lambda x: [tag for tag in x if tag[1] != 'O'])
    df2['Tags'] = df2['Tags'].apply(lambda x: [tag for tag in x if tag[1] != 'O'])

    # Ensure no empty tags
    df1 = df1[df1['Tags'].map(len) > 0].reset_index(drop=True)
    df2 = df2[df2['Tags'].map(len) > 0].reset_index(drop=True)
    # Explode the 'Tags' column while keeping the sentence information
    exploded_df1 = df1.explode('Tags').drop_duplicates(['Sentence', 'Tags'])
    exploded_df2 = df2.explode('Tags').drop_duplicates(['Sentence', 'Tags'])

    # Use merge to find unique tags in df2 compared to df1
    unique_to_df2 = exploded_df2.merge(exploded_df1, on=['Sentence', 'Tags'], how='left', indicator=True).loc[lambda x: x['_merge'] == 'left_only']

    # Drop the '_merge' column as it's no longer needed
    unique_to_df2 = unique_to_df2.drop('_merge', axis=1)

    # Group by sentence and aggregate the tags back into lists
    unique_to_df2_grouped = unique_to_df2.groupby('Sentence', as_index=False).agg({'Tags': lambda x: list(x)})

    print("Length=",len(unique_to_df2_grouped), unique_to_df2_grouped.head(10)) # Display the first 10 for review

    print("=====================================")

    df_gold = pd.read_csv(filepath2)
    print("Length of Gold=",len(df_gold))
    # Find the sentences from unique_to_df2_grouped in the original gold dataset
    unique_to_df2_gold = df_gold[df_gold['Sentence'].isin(unique_to_df2_grouped['Sentence'])]
    print("Length=",len(unique_to_df2_gold), unique_to_df2_gold.head(10)) # Display the first 10 for review

    print("********************************************")
    df_bc5 = pd.read_csv(filepath1)
    print("Length of BC5=",len(df_bc5))
    # add the unique_to_df2_gold to df_bc5
    df_bc5 = pd.concat([df_bc5, unique_to_df2_gold], ignore_index=True)
    print("Length=",len(df_bc5), df_bc5.head(10)) # Display the first 10 for review

    # Save the new merged dataset
    df_bc5.to_csv('csv/train_bc5_merged.csv', index=False)



print("TRAIN SET")
combine('csv/train_bc5_gold.csv', 'csv/train_ncbi_gold.csv')


# print("TEST SET")
# combine('csv/test_bc5_gold.csv', 'csv/test_ncbi_gold.csv')
