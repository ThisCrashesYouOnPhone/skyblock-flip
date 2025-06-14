import asyncio
import httpx # The async-compatible requests library
import time

# --- Configuration ---
API_KEY = "39244af7-0918-45b1-8920-c05bdd7ef1a7"  # Replace with your API key
HEADERS = {"API-Key": API_KEY}
API_URL = "https://api.hypixel.net/v2/skyblock/auctions"

# The exact names of the Mastiff armor pieces to find
MASTIFF_PIECES = {
    "Mastiff Crown",
    "Mastiff Chestplate",
    "Mastiff Leggings",
    "Mastiff Boots"
}

# --- Performance Tuning ---
# How many requests to send out at the same time.
# IMPORTANT: Setting this too high (>50) will likely get you rate-limited by the API.
CONCURRENCY_LIMIT = 50

# A shared dictionary to hold the results. It's safe to access in asyncio
# without a lock for this specific use case.
lowest_bins = {
    piece: {"price": float('inf'), "uuid": None}
    for piece in MASTIFF_PIECES
}

async def fetch_and_process_page(client, page_num, semaphore):
    """
    An async worker that fetches one page, processes its auctions, and updates
    the shared lowest_bins dictionary. The semaphore controls concurrency.
    """
    async with semaphore: # This waits until a "slot" is free to run
        try:
            response = await client.get(f"{API_URL}?page={page_num}", headers=HEADERS)
            response.raise_for_status() # Raise an error on 4xx/5xx responses
            data = response.json()
            
            auctions = data.get('auctions', [])
            
            for auction in auctions:
                if not auction.get('bin'):
                    continue

                item_name = auction.get('item_name')
                if item_name in MASTIFF_PIECES:
                    price = auction.get('starting_bid', 0)
                    # This check-and-set is atomic enough for asyncio
                    if price < lowest_bins[item_name]['price']:
                        print(f"  -> New lowest for {item_name}! Price: {price:,.0f} (Page {page_num})")
                        lowest_bins[item_name]['price'] = price
                        lowest_bins[item_name]['uuid'] = auction.get('uuid')

        except httpx.HTTPStatusError as e:
            print(f"Error processing page {page_num}: {e.response.status_code} - Rate limit likely hit.")
        except Exception as e:
            print(f"An error occurred on page {page_num}: {e}")

async def main():
    """
    Main async function to orchestrate the fetching and processing.
    """
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Error: Please replace 'YOUR_API_KEY_HERE' with your actual API key.")
        return

    start_time = time.time()
    
    # Use an async client session for connection pooling and better performance
    async with httpx.AsyncClient() as client:
        # --- Step 1: Get total page count ---
        print("Fetching auction house metadata...")
        try:
            initial_response = await client.get(API_URL, headers=HEADERS)
            initial_response.raise_for_status()
            total_pages = initial_response.json().get('totalPages', 0)
            print(f"Found {total_pages} pages. Preparing to fetch concurrently...")
        except Exception as e:
            print(f"Could not fetch initial data. Aborting. Error: {e}")
            return
            
        # --- Step 2: Create tasks and control concurrency with a Semaphore ---
        semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
        tasks = []
        for page_num in range(total_pages):
            task = fetch_and_process_page(client, page_num, semaphore)
            tasks.append(task)
            
        # --- Step 3: Run all tasks ---
        print(f"Scanning all pages with a concurrency of {CONCURRENCY_LIMIT}...")
        await asyncio.gather(*tasks)

    # --- Step 4: Print final results ---
    duration = time.time() - start_time
    print("\n-------------------------------------------")
    print(f"           Scan Complete!")
    print(f"       (Took {duration:.2f} seconds)")
    print("-------------------------------------------")
    for piece, data in lowest_bins.items():
        if data['price'] != float('inf'):
            price_str = f"{data['price']:,.0f} coins"
            print(f"{piece:<20}: {price_str}")
            print(f"  Auction ID: {data['uuid']}")
        else:
            print(f"{piece:<20}: Not found")
    print("-------------------------------------------")


# --- Run the async main function ---
if __name__ == "__main__":
    # On Windows, you might need a specific policy for asyncio to work smoothly
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())