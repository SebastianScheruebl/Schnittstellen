import requests
from datetime import date, timedelta
import xml.etree.ElementTree as ET


# URL der OAI-Schnittstelle
url = "https://opus4.kobv.de/opus4-th-wildau/oai"


def lese_url(url, parameter):
    #Datei zum beschreiben
    with open("opus_daten.txt", "w", encoding="utf-8") as datei:

        while True:

            response = requests.get(url, params=parameter)

            if response.status_code == 200:

                print("\nURL-Zugriff erfolgreich")
                print(response.url)

                tree = ET.ElementTree(ET.fromstring(response.content))
                root = tree.getroot()

                i = 1

                for record in root.iter():

                    if record.tag.endswith("record"):

                        print("\nDatensatz ", i)
                        datei.write("\nDatensatz " + str(i) + "\n")

                        for element in record.iter():

                            if element.tag.endswith("title"):
                                print("Titel:", element.text)
                                datei.write("Titel: " + str(element.text) + "\n")

                            if element.tag.endswith("creator"):
                                print("Creator:", element.text)
                                datei.write("Creator: " + str(element.text) + "\n")

                        i += 1

                # resumptionToken suchen
                token = None

                for element in root.iter():
                    if element.tag.endswith("resumptionToken"):
                        token = element.text

                if not token:
                    break

                parameter = {
                    "verb": "ListRecords",
                    "resumptionToken": token
                }

            else:
                print("Fehler beim URL-Aufruf:", response.status_code)
                break
#Zeitraums-Auswahl
print("Welchen Zeitraum möchtest du abrufen?")
print("1 - Letzte Woche")
print("2 - Letzter Monat")
print("3 - Eigener Zeitraum")

auswahl = input("Bitte auswählen (1, 2 oder 3): ")


# Letzte Woche
if auswahl == "1":

    # Heutiges Datum
    heute = date.today()

    # Enddatum heute
    enddatum = heute

    # Startdatum ist vor 7 Tagen
    startdatum = heute - timedelta(days=7)

    print("Letzte Woche ausgewählt")


# Letzter Monat (30 Tage)
elif auswahl == "2":

    # Heutiges Datum
    heute = date.today()

    # Enddatum heute
    enddatum = heute

    # Startdatum 30 Tage vor heute
    startdatum = heute - timedelta(days=30)

    print("Letzter Monat ausgewählt")


# Eigener Zeitraum
elif auswahl == "3":

    # Startdatum abfragen
    print("\nStartdatum eingeben:")

    start_jahr = input("Jahr (4 Stellen): ")
    start_monat = input("Monat (2 Stellen): ")
    start_tag = input("Tag (2 Stellen): ")

    # Enddatum abfragen
    print("\nEnddatum eingeben:")

    end_jahr = input("Jahr (4 Stellen): ")
    end_monat = input("Monat (2 Stellen): ")
    end_tag = input("Tag (2 Stellen): ")

    # EIngabeformat checken
    if (len(start_jahr) == 4 and start_jahr.isdigit() and
        len(start_monat) == 2 and start_monat.isdigit() and
        len(start_tag) == 2 and start_tag.isdigit() and
        len(end_jahr) == 4 and end_jahr.isdigit() and
        len(end_monat) == 2 and end_monat.isdigit() and
        len(end_tag) == 2 and end_tag.isdigit()):

        # Startdatum zusammensetzen
        startdatum = start_jahr + "-" + start_monat + "-" + start_tag

        # Enddatum zusammensetzen
        enddatum = end_jahr + "-" + end_monat + "-" + end_tag

        print("\nStartdatum:", startdatum)
        print("Enddatum:", enddatum)

    # Falsche Datumseingabe
    else:
        print("Fehler: Bitte Jahr mit 4 Stellen sowie Monat und Tag mit 2 Stellen eingeben.")
        exit()


# Ungültige Auswahl
else:

    print("Ungültige Auswahl. Bitte 1, 2 oder 3 eingeben.")
    exit()


# Parameter für die OAI-Anfrage
parameter = {
    "verb": "ListRecords",
    "metadataPrefix": "oai_dc",
    "from": startdatum,
    "until": enddatum
}
lese_url(url, parameter)