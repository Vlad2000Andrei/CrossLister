import shopify
from listing import Listing
from tqdm import tqdm
from time import sleep

class Publisher:
    def __init__(self): 
        pass

    def authenticate(self):
        pass

    def publish(self):
        pass

class ShopifyPublisher(Publisher):
    def __init__(self, shop_url, api_token):
        self.shop_url = shop_url
        self.api_token = api_token
        self.session = None
    
    def authenticate(self):
        print("[i] Authenticating to Shopify.")
        self.session = shopify.Session(shop_url=self.shop_url, version="2024-04", token=self.api_token)
        shopify.ShopifyResource.activate_session(self.session)

    def make_options(self, listing : Listing):
        to_import = ["Color", "Size"]
        product_options = []

        for option in to_import:
            try:
                product_options.append(shopify.Option(
                    {
                        "name": option,
                        "values": [listing.properties[option.lower()]]
                    }
                ))
            except:
                print(f"Could not find property {option} in listing source. Add manually please.")
        return product_options
    
    def make_default_variant(self, listing : Listing, options):
        variant_options = {}
        optionNr = 1

        for option in options:
            option_name = f"option{optionNr}"
            optionNr += 1
            option_value = option.values[0]

            variant_options[option_name] = option_value

        variant_options["price"] = listing.price
        variant_options["inventory_management"] = "shopify"

        return shopify.Variant(variant_options)

    def publish(self, listing : Listing):
        print(f"[i] Publishing to Shopify.")
        if not self.session:
            self.authenticate()

        options = self.make_options(listing)
        variant = self.make_default_variant(listing, options)

        try:
            product = shopify.Product()
            product.title = f"{listing.title}"
            product.body_html = listing.description
            product.vendor = "Retro Urban Wear"
            product.status = "draft"
            product.variants = [variant]
            product.options = options
            created = product.save()

            if not created:
                raise Exception("Product was not created on Shopify. Unkown Error.")
            
            inventory_item_id = product.variants[0].inventory_item_id
            location_id = shopify.Location.find()[0].id

            inventory_level = shopify.InventoryLevel()
            inventory_level.adjust(location_id = location_id, inventory_item_id = inventory_item_id, available_adjustment=1)

            print("[i] Publishig images to Shopify.")
            for img in tqdm(listing.images):
                image = shopify.Image()
                image.product_id = product.id
                image.src = img
                outcome = image.save()

                if not outcome:
                    raise Exception(f"Could not upload picture {listing.images.index(img) + 1} ( {img} )")
                
                sleep(0.7) # Limited to 2 requests per second, so this is fore safety.

        except Exception as e:
            print(f"[ERR] {str(e)}")