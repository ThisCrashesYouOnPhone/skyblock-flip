import requests
import json
# Hypixel Skyblock Auction House API Example

api_key = "39244af7-0918-45b1-8920-c05bdd7ef1a7"
api_url = "https://api.hypixel.net/v2/skyblock/auctions?page=2"

headers = {
    "API-Key": api_key
}
all_auctions = []
for page_num in range(1,5):
    api_url = f"https://api.hypixel.net/v2/skyblock/auctions?page={page_num}"
    print(f"Fetching data from: {api_url}")
    x = requests.get(api_url, headers=headers)
    all_auctions.append(x.json())
    # Fetching the data from the API

with open('auctions.json', 'w') as f:
    json.dump(all_auctions, f) 

print(all_auctions)