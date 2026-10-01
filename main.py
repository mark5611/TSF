import json
import re
import time

import requests
from bs4 import BeautifulSoup

found_links = {}
with open("./links.txt", "r") as f:
    data = f.readlines()
    for line in data:
        splitLine = line.strip().split(" ")
        found_links[splitLine[0]] = splitLine[1]

with open("stationPricePairs.jsonl", "w") as f:
    f.write("")

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

    def writeResults(self):
        with open("stationPricePairs.jsonl", "a", encoding="utf-8") as f:
            json.dump({self.name: self.prices}, f, ensure_ascii=False)
            f.write("\n")


for station, url in found_links.items():
    newStation = Station(url, station)
    newStation.printResults()
    newStation.writeResults()