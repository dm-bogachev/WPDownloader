import sys, os
from bs4 import BeautifulSoup
import requests
import time

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def get_page_text(url):
    r = requests.get(url)
    r.encoding = 'cp1251'
    return r.text

def download_image(url, path):
    response = requests.get(url, path)
    with open(path, 'wb') as f:
        f.write(response.content)

def prepare_to_download():
    items_len = 0
    pages_count = 1
    print('Preparing for download:\n')

    pages = []
    pages.append(get_page_text(BASIC_SITE + CATALOG))
    page_soup = BeautifulSoup(pages[pages_count-1], "html.parser")
    items_count = len(page_soup.findAll('a', class_='wallpapers__link'))
    items_len = items_len + items_count
    print(f"Prepared {pages_count} out of {NUMBER_OF_PAGES} pages ({100*pages_count/NUMBER_OF_PAGES:5.2f} %) : {items_count} found on {BASIC_SITE + CATALOG}")
    
    pages_count = 2

    for i in range(NUMBER_OF_PAGES-1):
        postfix = 'page' + str(i+2)
        pages_url = BASIC_SITE + CATALOG +'/' + postfix
        items_count = len(page_soup.findAll('a', class_='wallpapers__link', href = True))
        items_len = items_len + items_count
        print(f"Prepared {pages_count} out of {NUMBER_OF_PAGES} pages ({100*pages_count/NUMBER_OF_PAGES:5.2f} %) : {items_count} found on {BASIC_SITE + CATALOG}")
        pages_count = pages_count + 1
        pages.append(get_page_text(pages_url))
    return pages, items_len

def download(pages, items_len):
    wallpapers_count = items_len
    wallpapers_downloaded = 1
    print('\nDownloading:\n')
    for page in pages:
        page_soup = BeautifulSoup(page, "html.parser")
        page_data = page_soup.findAll('a', class_='wallpapers__link')
        print(f'Downloading {len(page_data)} images:')
        for wp_item in page_soup.findAll('a', class_='wallpapers__link', href = True):
            wp_page = get_page_text(BASIC_SITE + wp_item['href'])
            item_soup = BeautifulSoup(wp_page, "html.parser")
            download_url = item_soup.find('a', class_='gui-button gui-button_full-height', href = True)['href']
            head, tail = os.path.split(download_url)
            download_image(download_url, DIRNAME + '/' + tail)
            print(f"Downloaded {wallpapers_downloaded} out of {wallpapers_count} wallpapers ({100*wallpapers_downloaded/wallpapers_count:5.2f} %) : {tail}")
            wallpapers_downloaded = wallpapers_downloaded + 1

# Global variables
BASIC_SITE = 'https://wallpaperscraft.ru' # DO NOT CHANGE !!!!!!!!!!!

CATALOG = '/catalog/city/1920x1080' 
#CATALOG = '/catalog/nature/1920x1080' 
#CATALOG = '/catalog/vector/1920x1080' 
#CATALOG = '/catalog/art/1920x1080' 
#CATALOG = '/catalog/flowers/1920x1080'
NUMBER_OF_PAGES = 300
DIRNAME = 'all_cities'

# end Global variables

ensure_dir(DIRNAME)
start_time = time.time()
pages, items_len = prepare_to_download()
download(pages, items_len)
print(f'Finished in {time.time() - start_time}')
input("Press Enter to close...")

