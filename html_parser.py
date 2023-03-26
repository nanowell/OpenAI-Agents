import argparse
import urllib.request
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.errors = []

    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_error(self, message):
        self.errors.append(message)

    def parse_html(self, html_string):
        try:
            self.feed(html_string)
        except Exception as e:
            self.errors.append(str(e))

    def parse_url(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                html_string = response.read().decode('utf-8')
                self.parse_html(html_string)
        except Exception as e:
            self.errors.append(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse HTML string from URL.")
    parser.add_argument("--url", help="URL to parse HTML from", required=True)
    args = parser.parse_args()

    url = args.url

    parser = MyHTMLParser()
    parser.parse_url(url)

    if parser.errors:
        print("Errors occurred during parsing:")
        for error in parser.errors:
            print(error)
    else:
        print("Parsing completed successfully.")
