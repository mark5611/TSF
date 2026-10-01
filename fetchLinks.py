from ddgs import DDGS

targets = {"Avanti" : "AVANTI - Förthofer Donaulände 8", "Eni" : "eni24 3500 krems", "AVANTI2" : "AVANTI - 3500 krems"}

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
        with open("./links.txt", "w") as f:
            for name, url in self.targetUrls.items():
                f.write(f"{name} {url}\n")

newCrawler = Crawler(targets)
newCrawler.provideResult()