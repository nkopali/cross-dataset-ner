import pandas as pd
import ast


def decompose(filepath):
    df = pd.read_csv(filepath)

    # print("BC5CDR length: ", len(df1))
    # print("NCBI length: ", len(df2))
    # print("=====================================")

    df["Tags"] = df["Tags"].apply(ast.literal_eval)

    # Define the path for the output file
    output_file_path = "test.tsv"

    # Initialize an empty string to aggregate the content
    all_tags_content = ""

    # Iterate over each row of the DataFrame
    for index, row in df.iterrows():
        tags_list = row["Tags"]
        for word, label in tags_list:
            all_tags_content += f"{word}\t{label}\n"
        all_tags_content += "\n"  # Add a newline at the end of each row's content

    # Write the aggregated content to the file
    with open(output_file_path, "w") as file:
        file.write(all_tags_content)

    # Provide the path to the created file
    output_file_path


decompose("filtered_test_bc5_gold.csv")
