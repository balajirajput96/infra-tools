import requests
from bs4 import BeautifulSoup
import os

def get_latest_ubuntu_iso_url():
    # Direct link to the latest LTS release page
    url = "https://releases.ubuntu.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the latest LTS version folder (e.g., "26.04/")
    lts_version = None
    for link in soup.find_all('a', href=True):
        if link['href'].endswith('/') and link.text.strip().replace('.', '').isdigit():
            lts_version = link['href']
            # We want the latest, so we keep going or pick the first one if sorted
    
    if not lts_version:
        # Fallback to a known pattern if scraping fails
        lts_version = "26.04/"
        
    release_url = f"https://releases.ubuntu.com/{lts_version}"
    response = requests.get(release_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for link in soup.find_all('a', href=True):
        if link['href'].endswith('-desktop-amd64.iso'):
            return release_url + link['href']
    return None

def download_file(url, filename):
    print(f"Starting download from: {url}")
    # We will only download a small part to demonstrate, as the full ISO is ~4GB
    # and might exceed sandbox limits or take too long.
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    downloaded = 0
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024*1024): # 1MB chunks
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                print(f"Downloaded: {downloaded / (1024*1024):.2f} MB / {total_size / (1024*1024):.2f} MB", end='\r')
                if downloaded > 50 * 1024 * 1024: # Stop after 50MB for demo purposes
                    print("\nDownload stopped at 50MB for demonstration.")
                    break

if __name__ == "__main__":
    iso_url = get_latest_ubuntu_iso_url()
    if iso_url:
        filename = iso_url.split('/')[-1]
        download_file(iso_url, filename)
    else:
        print("Could not find the latest Ubuntu ISO URL.")
