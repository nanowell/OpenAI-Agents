# This function will rickroll


import re
import requests
from bs4 import BeautifulSoup


def rick_roll(url):
    """
    Returns a rickrolled url.
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    result = soup.find("a", {"class": "btn btn-default btn-lg btn-danger"})
    return "http://www.youtube.com/watch?v={}".format(result["href"])


def main():
    """
    This is the main function.
    """
    url = input()
    print(rick_roll(url))


if __name__ == "__main__":
    main()
