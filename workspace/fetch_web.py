import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

def extract_text(url, base_folder, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

    if 'text/html' not in response.headers.get('Content-Type', ''):
        print(f"Skipping non-HTML content: {url}")
        return None

    parsed_url = urlparse(url)
    file_path = parsed_url.path.lstrip('/')
    if not file_path or file_path.endswith('/'):
        file_path = file_path + "index.txt"
    local_file = os.path.join(base_folder, file_path)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    text_content = f"{url}\n"

    for paragraph in soup.find_all('p'):
        text_content += f"{paragraph.get_text().replace('\n', ' ')}\n"

    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(text_content + '\n')
    
    print(f"Extracted text: {url} -> {output_file}")
    return local_file

def process_html(html_file, base_url, base_folder, output_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading HTML file {html_file}: {e}")
        return

    soup = BeautifulSoup(content, 'html.parser')

    resources = {
        'a': 'href'
    }

    for tag, attr in resources.items():
        for element in soup.find_all(tag):
            resource_link = element.get(attr)
            if not resource_link or resource_link.startswith('data:'):
                continue
            full_resource_url = urljoin(base_url, resource_link)
            extract_text(full_resource_url, base_folder, output_file)

    print(f"Processed HTML: {html_file}")

def main(url):
    base_folder = "extracted_text"
    os.makedirs(base_folder, exist_ok=True)
    output_file = os.path.join(base_folder, "content.txt")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching the main URL: {e}")
        sys.exit(1)
    
    if 'text/html' not in response.headers.get('Content-Type', ''):
        print(f"Skipping non-HTML content: {url}")
        sys.exit(1)
    
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{url}\n")
        for paragraph in soup.find_all('p'):
            f.write(f"{paragraph.get_text().replace('\n', ' ')}\n")
        f.write('\n')
    
    process_html(output_file, url, base_folder, output_file)
    
    print(f"\nText extracted successfully at: {output_file}")

    links = [urljoin(url, link['href']) for link in soup.find_all('a', href=True)]
    
    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(lambda link: extract_text(link, base_folder, output_file), links)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fetch_web.py <URL>")
        sys.exit(1)
    main(sys.argv[1])