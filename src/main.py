from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Funzione di scraping per raccogliere i dati dai vari siti
def get_product_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
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

# Rotta principale per visualizzare i prodotti
@app.route('/')
def index():
    products = get_product_data('https://www.amazon.it/s?k=telefonia')  # esempio URL di ricerca
    return render_template('index.html', products=products)

# Rotta di ricerca per filtrare i prodotti
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    print("Query di ricerca:", query)  # Aggiungi debug per vedere la query
    
    products = get_product_data('https://www.amazon.it/s?k=telefonia')  # URL di ricerca
    filtered_products = [product for product in products if query.lower() in product['name'].lower()]
    
    print("Prodotti filtrati:", filtered_products)  # Aggiungi debug per vedere i prodotti filtrati
    return render_template('index.html', products=filtered_products)

if __name__ == '__main__':
    app.run(debug=True)
