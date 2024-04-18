import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path
import json

country_codes = ['global', 'af', 'al', 'dz', 'ao', 'ar', 'am', 'au', 'at', 'az', 'bs', 'bh', 'bd', 'by', 'be', 'bz', 'bo', 'ba', 'bw', 'br', 'bn', 'bg', 'cv', 'kh', 'cm', 'ca', 'cl', 'co', 'cg', 'cr', 'hr', 'cy', 'cz', 'dk', 'do', 'ec', 'eg', 'sv', 'ee', 'et', 'fi', 'fr', 'ge', 'de', 'gh', 'gr', 'gt', 'gy', 'ht', 'hn', 'hk', 'hu', 'is', 'in', 'id', 'ie', 'il', 'it', 'jm', 'jp', 'jo', 'kz', 'kw', 'lv', 'lb', 'ly', 'lt', 'lu', 'mg', 'my', 'mt', 'mu', 'mx', 'md', 'mn', 'me', 'ma', 'mz', 'na', 'np', 'nl', 'nz', 'ni', 'ng', 'no', 'om', 'pk', 'py', 'pe', 'ph', 'pl', 'pt', 'ro', 'ru', 'sa', 'sn', 'rs', 'sg', 'lk', 'sk', 'si', 'za', 'kr', 'es', 'se', 'th', 'tt', 'tn', 'tr', 'ua', 'ae', 'uk', 'us', 'uy', 've', 'vn', 'zm', 'zw']

category_codes = ['accounting-and-auditing', 'advertising-and-marketing', 'aerospace-and-defense', 'agriculture', 'airlines', 'apparel-and-fashion', 'architecture', 'automotive', 'beauty-and-cosmetics', 'computers-and-electronics', 'consumer-electronics', 'entertainment', 'finance', 'food-and-beverages', 'healthcare', 'market-research', 'mass-media', 'merged_file', 'newspapers', 'publishing', 'retail', 'travel-and-tourism', 'warehousing', 'wellness', 'wholesalers-and-liquidators', 'wine-and-spirits', 'writing-and-editing-services']


# File checks
csv_filename = 'country_category_data.csv'
xlsx_filename = 'country_category_data.xlsx'

if not os.path.exists(csv_filename):
    with open(csv_filename, 'w') as f:
        f.write('Domain Name,Total Traffic\n')

if not os.path.exists(xlsx_filename):
    df_init = pd.DataFrame(columns=['Domain Name', 'Total Traffic'])
    df_init.to_excel(xlsx_filename, index=False)

# Iterate over each country and category
for country_code in country_codes:
    for category_code in category_codes:
        url = f"https://www.semrush.com/trending-websites/{country_code}/{category_code}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the script containing '__PRELOADED_STATE__'
        script_tags = soup.find_all("script")
        data_script = None
        for script in script_tags:
            if '__PRELOADED_STATE__' in script.text:
                data_script = script.text
                break

        if data_script is None:
            print(f"No data found for {country_code} - {category_code}")
            continue

        try:
            json_str = data_script.split('=', 1)[1].strip()
            json_str = json_str.rstrip(';\n')  # Trimming the trailing semicolon if it exists
            data = json.loads(json_str)  # Safe parsing

            domain_traffic_data = data['data']['domains']  # Access data

            # Append data to CSV
            with open(csv_filename, 'a') as f:
                for item in domain_traffic_data:
                    f.write(f"{item['domain_name']},{item['total_traffic']}\n")

            # Append data to Excel
            df_append = pd.DataFrame({
                        'Domain Name': [item['domain_name'] for item in domain_traffic_data],
                        'Total Traffic': [item['total_traffic'] for item in domain_traffic_data]
                    })

            with pd.ExcelWriter(xlsx_filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_append.to_excel(writer, index=False, header=not os.path.exists(xlsx_filename), sheet_name='Sheet1')

        except KeyError as e:
            print(f"Missing data for {country_code} - {category_code}: {e}")
            continue
        except json.JSONDecodeError as e:
            print(f"JSON parsing error for {country_code} - {category_code}: {e}")
            continue