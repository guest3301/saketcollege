import hashlib
import re
from concurrent.futures import ThreadPoolExecutor
import threading

# Function to remove multiple new lines
def remove_multiple_newlines(text):
    return re.sub(r'\n+', '\n', text)

# Function to create a hash of the content
def hash_content(content):
    return hashlib.md5(content.encode()).hexdigest()

# Function to process a single URL and its content
def process_url_content(url, content, content_dict, nocontent_urls, lock):
    try:
        if content:
            content = '\n'.join(content)
            content = remove_multiple_newlines(content)
            content_hash = hash_content(content)
            with lock:
                if content_hash not in content_dict:
                    content_dict[content_hash] = content
        else:
            with lock:
                nocontent_urls.append(url)
    except Exception as e:
        print(f"Error processing {url}: {e}")

# Function to process the content with multithreading
def process_content(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        content_dict = {}
        nocontent_urls = []
        current_url = None
        current_content = []
        lock = threading.Lock()

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = []

            for line in lines:
                line = line.strip()
                if line.startswith('http'):
                    if current_url:
                        futures.append(executor.submit(process_url_content, current_url, current_content, content_dict, nocontent_urls, lock))
                        current_content = []
                    current_url = line
                    current_content.append(line)  # Add URL to content
                else:
                    current_content.append(line)

            # Process the last URL
            if current_url:
                futures.append(executor.submit(process_url_content, current_url, current_content, content_dict, nocontent_urls, lock))

            # Wait for all threads to complete
            for future in futures:
                future.result()

        # Write the unique content back to the file
        with open(file_path, 'w') as file:
            for content in content_dict.values():
                file.write(content + '\n\n')
            for line in lines:  # Write all URLs back to the file
                if line.startswith('http'):
                    file.write(line + '\n')

        # Write the URLs with no content to nocontent.txt
        with open('nocontent.txt', 'w') as file:
            for url in nocontent_urls:
                file.write(url + '\n')
        print(nocontent_urls)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Example usage
process_content('/workspaces/saket/extracted_text/content.txt')

