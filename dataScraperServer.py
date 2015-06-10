from dataScraper import pipeline
from flask import Flask 
import json
app = Flask(__name__)


@app.route("/")
def index(name=None):
    return app.send_static_file('index.html')

@app.route("/get_price/<upc>")
def get_price(upc):
    product_info = pipeline( str(upc ) )
    if product_info == None:
        product_info = {'price': 'None'}
    return json.dumps(product_info)

if __name__ == "__main__":
    app.run(debug=True)