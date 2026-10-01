import re
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
            print("\n\n-RETRY-\n\n")
            self.search()

    def provideResult(self):
        self.search()
        return self.targetUrls

class Station():
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.e10 = "N/A"
        self.diesel = "N/A"
        self.selectedResponse = []

    def getResponse(self, url):
        while self.selectedResponse == []:
            resp = requests.get(url)
            sp = BeautifulSoup(resp.content, 'html.parser')
            self.selectedResponse = sp.find_all("div", class_="preis_gross")
            print(self.selectedResponse)

    def parseE10(self):
        self.e10 = str(self.selectedResponse[1]).split(">")[1].split("<")[0]

    def parseDiesel(self):
        self.diesel = str(self.selectedResponse[0]).split(">")[1].split("<")[0]

    def printResults(self):
        self.getResponse(self.url)
        self.parseE10()
        self.parseDiesel()
        print(f"{self.name}\n----------\nE10: €{self.e10}\nDiesel: €{self.diesel}\n")


newCrawler = Crawler(targets)
found_links = newCrawler.provideResult()


for station, url in found_links.items():
    newStation = Station(url, station)
    newStation.printResults()