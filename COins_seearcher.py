import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs

url = "https://portal.kobv.de/KobvIndexRecord/almahu_9949068938002882?sid=38840"
response = requests.get(url)

url_inhalt = response.text

if response.status_code == 200:
 soup = BeautifulSoup(url_inhalt, "html.parser")
 found_class = soup.find_all("span", class_="Z3988")
 if not found_class:
    print("Kein COins enthalten")
 else:
    for i in found_class:
        #print(i.get("title"))
        
        coins_daten = i.get("title")
        daten = parse_qs(coins_daten)

        #print(daten)
        print("Titel:", daten.get("rft.title"))
        print("Autor:", daten.get("rft.creator"))
        print("ISSN:", daten.get("rft.issn"))
        print("Seiten:", daten.get("rft.pages"))
else:
    print("Fehler beim URL-Aufurf")


