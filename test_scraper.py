import requests
from bs4 import BeautifulSoup

# De toernooi-URL
url = "https://dartcounter.app/tournaments/european-league-day-2-2piSdd"

# Haal de HTML op
response = requests.get(url)
print(f"Statuscode: {response.status_code}")

# Print een deel van de HTML (alleen als het succesvol is)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Toon de eerste <table> (of de eerste 500 tekens)
    table = soup.find("table")
    if table:
        print("✅ Eerste tabel gevonden!")
        print(table.prettify()[:1000])  # Eerste 1000 tekens van de tabel
    else:
        print("⚠️ Geen tabel gevonden in de HTML.")
else:
    print("❌ Pagina niet bereikbaar of geblokkeerd.")
