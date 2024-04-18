import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('cleaned_file11.csv')

# Group the data by 'Domain Name' and aggregate the 'Country Code' column
# into a single cell separated by '/'
df_grouped = df.groupby('Domain Name')['Country Code'].apply('/'.join).reset_index()

# Merge the grouped data with the original DataFrame to retain other columns
# You can choose to keep or drop other columns as per your requirement
df_merged = pd.merge(df, df_grouped, on='Domain Name').drop_duplicates(subset=['Domain Name'])

# Save the merged DataFrame to a new CSV file
df_merged.to_csv('final_draft.csv', index=False)

print("Final draft CSV file created successfully!")
