# Proxy Grabber


import urllib.request
import re
import time
import os
import sys
import random
from urllib.error import URLError, HTTPError


class Main:

    def __init__(self):

        self.dirpath = "proxies"
        self.proxy_list = []
        self.proxy_list2 = []

        if not os.path.exists(self.dirpath):
            os.mkdir(self.dirpath)

    def main(self):

        print("\n\n\t[ Select Proxy Type ]\n")
        print("  1) HTTP/HTTPS")
        print("  2) Socks 4")
        print("  3) Socks 5")

        choice = int(input("\nSelect : "))

        if choice == 1:

            self._http()

            print("\nHTTP/HTTPS Proxies have been updated.")
            input("Press Enter to Continue...")

            sys.exit()

        elif choice == 2:

            self._socks4()

            print("Socks 4 Proxies have been updated.")
            input("Press Enter to Continue...")

            sys.exit()

        elif choice == 3:

            self._socks5()

            print("Socks 5 Proxies have been updated.")
            input("Press Enter to Continue...")

            sys.exit()

    def _http(self):

        print("\n  HTTP/HTTPS Proxy Grabber")
        print("  =========================\n")

        http_url = "https://free-proxy-list.net/"
        https_url = "https://www.proxy-list.download/api/v1/get?type=https"

        self._get_proxy(http_url, "http")
        self._get_proxy(https_url, "https")

    def _socks4(self):

        print("\n  Socks 4 Proxy Grabber")
        print("  ======================\n")

        url = "https://www.socks-proxy.net/"

        data = urllib.request.urlopen(url).read().decode("utf-8")
        matches = re.findall(r"<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+?)</td>", data)

        for match in matches:

            ip = match[0]
            port = match[1]

            self._append_proxy(ip, port, "Socks4", "socks4")

    def _socks5(self):

        print("\n  Socks 5 Proxy Grabber")
        print("  ======================\n")

        url = "https://www.socks-proxy.net/"

        data = urllib.request.urlopen(url).read().decode("utf-8")
        matches = re.findall(r"<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+?)</td>", data)

        for match in matches:

            ip = match[0]
            port = match[1]

            self._append_proxy(ip, port, "Socks5", "socks5")

    def _get_proxy(self, url: str, type: str):

        data = urllib.request.urlopen(url).read().decode("utf-8")
        matches = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+", data)

        for match in matches:

            ip = match.split(":")[0]
            port = match.split(":")[1]

            self._append_proxy(ip, port, type)

    def _append_proxy(self, ip: str, port: str, type: str, subtype: str="http"):

        if not os.path.exists(f"{self.dirpath}/{subtype}.txt"):
            open(f"{self.dirpath}/{subtype}.txt", "w").close()

        with open(f"{self.dirpath}/{subtype}.txt", "r") as f:
            proxylist = f.read()

        if ip in proxylist and subtype == "http":
            return None
        elif ip in proxylist and subtype == "https":
            return None

        with open(f"{self.dirpath}/{subtype}.txt", "a") as f:
            f.write("".join([ip + ":" + port + "\n"]))


if __name__ == "__main__":
    Main().main()