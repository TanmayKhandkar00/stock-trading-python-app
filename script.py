import requests
import openai
from dotenv import load_dotenv
import os
from collections import deque
import time
import csv
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")



# LIMIT = 1000
# url = f"https://api.polygon.io/v3/reference/tickers/?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

# response = requests.get(url)

# tickers = []

# data = response.json()

# for ticker in data['results']:
#     tickers.append(ticker['ticker'])

# while 'next_url' in data:
#     print('requesting next page', data['next_url'])
#     response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
#     data = response.json()
#     print(data)
#     for ticker in data['results']:
#         tickers.append(ticker['ticker'])



MAX_CALLS = 5
WINDOW = 60.0  # seconds

timestamps = deque()
session = requests.Session()  # reuse TCP connection

def rate_limited_get(url, **kwargs):
    now = time.monotonic()

    # If we've already made MAX_CALLS within the last WINDOW, wait.
    while len(timestamps) >= MAX_CALLS and (now - timestamps[0]) < WINDOW:
        sleep_for = timestamps[0] + WINDOW - now
        if sleep_for > 0:
            time.sleep(sleep_for)
        # After sleeping, recompute 'now'
        now = time.monotonic()

    # Drop any timestamps that are outside the window
    while timestamps and (now - timestamps[0]) >= WINDOW:
        timestamps.popleft()

    # Record this call and proceed
    timestamps.append(now)
    return session.get(url, **kwargs)

LIMIT = 1000


url = f"https://api.polygon.io/v3/reference/tickers/?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

resp = rate_limited_get(url, timeout=15)
data = resp.json()

# collect full objects matching API response schema
tickers = list(data.get('results', []))

while 'next_url' in data and data['next_url']:
    print('requesting next page', data['next_url'])
    resp = rate_limited_get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}', timeout=15)
    data = resp.json()
    page = data.get('results', [])
    if isinstance(page, list):
        tickers.extend(page)

exapmle_ticker = {'ticker': 'BIT', 
 'name': 'BLACKROCK MULTI-SECTOR INCOME TRUST', 
 'market': 'stocks', 
 'locale': 'us', 
 'primary_exchange': 'XNYS', 
 'type': 'FUND', 
 'active': True, 
 'currency_name': 'usd',  
 'cik': '0001562818', 
 'composite_figi': 'BBG003P84BH1', 
 'share_class_figi': 'BBG003P84C70', 
 'last_updated_utc': '2025-10-29T06:06:31.255055438Z'}

# while 'next_url' in data:

#     print('requesting next page', data['next_url'])
#     print(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
#     response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
#     data1 = response.json()
#     print(data1)

#     for item in data1['results']:
#         tickers.append(item)
    

headers = list(exapmle_ticker.keys())

# write CSV with the same schema as example_ticker
output_csv = 'tickers.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
    writer.writeheader()
    for item in tickers:
        row = {key: item.get(key, '') for key in headers}
        writer.writerow(row)

print(f"Wrote {len(tickers)} rows to {output_csv}")


