import re
import os
import sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


class ProxyGrabber:
    """Parent class for grabbing proxies from websites"""

    def __init__(self):
        self.dirpath = "proxies"
        self.proxy_list = []

        if not os.path.exists(self.dirpath):
            os.mkdir(self.dirpath)

    def main(self):
        print("\n\n\t[ Select Proxy Type ]\n")
        print("  1) HTTP/HTTPS")
        print("  2) Socks 4")
        print("  3) Socks 5")

        choice = int(input("\nSelect : "))

        if choice == 1:
            self.http()
            print("\nHTTP/HTTPS Proxies have been updated.")
            input("Press Enter to Continue...")
            sys.exit()

        elif choice == 2:
            self.socks4()
            print("Socks 4 Proxies have been updated.")
            input("Press Enter to Continue...")
            sys.exit()

        elif choice == 3:
            self.socks5()
            print("Socks 5 Proxies have been updated.")
            input("Press Enter to Continue...")
            sys.exit()

    def http(self):
        """Grab HTTP and HTTPS proxies"""
        print("\n  HTTP/HTTPS Proxy Grabber")
        print("  =========================\n")

        http_url = "https://free-proxy-list.net/"
        https_url = "https://www.proxy-list.download/api/v1/get?type=https"

        self.get_proxy(http_url, "http")
        self.get_proxy(https_url, "https")

    def socks4(self):
        """Grab SOCKS4 proxies"""
        print("\n  Socks 4 Proxy Grabber")
        print("  ======================\n")

        url = "https://www.socks-proxy.net/"

        data = urlopen(url).read().decode("utf-8")
        matches = re.findall(r"<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+?)</td>", data)

        for match in matches:
            ip = match[0]
            port = match[1]
            self.append_proxy(ip, port, "Socks4", "socks4")

    def socks5(self):
        """Grab SOCKS5 proxies"""
        print("\n  Socks 5 Proxy Grabber")
        print("  ======================\n")

           url = "https://www.socks-proxy.net/"

    data = urlopen(url).read().decode("utf-8")
    matches = re.findall(r"<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+?)</td>", data)

    for match in matches:
        ip = match[0]
        port = match[1]
        self.append_proxy(ip, port, "Socks5", "socks5")

def get_proxy(self, url: str, type: str):
    """Extract IP and port from website and append to proxy list"""
    data = urlopen(url).read().decode("utf-8")
    matches = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+", data)

    for match in matches:
        ip = match.split(":")[0]
        port = match.split(":")[1]
        self.append_proxy(ip, port, type)

def append_proxy(self, ip: str, port: str, type: str, subtype: str="http"):
    """Append proxy to list and save to file"""
    if not os.path.exists(f"{self.dirpath}/{subtype}.txt"):
        open(f"{self.dirpath}/{subtype}.txt", "w").close()

    with open(f"{self.dirpath}/{subtype}.txt", "a") as f:
        f.write(f"{ip}:{port}:{type}\n")

    self.proxy_list.append(f"{ip}:{port}:{type}")
    
    
if __name__ == "__main__":
    proxy_grabber = ProxyGrabber()
    proxy_grabber.main()
