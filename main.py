import json
import re
import time

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

targets = {"Avanti" : "AVANTI - Förthofer Donaulände 8", "Eni" : "eni24 3500 krems", "avanti2" : "AVANTI - 3500 krems"}

class Crawler():
    def __init__(self, targets):
        self.targets = targets
        self.targetUrls = {}

    def search(self):
        try:
            for name, target in self.targets.items():
                results = DDGS().text(
                    f'"benzinpreis blitz" {target}',
                    region="at-de",
                    max_results=1)

                needed = results[0]["href"]
                if needed != '':
                    self.targetUrls[name] = needed
                else:
                    self.search()
        except:
            print("\n-RETRY-\n\n")
            self.search()

    def provideResult(self):
        self.search()
        return self.targetUrls

class Station():
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.prices = {}
        self.selectedResponse = []

    def getResponse(self, url):
        pattern = re.compile(r"^(?P<name>.+?)(?P<price>\d,\d+)\s*€")

        for attempt in range(3):
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            sp = BeautifulSoup(resp.content, "html.parser")
            selectedResponse = sp.find_all("div", class_="preis_gross")
            if selectedResponse:
                for div in selectedResponse:
                    m = pattern.match(div.get_text(strip=True))
                    if m:
                        self.prices[m["name"].strip()] = float(m["price"].replace(",", "."))
                break
            time.sleep(2)
        else:
            print(f"No prices found for {self.name}")


    def printResults(self):
        self.getResponse(self.url)
        print(f"{self.name}\n----------")
        for fuel, price in self.prices.items():
            print(f"{fuel}: {price}€")
        print()



newCrawler = Crawler(targets)
found_links = newCrawler.provideResult()


for station, url in found_links.items():
    newStation = Station(url, station)
    newStation.printResults()