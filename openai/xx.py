import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('merged_final.csv')

# Drop the 'Category' column
df.drop('Category', axis=1, inplace=True)

# Remove duplicates based on all remaining columns
df.drop_duplicates(inplace=True)

# Write the DataFrame back to a CSV file
df.to_csv('cleaned_file11.csv', index=False)
