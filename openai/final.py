import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('merged_file.csv')

# Drop duplicate rows based on the 'Domain Name' column
df = df.drop_duplicates(subset=['Domain Name'])

# Filter rows where 'Total Traffic' is greater than or equal to 10000
df = df[df['Total Traffic'] >= 15000]

# Write the filtered DataFrame to a new CSV file
df.to_csv('filtered_file.csv', index=False)
