#!/usr/bin/local/python3

import sys
import os
import urllib.request
from urllib.parse import urlparse
from os.path import splitext, basename
from bs4 import BeautifulSoup

def scrape(url, the_page):
    images = []
    img_count = 0
    soup = BeautifulSoup(the_page, 'html.parser')
    for img in soup.find_all('img'):
        if url not in img.get('src'):
            images.append(url + '/'+ img.get('src'))
            img_count += 1
        else:
            images.append(img.get('src'))
            img_count += 1

    if img_count > 0: 
        print(str(img_count) + " found.")
        save(images)
    else:
        print(str(img_count) + " found.")
        sys.exit(0)

def save(images):
    os.mkdir('scraped_images', 0o777,)
    os.chdir('scraped_images')

    try:
        for image in images:
            parsed = urlparse(image)
            filename, file_ext = splitext(basename(parsed.path))
            urllib.request.urlretrieve(image, filename + file_ext)
    except urllib.error.URLError as e:
        print(e.reason())

if __name__ == "__main__":
    try:
        url = input('Introduce the URL to scrape: ')
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            scrape(url, the_page)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read())
