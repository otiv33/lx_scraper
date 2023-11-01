from flask import Flask, render_template
from DB.db import Db
from web_scraper.web_scraper_runner import WebScraperRunner

app = Flask(__name__)

# Initial scrape data and fill DB
with app.app_context():
    results = WebScraperRunner().run_spider()
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