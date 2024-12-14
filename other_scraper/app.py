from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            # Extract all links from the page
            links = [a["href"] for a in soup.find_all("a", href=True)]
            return render_template("index.html", links=links, url=url)
        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html", links=None)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6800)
