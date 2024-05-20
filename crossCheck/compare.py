import pandas as pd
from ast import literal_eval
from pprint import pprint


def read_csvs(file1, file2, file3):
    """
    Read the CSV files and return the dataframes.
    """
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)

    df1["Tags"] = df1["Tags"].apply(literal_eval)
    df2["Tags"] = df2["Tags"].apply(literal_eval)
    df3["Tags"] = df3["Tags"].apply(literal_eval)

    return df1, df2, df3


def find_missmatchesBc5(gold, bc5, train):

    df1, df2, dfTrain = read_csvs(gold, bc5, train)
    # Find the indexes where the 'Tags' columns do not match
    mismatch_indexes = df1[df1["Tags"] != df2["Tags"]].index

    differing_tags_examples = []
    print(len(df1["Tags"]), len(df2["Tags"]), len(dfTrain["Tags"]))

    def find_differing_tags(tags1, tags2):
        """
        Compare two lists of tags and return only the elements that differ.
        """
        differing_tags = [(t1, t2) for t1, t2 in zip(tags1, tags2) if t1 != t2]
        return differing_tags

    def tag_in_dfTrain(tag, dfTrain):
        """
        Check if a tag appears in any of the 'Tags' lists in the dfTrain dataframe.
        """
        for tags in dfTrain["Tags"]:
            for t in tags:
                if str(tag[0]) == str(t[0]):
                    return True
        return False

    for index in mismatch_indexes:  # Limiting to the first 10 for brevity
        sentence = df1.loc[index, "Sentence"]
        tags1 = df1.loc[index, "Tags"]
        tags2 = df2.loc[index, "Tags"]

        differing_tags = find_differing_tags(tags1, tags2)
        if differing_tags:  # If there are differing tags
            exists = tag_in_dfTrain(differing_tags[0][0], dfTrain)
            if not exists:
                differing_tags_examples.append(
                    {
                        "Sentence": sentence,
                        "Differing Tags": differing_tags,
                        "Tag not in dfTrain": differing_tags[0][0],
                    }
                )

    # pprint(differing_tags_examples)
    print("Not existing in Train", len(differing_tags_examples))
    print(
        "Mismatched",
        len(mismatch_indexes),
        " without non-existing tags: ",
        len(mismatch_indexes) - len(differing_tags_examples),
    )

    return differing_tags_examples


# bc5toTrain = find_missmatchesBc5("csv/test_bc5_gold.csv", "csv/test_predictions_biobert_bc5.csv", "csv/train_bc5_gold.csv")
# pprint(bc5toTrain)


def find_missmatches_cross(gold, ncbi, train):

    df1, df2, dfTrain = read_csvs(gold, ncbi, train)

    # Create lists of tags for each dataset
    tags_list_df1 = df1["Tags"].tolist()
    tags_list_df2 = df2["Tags"].tolist()
    dfTrain_list = dfTrain["Tags"].tolist()

    print(
        "Test BC5=",
        len(tags_list_df1),
        "Test ncbi=",
        len(tags_list_df2),
        "Train=",
        len(dfTrain_list),
    )

    def find_difference(df1, df2):
        results = []
        index = 0
        for tags1 in df1:
            tempTags2 = list(tags1)
            for tags2 in df2:
                for tg1 in tags1:
                    for tg2 in tags2:
                        if tg1[0] == tg2[0]:
                            try:
                                tempTags2.remove(tg1)
                            except:
                                continue
            if tempTags2 == []:
                index += 1
                continue
            else:
                results.append(
                    {
                        "Index": index,
                        "Tag": tempTags2,
                    }
                )
                index += 1
                tempTags2 = []
        return results

    # test = find_difference(tags_list_df2, tags_list_df1)
    # print("Tags not in Test:", len(test))
    # print("Test:", test[:10])

    train = find_difference(tags_list_df2, dfTrain_list)
    print("Tags not in Train:", len(train))
    print("Train:", train[:10])

    # Compare ncbi test with ncbi train
    # dfTrainNcbi = pd.read_csv("csv/train_ncbi_gold.csv")
    # dfTrainNcbi['Tags'] = dfTrainNcbi['Tags'].apply(literal_eval)
    # dfTrainNcbi_list = dfTrainNcbi['Tags'].tolist()
    # print("Train ncbi length=", len(dfTrainNcbi))

    # trainNcbi = find_difference(tags_list_df2, dfTrainNcbi_list)
    # print("Tags not in Train Ncbi:", len(trainNcbi))
    # print("Train Ncbi:", trainNcbi[:10])

    return train


# test, train = find_missmatches_cross(
#     "csv/test_bc5_gold.csv",
#     "csv/test_predictions_biobert_bc5_toncbi.csv",
#     "csv/train_bc5_gold.csv",
# )
# # Save test and train in CSV
# dfTest = pd.DataFrame(test)
# dfTrain = pd.DataFrame(train)
# # dfTrainNcbi = pd.DataFrame(trainNcbi)
# dfTest.to_csv("csv/test_not_in_bc5.csv", index=False)
# dfTrain.to_csv("csv/train_not_in_bc5.csv", index=False)
# # dfTrainNcbi.to_csv('csv/train_not_in_ncbi.csv', index=False)

training = find_missmatches_cross(
    "csv/test_bc5_gold.csv", "csv/train_ncbi_gold.csv", "csv/train_bc5_gold.csv"
)

dfTrain = pd.DataFrame(training)
dfTrain.to_csv("csv/train_set_not_in_bc5.csv", index=False)
