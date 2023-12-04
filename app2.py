import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import time
from datetime import datetime
from pymongo import MongoClient
import logging
from collections import Counter
import matplotlib.pyplot as plt

# MongoDB'ye bağlanmak için bir client oluşturuyoruz.
client = MongoClient('mongodb://localhost:27017')
db = client['ErmanKonyar']  
news_collection = db['news']  
word_freq_collection = db['word_frequency']
stats_collection = db['stats']

# Log kayıtları için ayarlar
logging.basicConfig(filename='logs/logs.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

lock = Lock()
text_data = []

# İstatistikler için değişkenler
total_requests, successful_requests, failed_requests = 0, 0, 0
start_time = time.time()

def format_iso_date(date_str):
    # Tarih formatını ISO standardına dönüştürme
    parts = date_str.split('-')
    parts[1], parts[2] = parts[1].zfill(2), parts[2].zfill(2)
    return '-'.join(parts)

def fetch_data(url, max_retries=5):
    # Veri çekme işlemi
    global total_requests, successful_requests, failed_requests
    headers = {"User-Agent": "Mozilla/5.0"}
    for _ in range(max_retries):
        total_requests += 1
        try:
            response = requests.get(url, headers=headers, timeout=100)
            if response.status_code == 200:
                successful_requests += 1
                parse_and_save(response, url)
            break
        except requests.exceptions.RequestException as e:
            failed_requests += 1
            logging.error(f"URL: {url} - Hata: {e}")
            time.sleep(1)

def parse_and_save(response, url):
    # Yanıtı ayrıştırıp veritabanına kaydetme
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    header, summary = soup.find('h1', class_='single_title').text.strip(), soup.find('h2', class_='single_excerpt').p.text.strip()
    img_urls = [img['src'] for img in soup.find_all('img')]
    date_span = soup.find_all('span', class_='tarih')
    publish_date, update_date = format_iso_date(date_span[0].time['datetime']), format_iso_date(date_span[1].time['datetime'])
    content = ' '.join(p.text.strip() for p in soup.select('div.yazi_icerik p'))
    news_item = {
        'url': url, 'header': header, 'summary': summary, 
        'content': content, 'img_url_list': img_urls,
        'publish_date': publish_date, 'update_date': update_date
    }
    with lock:
        news_collection.insert_one(news_item)
        text_data.append(content)

def analyze_text_data():
    # Metin verilerini analiz etme ve grafik oluşturma
    words = ' '.join(text_data).split()
    most_common = Counter(words).most_common(10)
    word_freq_collection.insert_one({"words": most_common})
    plt.bar(*zip(*most_common))
    plt.xlabel('Kelimeler'), plt.ylabel('Frekans'), plt.title('En Çok Kullanılan 10 Kelime')
    plt.savefig('word_frequency.png')

# Haberleri çekmek için url oluşturma
base_url = "https://turkishnetworktimes.com/kategori/gundem/page/"
article_urls = [f"{base_url}{page}/" for page in range(1, 51)]

# Çoklu iş parçacığı thread yönetimi
with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = {executor.submit(fetch_data, url): url for url in article_urls}
    for future in as_completed(future_to_url):
        try:
            future.result()
        except Exception as exc:
            logging.error('%r generated an exception: %s' % (future_to_url[future], exc))

# Veri analizi ve performans verilerinin kaydedilmesi
analyze_text_data()
end_time = time.time()
performance_data = {
    "total_requests": total_requests,
    "successful_requests": successful_requests,
    "failed_requests": failed_requests,
    "total_time": end_time - start_time,
    "data_collection_date": datetime.now()
}
stats_collection.insert_one(performance_data)

# Gruplanmış verileri yazdırmak için fonksiyon 
# def print_grouped_data():
#     grouped_data = news_collection.aggregate([
#         {"$group": {"_id": "$update_date", "count": {"$sum": 1}}}
#     ])
#     for data in grouped_data:
#         print(f"Tarih: {data['_id']}, Haber Sayısı: {data['count']}")
