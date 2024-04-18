import openai
import pandas as pd
import json

total_prompt_tokens = 0
total_completion_tokens = 0

def get_website_type(url):
    global total_prompt_tokens, total_completion_tokens
    prompt = f"What type of website is {url}? If it's an ecommerce platform that sells more than two different brands, respond with 'marketplace'. If it's a news articles, content publishing, or a blog website providing information, respond with 'News/Blog'. If the website doesn't fit into any of these categories or if it's completely irrelevant, respond with 'None' in JSON format: {{'type': '', 'description': ''}}"
    openai_msg = [{"role": "system", "content": prompt}]
    response = openai.chat.completions.create(
        temperature=0,
        model="southindia35",
        messages=openai_msg
    )
    total_prompt_tokens += response.usage.prompt_tokens
    total_completion_tokens += response.usage.completion_tokens
    print(total_completion_tokens)
    print(total_prompt_tokens)

    content = response.choices[0].message.content.replace("'", '"')
    try:
        content_json = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for URL {url}: {e}")
        return None
    return content_json

excel_file_path = 'test.xlsx'
output_file_path = 'test_result.xlsx'

df = pd.read_excel(excel_file_path)
df['Type'] = ''
df['Description'] = ''

for index, row in df.iterrows():
    website_url = row['URL']
    website_info = get_website_type(website_url)
    if website_info is not None:
        df.at[index, 'Type'] = website_info.get('type', '')
        df.at[index, 'Description'] = website_info.get('description', '')
    else:
        print(f"Skipped URL due to JSON issues: {website_url}")

df.to_excel(output_file_path, index=False)

print("Prediction complete. Check test_result.xlsx for results.")
print("Total prompt tokens:", total_prompt_tokens)
print("Total completion tokens:", total_completion_tokens)
