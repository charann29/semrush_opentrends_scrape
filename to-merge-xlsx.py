import pandas as pd
import os

# Path to the folder containing your Excel files
folder_path = r'C:\Users\pc\Desktop\Charan\selenium'

# Get a list of all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Initialize an empty DataFrame to store the merged data
merged_df = pd.DataFrame()

for file_name in excel_files:
    # Read each Excel file into a pandas DataFrame
    df = pd.read_excel(os.path.join(folder_path, file_name))
    
    # Concatenate the current DataFrame with the merged DataFrame
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# Drop duplicate rows to keep only unique ones
merged_df = merged_df.drop_duplicates()

# Write the merged DataFrame to a new Excel file
merged_df.to_excel('merged_file.xlsx', index=False)
