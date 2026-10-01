import requests
from bs4 import BeautifulSoup

resp = requests.get("https://www.benzinpreis-blitz.de/avanti--krems-an-der-donau-f%C3%B6rthofer-donaul%C3%A4nde-8-krems-an-der-donau-foerthofer-donaul%C3%A4nde-8-18419/")

sp = BeautifulSoup(resp.content, 'html.parser')
lf = sp.find_all("span", class_="preis_part1")

print(lf[1])