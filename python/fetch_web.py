import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Function to download any file from URL and save it locally
def download_file(url, base_folder):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

    parsed_url = urlparse(url)
    # Remove starting "/" and if empty, use a default name
    file_path = parsed_url.path.lstrip('/')
    if not file_path or file_path.endswith('/'):
        file_path = file_path + "index.html"
    local_file = os.path.join(base_folder, file_path)
    
    # Create directory if not exists
    os.makedirs(os.path.dirname(local_file), exist_ok=True)
    
    with open(local_file, 'wb') as f:
        # Add the URL as a comment at the top of the file
        if local_file.endswith('.html'):
            f.write(f"<!-- Source: {url} -->\n".encode('utf-8'))
        elif local_file.endswith('.css'):
            f.write(f"/* Source: {url} */\n".encode('utf-8'))
        elif local_file.endswith('.js'):
            f.write(f"// Source: {url}\n".encode('utf-8'))
        f.write(response.content)
    
    print(f"Downloaded: {url} -> {local_file}")
    return local_file

# Function to process CSS files and download assets referenced inside (like background images)
def process_css(css_file, base_url, base_folder):
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading CSS file {css_file}: {e}")
        return

    # Regex to find url(...) patterns
    pattern = re.compile(r'url\(([^)]+)\)')
    matches = pattern.findall(content)
    for match in matches:
        # Clean the matched url (remove quotes and spaces)
        asset_url = match.strip(' \'"')
        if asset_url.startswith('data:'):
            continue  # Skip data URIs

        full_asset_url = urljoin(base_url, asset_url)
        local_asset = download_file(full_asset_url, base_folder)
        if local_asset:
            # Calculate relative path from the CSS file's directory
            rel_path = os.path.relpath(local_asset, os.path.dirname(css_file))
            rel_path = rel_path.replace(os.sep, '/')
            # Replace the url reference in CSS file
            content = content.replace(match, f"'{rel_path}'")

    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed CSS: {css_file}")

# Function to process HTML files and download linked resources
def process_html(html_file, base_url, base_folder):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading HTML file {html_file}: {e}")
        return

    soup = BeautifulSoup(content, 'html.parser')

    # Define tags and their attributes to look for static resources
    resources = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
        'a': 'href'
    }

    for tag, attr in resources.items():
        for element in soup.find_all(tag):
            resource_link = element.get(attr)
            if not resource_link or resource_link.startswith('data:'):
                continue
            full_resource_url = urljoin(base_url, resource_link)
            local_file = download_file(full_resource_url, base_folder)
            if local_file:
                # If it's a CSS file, process its internal assets
                if tag == 'link':
                    rel = element.get('rel')
                    if rel and 'stylesheet' in rel:
                        process_css(local_file, base_url, base_folder)
                # Update the element attribute to point to the locally saved file (relative path)
                rel_path = os.path.relpath(local_file, os.path.dirname(html_file))
                element[attr] = rel_path.replace(os.sep, '/')

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f"Processed HTML: {html_file}")


def main(url):
    base_folder = "downloaded_site"
    os.makedirs(base_folder, exist_ok=True)
    
    # Download the main HTML page
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching the main URL: {e}")
        sys.exit(1)
    
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Define tags and their attributes to look for static resources
    resources = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
        'a': 'href'
    }
    
    for tag, attr in resources.items():
        for element in soup.find_all(tag):
            resource_link = element.get(attr)
            if not resource_link or resource_link.startswith('data:'):
                continue
            full_resource_url = urljoin(url, resource_link)
            local_file = download_file(full_resource_url, base_folder)
            if local_file:
                # If it's a CSS file, process its internal assets
                if tag == 'link':
                    rel = element.get('rel')
                    if rel and 'stylesheet' in rel:
                        process_css(local_file, url, base_folder)
                # Update the element attribute to point to the locally saved file (relative path)
                rel_path = os.path.relpath(local_file, base_folder)
                element[attr] = rel_path.replace(os.sep, '/')

    # Save the prettified HTML to index.html inside our base_folder
    output_file = os.path.join(base_folder, "index.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"<!-- Source: {url} -->\n")
        f.write(soup.prettify())
    
    # Process the downloaded HTML file to fetch linked resources
    process_html(output_file, url, base_folder)
    
    print(f"\nPage saved successfully at: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fetch_web.py <URL>")
        sys.exit(1)
    main(sys.argv[1])