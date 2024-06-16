import pandas as pd
import ast

diff_tags = pd.read_csv('diff_tags_bc5_filtered_onbc5.csv')

sorted_diff_tags = sorted(diff_tags, key=lambda x: x['Gold'])

#save the sorted tags to a new csv file
sorted_diff_tags_df = pd.DataFrame(sorted_diff_tags)
sorted_diff_tags_df.to_csv('sorted_diff_tags_bc5_filtered_onbc5.csv', index=False)