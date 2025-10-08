# import requests
# import openai
# from dotenv import load_dotenv
# import os
# load_dotenv()

# POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# print(POLYGON_API_KEY)

# LIMIT = 1000
# url = f"https://api.polygon.io/v3/reference/tickers/?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

# response = requests.get(url)
# tickers = []
# data = response.json()



# while 'next_url' in data:

#     print('requesting next page', data['next_url'])
#     print(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
#     response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
#     data1 = response.json()
#     print(data1)

#     for item in data1['results']:
#         tickers.append(item)
    

# print(len(tickers))



# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# print(POLYGON_API_KEY)

# LIMIT = 1000
# url = f"https://api.polygon.io/v3/reference/tickers/?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

# response = requests.get(url)
# data = response.json()

# tickers = []

# # Add first page results
# if 'results' in data:
#     tickers.extend(data['results'])

# # Paginate through next pages
# while 'next_url' in data:
#     print('requesting next page', data['next_url'])
#     response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
#     data = response.json()
#     if 'results' in data:
#         tickers.extend(data['results'])

# print(len(tickers))
# import time

# # Add first page
# if 'results' in data:
#     tickers.extend(data['results'])

# # Pagination loop
# while 'next_url' in data:
#     print('requesting next page', data['next_url'])
#     response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
#     data = response.json()
    
#     # Handle rate limit or errors
#     if data.get('status') == "ERROR":
#         print("Error:", data.get("error"))
#         print("Waiting 60 seconds before retrying...")
#         time.sleep(60)
#         continue  # retry loop
    
#     if 'results' in data:
#         tickers.extend(data['results'])
#     else:
#         break  # no results, stop loop

# print("Total tickers fetched:", len(tickers))
import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

print("Using API key:", POLYGON_API_KEY)

LIMIT = 1000
url = f"https://api.polygon.io/v3/reference/tickers/?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

# First request
response = requests.get(url)
data = response.json()

tickers = []

# Add first page results
if 'results' in data:
    tickers.extend(data['results'])

# Pagination loop
while 'next_url' in data:
    print('Requesting next page:', data['next_url'])
    response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
    data = response.json()
    
    # Handle rate limit or errors
    if data.get('status') == "ERROR":
        print("Error:", data.get("error"))
        print("Waiting 60 seconds before retrying...")
        time.sleep(60)
        continue  # retry loop
    
    if 'results' in data:
        tickers.extend(data['results'])
    else:
        break  # no results, stop loop

print("Total tickers fetched:", len(tickers))
