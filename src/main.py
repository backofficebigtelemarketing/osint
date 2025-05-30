from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Funzione di scraping per raccogliere i dati dai vari siti
def get_best_prices(product_name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Simulazione di scraping da più siti (esempio Amazon, MediaWorld, eBay, ecc.)
    results = []

    # Esempio di scraping Amazon (modifica con URL effettivi)
    amazon_url = f'https://www.amazon.it/s?k={product_name}'
    response = requests.get(amazon_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', {'class': 's-main-slot s-result-list s-search-results sg-row'})
        for item in items:
            name = item.find('span', class_='a-text-normal')
            price = item.find('span', class_='a-price-whole')
            if name and price:
                results.append({
                    'name': name.text.strip(),
                    'price': price.text.strip(),
                    'store': 'Amazon',
                    'url': amazon_url
                })

    # Aggiungi altre fonti di scraping (ad esempio, MediaWorld, eBay)

    return results

# Rotta principale per visualizzare i prodotti
@app.route('/')
def index():
    return render_template('index.html')

# Rotta di ricerca per filtrare i prodotti
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    print(f"Ricerca per: {query}")
    products = get_best_prices(query)  # Ottieni i migliori prezzi per il prodotto
    return render_template('index.html', products=products, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Flask ascolta su tutte le interfacce

