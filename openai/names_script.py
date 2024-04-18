import os

folder_path = r'C:\Users\pc\Desktop\Charan\selenium'

# List all files in the folder
files = os.listdir(folder_path)

# Filter only .xlsx files
xlsx_files = [file[:-5] for file in files if file.endswith('.xlsx')]

# Print the names of xlsx files without the extension
for xlsx_file in xlsx_files:
    print(xlsx_file)
