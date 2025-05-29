from flask import Flask
import requests
from bs4 import BeautifulSoup
import schedule
import time
import threading

app = Flask(__name__)

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

def job():
    url = "https://www.amazon.it/s?k=smartphone"
    products = get_product_data(url)
    for product in products:
        print(f"Nome: {product['name']}, Prezzo: {product['price']}")

# Funzione per eseguire job di scraping periodicamente in un thread separato
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/')
def index():
    return "Scraping in corso... Guarda i log!"

if __name__ == '__main__':
    # Start del job di scraping in background
    schedule.every().day.at("09:00").do(job)
    threading.Thread(target=run_schedule, daemon=True).start()

    # Avvio del server Flask
    app.run(host="0.0.0.0", port=5000)
