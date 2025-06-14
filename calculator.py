import requests
import json
# Hypixel Skyblock Auction House API Example

api_key = "39244af7-0918-45b1-8920-c05bdd7ef1a7"

headers = {
    "API-Key": api_key
}

mastiff_auctions = []
for page_num in range(0,64):
    api_url = f"https://api.hypixel.net/v2/skyblock/auctions?page={page_num}"
    print(f"Fetching data from: {api_url}")
    x = requests.get(api_url, headers=headers)
    chunks = x.json()
    for s in chunks['auctions']:
        if s['item_name'] == 'Mastiff Boots' or s['item_name'] == 'Mastiff Crown' or s['item_name'] == 'Mastiff Chestplate' or s['item_name'] == 'Mastiff Leggings':
            # print(f"Mastiff Boots in auction {s['auction_id']}")

            # print(s)
            mastiff_auctions.append(s)

mastiff_bins = []

for t in mastiff_auctions:
    
    # Check if the value for the key 'bin' is True
    if t['bin'] == True:
        mastiff_bins.append(t)
        # Print the auction's 'uuid' (the correct key for the ID)
        print(f"BIN Auction found for Mastiff Boots: {t['uuid']}")
        
mastiff_chestplates = [item for item in mastiff_bins if item['item_name'] == 'Mastiff Chestplate']
mastiff_leggings = [item for item in mastiff_bins if item['item_name'] == 'Mastiff Leggings']
mastiff_boots = [item for item in mastiff_bins if item['item_name'] == 'Mastiff Boots']
mastiff_crowns = [item for item in mastiff_bins if item['item_name'] == 'Mastiff Crown']

sorted_boots_bins = sorted(mastiff_boots, key=lambda s: s['starting_bid'])
sorted_chestplate_bins = sorted(mastiff_chestplates, key=lambda s: s['starting_bid'])
sorted_leggings_bins = sorted(mastiff_leggings, key=lambda s: s['starting_bid'])
sorted_crown_bins = sorted(mastiff_crowns, key=lambda s: s['starting_bid'])


print("Lowest Chestplate BIN: ", sorted_chestplate_bins[0]['starting_bid'])
print("Lowest Leggings BIN: ", sorted_leggings_bins[0]['starting_bid'])
print("Lowest Boots BIN: ", sorted_boots_bins[0]['starting_bid'])
print("Lowest Crown BIN: ", sorted_crown_bins[0]['starting_bid'])   

# # with open('auctions.json', 'w') as f:
# #     json.dump(mastiff_bins, f, indent=2) 


bazaar_api_url = "https://api.hypixel.net/v2/skyblock/bazaar"
bazaar_response = requests.get(bazaar_api_url, headers=headers)

products = bazaar_response.json().get('products', {})

for a in products.values():
    if a['product_id'] == "GOLDEN_TOOTH":
        quick_summary = a['quick_status']
        golden_tooth_price = quick_summary['sellPrice']

    if a['product_id'] == "ENCHANTED_DARK_OAK_LOG":
        quick_summary = a['quick_status']
        edarkoak_price = quick_summary['sellPrice']

    if a['product_id'] == "ENCHANTED_DIAMOND":
        quick_summary = a['quick_status']
        ediamond_price = quick_summary['sellPrice']

    if a['product_id'] == "ENCHANTED_GOLD":
        quick_summary = a['quick_status']
        egold_price = quick_summary['sellPrice']

        # for p in a:
        #     for z in p:
        #      print(z)
        #      print(f"Golden Tooth found in Bazaar: available for buy order at {p['sellPrice']} coins")
            
print(f"Golden Tooth price: {golden_tooth_price} coins")
print(f"Enchanted Dark Oak Log price: {edarkoak_price} coins")
print(f"Enchanted Diamond price: {ediamond_price} coins")
print(f"Enchanted Gold price: {egold_price} coins")

mastiff_hemlet_price = golden_tooth_price * 4 + edarkoak_price * 320 + egold_price * 64
mastiff_chestplate_price = golden_tooth_price * 4 + edarkoak_price * 512 + egold_price * 64
mastiff_leggings_price = golden_tooth_price * 4 + edarkoak_price * 428 + ediamond_price * 64
mastiff_leggings_price = golden_tooth_price * 4 + edarkoak_price * 256 + ediamond_price * 64

print(f"Mastiff Hemlet price: {mastiff_hemlet_price} coins")
print(f"Mastiff Chestplate price: {mastiff_chestplate_price} coins")
print(f"Mastiff Leggings price: {mastiff_leggings_price} coins")
print(f"Mastiff Boots price: {mastiff_leggings_price} coins")

print(f"Mastiff profit for chestplate: {sorted_chestplate_bins[0]['starting_bid'] - mastiff_chestplate_price} coins")
print(f"Mastiff profit for leggings: {sorted_leggings_bins[0]['starting_bid'] - mastiff_leggings_price} coins")
print(f"Mastiff profit for boots: {sorted_boots_bins[0]['starting_bid'] - mastiff_leggings_price} coins")
print(f"Mastiff profit for crown: {sorted_crown_bins[0]['starting_bid'] - mastiff_hemlet_price} coins")

with open('bazaar.json', 'w') as f:
    json.dump(products, f, indent=2) 