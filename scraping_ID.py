import requests
from bs4 import BeautifulSoup
import re
import json
import datetime

def get_articles_kompas(url=" "):
    res = requests.get(url)
    
    if res.status_code == 200: # Cek apakah bisa diakses
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Ambil metadata
        title = soup.find("meta", property="og:title")
        description = soup.find("meta", property="og:description")
        url = soup.find("meta", property="og:url")
        published_date = soup.find("meta", property="article:published_time")

        # Mencari class/div untuk isi berita
        articles = soup.find(class_="read__content")
        articles.find(class_="clearfix")
        contents = articles.find_all("p")
        
        items = list()
        for item in contents:
            items.append(item.text)

        # Filter konten berita
        r = re.compile(".*Baca juga:")
        filter_items = list(filter(r.match, items))
        filter_contents = list(set(items) - set(filter_items))

        # Gabung elemen-elemen di list
        filter_contents = " ".join(filter_contents)

        # Simpan data dalam dictionary
        data = dict()
        data = {'title': title["content"],
                'description': description["content"],
                'url': url["content"],
                'published_date': published_date["content"],
                'content': filter_contents
                }
        return data
    
    else:
        return "Artikel berita tidak dapat diakses."

def get_articles_detik(url=" "):
    res = requests.get(url)
    
    if res.status_code == 200: # Cek apakah bisa diakses
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Ambil metadata
        title = soup.find("meta", property="og:title")
        description = soup.find("meta", property="og:description")
        url = soup.find("meta", property="og:url")
        published_date = soup.find("meta", attrs={'name': 'pubdate'})

        # Mencari class/div untuk isi berita
        articles = soup.find(class_="detail__body-text")
        contents = articles.find_all("p")
        
        items = list()
        for item in contents:
            items.append(item.text)

        # Filter konten berita
        r = re.compile(".*Baca juga:")
        filter_items = list(filter(r.match, items))
        filter_contents = list(set(items) - set(filter_items))

        # Gabung elemen-elemen di list
        filter_contents = " ".join(filter_contents)

        # Simpan data dalam dictionary
        data = dict()
        data = {'title': title["content"],
                'description': description["content"],
                'url': url["content"],
                'published_date': published_date["content"],
                'content': filter_contents
                }
        return data
    
    else:
        return "Artikel berita tidak dapat diakses."

def save_dump_file(dataset = list(), name='unknown'):
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%Y_%H:%M:%S")
    filename = 'dump_files/dataset_dump_'+ name +'_'+ time +'.json'

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
    except:
        print("Error occured.")
