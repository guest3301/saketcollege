import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def fetch_images_from_site(url, download_folder, visited=None):
    if visited is None:
        visited = set()
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    img_tags = soup.find_all('img')
    
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    for img in img_tags:
        img_url = img.get('src')
        if not img_url:
            continue
        
        img_url = urljoin(url, img_url)
        
        img_filename = os.path.join(download_folder, os.path.basename(img_url))
        
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            with open(img_filename, 'wb') as f:
                f.write(img_response.content)
            print(f"Downloaded {img_filename}")
        else:
            print(f"Failed to download {img_url}")
    
    visited.add(url)
    
    for link in soup.find_all('a', href=True):
        link_url = urljoin(url, link['href'])
        if urlparse(link_url).netloc == urlparse(url).netloc and link_url not in visited:
            fetch_images_from_site(link_url, download_folder, visited)

fetch_images_from_site('https://saketcollege.edu.in', 'downloaded_images')