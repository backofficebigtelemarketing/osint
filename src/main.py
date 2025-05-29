import requests
from bs4 import BeautifulSoup
import schedule
import time

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

schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
