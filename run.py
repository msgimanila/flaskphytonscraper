from flask import Flask
 
from run_scrapy import run_spider



app = Flask(__name__)

 

if __name__ == '__main__':
    print("Running Scrapy spider automatically...")
    run_spider()  # Automatically run Scrapy before starting the Flask server
    app.run(debug=True)