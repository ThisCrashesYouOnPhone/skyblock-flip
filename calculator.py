import requests
import json
# Hypixel Skyblock Auction House API Example

api_key = "39244af7-0918-45b1-8920-c05bdd7ef1a7"
api_url = "https://api.hypixel.net/v2/skyblock/auctions"

data = requests.get(api_url).json()

with open('auctions.json', 'w') as f:
    json.dump(data, f) 

print(data)