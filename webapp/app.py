from datetime import datetime
from flask import Flask, render_template
import requests
import os
import json 
from pytz import timezone

app = Flask(__name__)

@app.route('/')
def index():
    tz = timezone('EST')
    today = datetime.now(tz).strftime('%Y-%m-%d')
    res = requests.get(os.environ["URL"])
    products = json.loads(res.text).get("Products")
    for product in products:
        if product['last_updated'] != today:
            product['received'] = 0
            product['shipped'] = 0
            product['returned'] = 0
    return render_template('index.html', date=today, products=products)

if __name__ == '__main__':
   app.run()