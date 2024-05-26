from flask import Flask

DEBUG = True

app = Flask("crosslister")

# Default landing page route
@app.route("/")
def home():
    with open("./static/index.html", "r") as f:
        content = f.read()
    return content

@app.route("/scrape")
def scrape():
    return "Done!"

if __name__ == "__main__":
    app.run(debug=DEBUG, port=5000) 