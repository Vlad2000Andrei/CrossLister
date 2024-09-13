import requests
import bs4
from tqdm import tqdm
from listing import Listing

class Scraper:
    def __init__(self):
        pass

    def scrape (self, url : str):
        # Scrape the URL and return the data
        pass

    def scrape_all (self, urls : list[str]):
        result = []
        for url in tqdm(urls):
            result.append(self.scrape(url))
        return result

class VintedScraper (Scraper):
    def scrape(self, url):
        soup = self.get_webpage(url)

        if not soup:
            return None

        try:
            images = self.get_images(soup)
            properties = self.get_properties(soup)
            title = self.get_title(soup)
            description = self.get_description(soup)
            price = self.get_price(soup)
            return Listing(title, description, price, images, properties)
        except Exception as e:
            print(f"[ERR] Got page {url} but could not retrieve attributes from page contents.", f"\t>> Error is {e} on line {e.__traceback__.tb_lineno}.", sep="\n")
            return None
        


    def get_webpage(self, url : str) -> bs4.BeautifulSoup:
        print(f"[i] Getting webpage {url}.")
        if "vinted.nl" in url:
            print("\t[!] URL is for Dutch Vinted (vinted.nl). Replacing with vinted.com for English content.")
            url = url.replace("vinted.nl", "vinted.com")

        try:
            html_text = requests.get(url)
            soup = bs4.BeautifulSoup(html_text.text, 'html.parser')
            return soup
        except Exception as e:
            print(f"Could not get and parse {url}.", e)
            return None

    def get_images(self, soup : bs4.BeautifulSoup):
        print("[i] Parsing images.")
        photo_container = soup.find(class_="item-photos")
        image_tags = photo_container.find_all("img")
        photo_urls = [img['src'] for img in image_tags]
        return photo_urls

    def get_properties(self, soup : bs4.BeautifulSoup):
        print(f"[i] Parsing item properties.")
        detail_items_html = soup.find_all(class_="details-list__item")
        details = {}
        for detail_tem in detail_items_html:
            label = detail_tem.find(class_="details-list__item-title")
            if label:
                label = label.text

            value = detail_tem.find(class_="details-list__item-value")
            if value:
                value = value.text
                if value.endswith("Brand menu"):
                    value = value.replace("Brand menu", "")

            if label and value:
                details[label.lower()] = value
        return details

    def get_title(self, soup : bs4.BeautifulSoup):
        print("[i] Parsing title.")
        title = soup.find("title").text
        title = title.replace(" | Vinted", "")
        return title

    def get_description(self, soup : bs4.BeautifulSoup):
        print("[i] Parsing description.")
        desc_container = soup.select_one("div.details-list--info")
        spans = desc_container.find_all("span")
        innermost = [span for span in spans if not span.has_attr('class')]
        description = innermost[0].text
        return description

    def get_price(self, soup : bs4.BeautifulSoup):
        print("[i] Parsing price.")
        price = soup.select_one('div[data-testid="item-price"] p').text
        try:
            price = float(price)
        except:
            price = float(price[1:])
        return str(price)