from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import schedule
import time
import threading

app = Flask(__name__)

# Funzione di scraping
def get_product_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Errore nella richiesta della pagina")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='s-main-slot s-result-list s-search-results sg-row')
    product_list = []
    for product in products:
        try:
            name = product.find('span', class_='a-text-normal').text.strip()
            price = product.find('span', class_='a-price-whole')
            price = price.text.strip() if price else 'N/A'
            product_list.append({'name': name, 'price': price})
        except AttributeError:
            continue
    return product_list

# Job di scraping (periodico)
def job():
    url = "https://www.amazon.it/s?k=smartphone"
    products = get_product_data(url)
    return products

# Rotta principale (per visualizzare la dashboard)
@app.route('/')
def index():
    products = job()  # Ottenere i prodotti dallo scraping
    return render_template('index.html', products=products)

# Rotta di ricerca (con filtri)
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    price_filter = request.form['price']
    products = job()

    # Filtrare i prodotti in base alla ricerca
    filtered_products = [product for product in products if query.lower() in product['name'].lower()]

    if price_filter:
        filtered_products = [product for product in filtered_products if product['price'] == price_filter]

    return render_template('index.html', products=filtered_products)

# Funzione per eseguire il job di scraping ogni giorno
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    schedule.every().day.at("09:00").do(job)
    threading.Thread(target=run_schedule, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
