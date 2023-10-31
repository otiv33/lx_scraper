from flask import Flask, jsonify, render_template
from web_scraper import WebScraper
from db import Db

app = Flask(__name__)

with app.app_context():
    results = WebScraper().run_spider()
    db = Db()
    db.fill_data(results)
    
# Get all apartments
@app.route('/', methods=['GET'])
def get_apartments():
    db = Db()
    apts = db.get_apartments()
    return render_template('index.html', apartments=apts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)