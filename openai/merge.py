import pandas as pd

def merge_csv(csv1_path, csv2_path, output_path):
    # Read CSV files into pandas dataframes
    df1 = pd.read_csv(csv1_path, encoding='latin1')  # Adjust encoding if needed
    df2 = pd.read_csv(csv2_path, encoding='latin1')  # Adjust encoding if needed
    
    # Concatenate the dataframes
    merged_df = pd.concat([df1, df2])
    
    # Drop duplicates
    merged_df.drop_duplicates(inplace=True)
    
    # Write merged dataframe to a new CSV file
    merged_df.to_csv(output_path, index=False)

# Example usage
merge_csv('domain_results.csv', 'domain_results2.csv', 'merged.csv')
