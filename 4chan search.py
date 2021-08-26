
from bs4 import BeautifulSoup
import requests
import urllib
import re
import os
import sys

def get_soup(url):
    return BeautifulSoup(requests.get(url).text, "lxml")

def get_main_page(board):
    return get_soup("http://boards.4chan.org/{}/".format(board))

def get_thread_page(board, thread_id):
    return get_soup("http://boards.4chan.org/{}/res/{}".format(board, thread_id))

def get_thread_ids(board):
    main_page = get_main_page(board)
    thread_ids = []
    for link in main_page.find_all("a", class_="replylink"):
        thread_ids.append(link["href"][1:])
    return thread_ids

def get_image_urls(thread_id):
    thread_page = get_thread_page("g", thread_id)
    image_urls = []
    for post in thread_page.find_all("div", class_="postContainer"):
        for link in post.find_all("a"):
            if link.has_attr("href") and link["href"].endswith("jpg"):
                image_urls.append(link["href"])
    return image_urls

def download_image(url, filename):
    print ("Downloading {} to {}".format(url, filename))
    urllib.urlretrieve(url, filename)

def download_images(board):
    thread_ids = get_thread_ids(board)
    for thread_id in thread_ids:
        image_urls = get_image_urls(thread_id)
        for url in image_urls:
            download_image(url, url.split("/")[-1])

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

if __name__ == "__main__":
    main()