import pandas as pd

# Read both CSV files into pandas DataFrames
df1 = pd.read_csv('country_category_data2.csv')
df2 = pd.read_csv('country_category_data.csv')

# Remove duplicates from each DataFrame
df1 = df1.drop_duplicates()
df2 = df2.drop_duplicates()

# Concatenate the DataFrames vertically (stacking one below the other)
merged_df = pd.concat([df1, df2], ignore_index=True)

# Remove duplicates from the merged DataFrame
merged_df = merged_df.drop_duplicates()

# Write the merged DataFrame to a new CSV file
merged_df.to_csv('merged_file.csv', index=False)
