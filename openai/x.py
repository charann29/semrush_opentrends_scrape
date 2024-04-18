import pandas as pd

# Read CSV1
csv1 = pd.read_csv('cleaned_file.csv')

# Read CSV2
csv2 = pd.read_csv('merged.csv')

# Merge CSV2 with CSV1 based on 'Domain Name'
merged_df = pd.merge(csv2, csv1[['Domain Name', 'Country Code', 'Category']], on='Domain Name', how='left')

# Write the merged DataFrame back to CSV
merged_df.to_csv('merged_final.csv', index=False)
