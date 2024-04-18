import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os.path
import json
import threading

country_codes = ['global', 'af', 'al', 'dz', 'ao', 'ar', 'am', 'au', 'at', 'az', 'bs', 'bh', 'bd', 'by', 'be', 'bz', 'bo', 'ba', 'bw']

category_codes = ['accounting-and-auditing', 'advertising-and-marketing', 'aerospace-and-defense', 'agriculture', 'airlines', 'apparel-and-fashion', 'architecture', 'automotive', 'beauty-and-cosmetics', 'computers-and-electronics', 'consumer-electronics', 'entertainment', 'finance', 'food-and-beverages', 'healthcare', 'market-research', 'mass-media', 'merged_file', 'newspapers', 'publishing', 'retail', 'travel-and-tourism', 'warehousing', 'wellness', 'wholesalers-and-liquidators', 'wine-and-spirits', 'writing-and-editing-services']

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
]

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

# File checks
csv_filename = 'country_category_data3.csv'
failed_requests_file = 'failed_requests.csv'

if not os.path.exists(csv_filename):
    with open(csv_filename, 'w') as f:
        f.write('Country Code,Category,Domain Name,Total Traffic\n')

if not os.path.exists(failed_requests_file):
    with open(failed_requests_file, 'w') as f:
        f.write('Country Code,Category,URL\n')

data_to_append = []  # Define data_to_append in the global scope

def append_to_csv(data_to_append):
    with open(csv_filename, 'a') as f:
        for row in data_to_append:
            f.write(','.join(map(str, row)) + '\n')

def scrape_website_data(country_code, category_code, failed_urls, scraped_count):
    url = f"https://www.semrush.com/trending-websites/{country_code}/{category_code}"
    headers = {'User-Agent': user_agents[threading.current_thread().ident % len(user_agents)]}
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
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
            return

        json_str = data_script.split('=', 1)[1].strip()
        json_str = json_str.rstrip(';\n')  # Trimming the trailing semicolon if it exists
        data = json.loads(json_str)  # Safe parsing

        domain_traffic_data = data['data']['domains']  # Access data

        # Append data to the list for writing to CSV
        for item in domain_traffic_data:
            data_to_append.append([country_code, category_code, item['domain_name'], item['total_traffic']])

        # Increment scraped count
        scraped_count[0] += len(domain_traffic_data)

        # Check if 1000 URLs have been scraped
        if scraped_count[0] >= 1000:
            append_to_csv(data_to_append)
            # Reset scraped count and failed URLs
            scraped_count[0] = 0
            del failed_urls[:]
            del data_to_append[:]

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        # Store failed URL
        failed_urls.append((country_code, category_code, url))

def thread_worker():
    while True:
        if not categories:
            break
        country_code, category_code = categories.pop()
        failed_urls = []
        scraped_count = [0]  # Using list to allow modification within the function
        print(f"Processing {country_code} - {category_code}")
        scrape_website_data(country_code, category_code, failed_urls, scraped_count)

# Populate categories list with all combinations of country and category codes
categories = [(country_code, category_code) for country_code in country_codes for category_code in category_codes]

# Create and start threads
threads = []
for _ in range(5):
    thread = threading.Thread(target=thread_worker)
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Write any remaining data to CSV
if data_to_append:
    append_to_csv(data_to_append)
