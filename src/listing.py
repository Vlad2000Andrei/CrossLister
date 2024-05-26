class Listing:
    def __init__ (self, title, description, price, images, properties : dict):
        self.title = title
        self.description = description
        self.price = price
        self.images = images
        self.properties = properties

    def __str__(self) -> str:
        result = ""
        result += "-"*80 + "\n"
        result += f"Title: \t{self.title}\n"
        result += f"Price: \t{self.price}\n"
        result += f"Desc: \t{self.description}\n"

        result += f"Properties:\n"
        for (name, value) in self.properties.items():
            result += f"\t {name}: \t{value}\n"
        
        result += f"Images:\n"
        for img in self.images:
            result += f"\t {self.images.index(img) + 1}.) {img}\n"

        result += "-"*80 + "\n"

        return result