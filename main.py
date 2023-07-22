import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_static_files(url, output_folder):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        # Fetch the HTML content
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        return

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all CSS and JS links
    static_links = soup.find_all(["link", "script"], rel=["stylesheet", "javascript"])

    # Download each CSS and JS file
    for link in static_links:
        if file_url := link.get("href") or link.get("src"):
            # Resolve relative URLs to absolute URLs
            file_url = urljoin(url, file_url)

            # Get the file content
            file_response = requests.get(file_url, headers=headers)
            file_response.raise_for_status()

            # Save the file content to a file
            file_name = os.path.basename(file_url)
            output_path = os.path.join(output_folder, file_name)

            with open(output_path, "wb") as f:
                f.write(file_response.content)

            print(f"Downloaded: {file_name}")

if __name__ == "__main__":
    # Replace 'your_url_here' with the URL of the HTML page you want to download CSS and JS files from
    url_to_scrape = "https://www.pertaminadppubabullah.com/"
    output_folder = "static_files"  # Folder where downloaded CSS and JS files will be saved

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    download_static_files(url_to_scrape, output_folder)
