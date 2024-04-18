import openai
import pandas as pd
import json
import csv
import time  # Import the time module for sleeping



total_prompt_tokens = 0
total_completion_tokens = 0

def get_website_type(domain_name):
    global total_prompt_tokens, total_completion_tokens
    prompt = f"What type of website is {domain_name}? If it's an ecommerce platform that sells more than two different brands, respond with 'marketplace'. If it's news articles, content publishing, or a blog website providing information, respond with 'News/Blog'. If the website doesn't fit into any of these categories or if it's completely irrelevant, respond with 'None' in JSON format: {{'type': '', 'description': ''}}"
    openai_msg = [{"role": "system", "content": prompt}]
    response = openai.chat.completions.create(
        temperature=0,
        model="southindia35",
        messages=openai_msg
    )
    total_prompt_tokens += response.usage.prompt_tokens
    total_completion_tokens += response.usage.completion_tokens

    # Convert single quotes to double quotes and remove leading/trailing characters if needed
    content = response.choices[0].message.content.replace("'", '"')
    try:
        # Try parsing the adjusted JSON string
        content_json = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for domain {domain_name}: {e}")
        return None  # Or handle as appropriate
    return content_json

input_file_path = 'filtered_file.csv'
output_file_path = 'domain_results.csv'

# Set up the output CSV file and write headers if it does not exist
with open(output_file_path, mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Domain Name', 'Total Traffic', 'Type', 'Description'])
    if file.tell() == 0:  # Check if file is empty
        writer.writeheader()

# Read from the input CSV file
df = pd.read_csv(input_file_path)

for index, row in df.iterrows():
    domain_name = row['Domain Name']
    total_traffic = row['Total Traffic']
    website_info = get_website_type(domain_name)
    if website_info is not None:
        result = {
            'Domain Name': domain_name,
            'Total Traffic': total_traffic,
            'Type': website_info.get('type', ''),
            'Description': website_info.get('description', '')
        }
        # Write results to the output CSV file
        with open(output_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Domain Name', 'Total Traffic', 'Type', 'Description'])
            writer.writerow(result)
    else:
        print(f"Skipped domain due to JSON issues: {domain_name}")

    # Sleep for 30 seconds every 800 rows
    if (index + 1) % 400 == 0:
        print("Sleeping for 30 seconds...")
        time.sleep(30)

print("Prediction complete. Check domain_results.csv for results.")
print("Total prompt tokens:", total_prompt_tokens)
print("Total completion tokens:", total_completion_tokens)
