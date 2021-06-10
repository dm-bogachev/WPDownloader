import sys, os
from bs4 import BeautifulSoup
import requests

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

BASIC_SITE = 'https://wallpaperscraft.ru' # DO NOT CHANGE !!!!!!!!!!!

CATALOG = '/catalog/vector/1920x1080' #'/catalog/nature/1920x1080'
NUMBER_OF_PAGES = 10
DIRNAME = 'vector'

print("Welcome to WPDownloader")
print("This program allows you to bulk download wallpapers from https://wallpaperscraft.ru/")
print("For now, all configuration is inside the file without any user prompt, but later it will be changed")
print("\n\nProgram parameters:")
print("CATALOG: Choose any catalog from site and copy part of it's url like in example")
print("NUMBER_OF_PAGES: How many pages you want to donwload (one page contains 15 wallpapers)")
print("DIRNAME: Directory name for saving files\n\n")

ensure_dir(DIRNAME)
pages = []
pages.append(get_page_text(BASIC_SITE + CATALOG))

for i in range(NUMBER_OF_PAGES-1):
    postfix = 'page' + str(i+2)
    pages.append(get_page_text(BASIC_SITE + CATALOG +'/' + postfix))

wallpapers_count = NUMBER_OF_PAGES*15
wallpapers_downloaded = 1

for page in pages:
    page_soup = BeautifulSoup(page, "html.parser")
    for wp_item in page_soup.findAll('a', class_='wallpapers__link', href = True):
        wp_page = get_page_text(BASIC_SITE + wp_item['href'])
        item_soup = BeautifulSoup(wp_page, "html.parser")
        download_url = item_soup.find('a', class_='gui-button gui-button_full-height', href = True)['href']
        head, tail = os.path.split(download_url)
        download_image(download_url, DIRNAME + '/' + tail)
        print(f"Downloaded {wallpapers_downloaded} out of {wallpapers_count} wallpapers ({100*wallpapers_downloaded/wallpapers_count:5.2f} %)")
        wallpapers_downloaded = wallpapers_downloaded + 1
        pass
