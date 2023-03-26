from bs4 import BeautifulSoup
import requests
import urllib.parse
import urllib.request
import re
import os
import sys
import threading

def get_page_soup(board, page_type, thread_id=None):
    base_url = "http://boards.4chan.org/{}/".format(board)
    if page_type == "main":
        url = base_url
    elif page_type == "thread":
        url = "{}res/{}".format(base_url, thread_id)
    else:
        raise ValueError("Invalid page type: {}".format(page_type))
    response = requests.get(url)
    return BeautifulSoup(response.text, "lxml")

def get_thread_ids(board):
    main_page = get_page_soup(board, "main")
    thread_ids = []
    for link in main_page.find_all("a", class_="replylink"):
        thread_ids.append(link["href"][1:])
    return thread_ids

def get_image_urls(thread_id):
    thread_page = get_page_soup("g", "thread", thread_id)
    base_url = thread_page.find("meta", property="og:url")["content"]
    image_urls = []
    for post in thread_page.find_all("div", class_="postContainer"):
        for link in post.find_all("a"):
            if link.has_attr("href") and link["href"].endswith("jpg"):
                image_urls.append(urllib.parse.urljoin(base_url, link["href"]))
    return image_urls

def download_image(url, filename):
    print ("Downloading {} to {}".format(url, filename))
    urllib.request.urlretrieve(url, filename)

def download_image_in_thread(url, filename):
    def download():
        download_image(url, filename)
    thread = threading.Thread(target=download)
    thread.start()

def download_images(board):
    thread_ids = get_thread_ids(board)
    threads = []
    for thread_id in thread_ids:
        image_urls = get_image_urls(thread_id)
        for url in image_urls:
            thread = threading.Thread(target=download_image, args=(url, url.split("/")[-1]))
            threads.append(thread)
            thread.start()
    for thread in threads:
        thread.join()

def main():
    if len(sys.argv) < 2:
        print ("Usage: python 4chan.py <board> [<thread_id>]")
        sys.exit(1)
    board = sys.argv[1]
    if len(sys.argv) > 2:
        thread_id = sys.argv[2]
        image_urls = get_image_urls(thread_id)
        for url in image_urls:
            download_image(url, url.split("/")[-1])
    else:
        download_images(board)
