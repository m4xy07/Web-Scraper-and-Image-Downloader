import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from urllib.parse import urljoin
import time

def scrape_and_store(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image URLs on the page
    image_urls = [urljoin(url, img['src']) for img in soup.find_all('img')]

    # Find all link URLs on the page
    link_urls = [urljoin(url, link['href']) for link in soup.find_all('a', href=True)]

    # Create a file to store the URLs
    with open('index.txt', 'w') as f:
        f.write('Image URLs:\n')
        for url in image_urls:
            f.write(f'{url}\n')
        f.write('\nLink URLs:\n')
        for url in link_urls:
            f.write(f'{url}\n')

    # Display a message to the user
    messagebox.showinfo('Scrape Complete', 'The URLs have been stored in "index.txt".')

def scrape_and_download(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image URLs on the page
    image_urls = [urljoin(url, img['src']) for img in soup.find_all('img')]

    # Create a directory to save the images
    if not os.path.exists('images'):
        os.makedirs('images')

    # Download each image and save it to the directory
    for i, img_url in enumerate(image_urls):
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            filename = f'images/image_{i}.jpg'
            with open(filename, 'wb') as f:
                for chunk in response:
                    f.write(chunk)
        else:
            print(f'Error downloading image {img_url}: {response.status_code}')
            time.sleep(1)

    # Write the image URLs to the file
    with open('index.txt', 'a') as f:
        f.write('Image URLs:\n')
        for url in image_urls:
            f.write(f'{url}\n')

    # Display a message to the user
    messagebox.showinfo('Scrape Complete', 'All images have been downloaded to the "images" directory and the URLs have been stored in "index.txt".')

def scrape_button_clicked():
    # Get the URL entered by the user
    url = url_entry.get()

    # Call the scrape_and_store function with the URL
    scrape_and_store(url)

def download_button_clicked():
    # Get the URL entered by the user
    url = url_entry.get()

    # Call the scrape_and_download function with the URL
    scrape_and_download(url)

# Create the GUI
root = tk.Tk()
root.title('Web Scraper')

# Create a label and entry for the URL input
url_label = tk.Label(root, text='Enter URL:')
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()

# Create the "Scrape!" button
scrape_button = tk.Button(root, text='Scrape!', command=scrape_button_clicked)
scrape_button.pack()

# Create the "Scrape & Download" button
download_button = tk.Button(root, text='Scrape & Download', command=download_button_clicked)
download_button.pack()

# Run the GUI
root.mainloop()