from listing import Listing
from publisher import ShopifyPublisher
from scraper import VintedScraper
from os import path

def get_YN(text : str):
    print(text)
    while True:
        answer = input("Please confirm (Y / N):  ")
        if answer.lower() in ["yes", "y", "confirm"]:
            return True
        if answer.lower() in ["n", "no", "no", "cancel", "stop", "quit"]:
            return False
        print(f'"{answer}" is not a valid answer. Please type Y, y, N, or n, then press Enter.')

api_token = None
while not api_token:
    if not path.isfile("./shopify_api_token.secret"):
        read_token = input("[ERR] No API Token found locally. Please type it and press enter: ")
        with open("./shopify_api_token.secret", "w") as f:
            f.write(read_token)
        print("[i] Token saved successfully!")
        api_token = read_token
    else:
        try:
            with open("./shopify_api_token.secret", "r") as f:
                api_token = f.read()
        except Exception as e:
            print("[ERR] Could not save token to file. Exiting...")
            exit(-1)

# Scrape data
scraper = VintedScraper()
publisher = ShopifyPublisher("https://9014a6-4.myshopify.com/", api_token)

while True:
    vinted_url = input("\n\n(Ctrl + C to quit!) Please enter your Vinted URL: ").strip()
    listing = scraper.scrape(vinted_url)

    if not listing:
        print(f"[ERR] Could not scrape data from {vinted_url}")
        continue

    print("Scraped Item:", listing, sep="\n")
    if get_YN("Publish to Shopify?"):
        publisher.publish(listing)
    else:
        print("[i] Cancelled publication.")