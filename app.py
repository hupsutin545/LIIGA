import os
import json
import requests
import xml.etree.ElementTree as ET
from googleapiclient.discovery import build

# API-avain suoraan koodissa
YOUTUBE_API_KEY = "AIzaSyCzqFkntOh2A7ZaWfaCQPoeMU1V5DFh14k"

try:
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
except Exception as e:
    print(f"Virhe YouTubessa: {e}")
    youtube = None

LIIGA_CHANNEL_ID = "UCGxrUE2U-ncnBf4vDww-gAQ" 

def hae_liigan_viralliset_uutiset():
    """Hakee virallista dataa ja uutisia suoraan Liiga.fi uutisvirrasta"""
    try:
        # Haetaan Liiga.fi:n virallinen uutisvirta (RSS)
        vastaus = requests.get("https://liiga.fi", timeout=10)
        if vastaus.status_code == 200:
            root = ET.fromstring(vastaus.content)
            uutiset = []
            for item in root.findall('.//item')[:3]:  # Otetaan 3 uusinta virallista uutista
                otsikko = item.find('title').text
                kuvaus = item.find('description').text if item.find('description') is not None else ""
                uutiset.append(f"📰 Liiga.fi Uutinen: {otsikko}\n{kuvaus}")
            return "\n\n".join(uutiset)
    except Exception as e:
        print(f"Ei saatu yhteyttä Liiga.fi uutisfeediin: {e}")
    return "Ei ylimääräisiä Liiga.fi uutisia tällä sekunnilla."

def luo_2min_radioselostus(title, kuvaus, liiga_data):
    """Rakentaa YouTuben ja Liiga.fi:n pohjalta täydellisen 2 minuutin puhekäsikirjoituksen"""
    clean_title = title.replace("Ottelukooste:", "").replace("| 5.9.2026", "").strip()
    
    käsikirjoitus = f"""🎙️ [ÄÄNITYSVALMIS KÄSIKIRJOITUS - KESTO: 2 MINUUTTIA]
(Lue teksti dynaamisella, kovalla tempolla ja eläydy peliin!)

"Noniin kiekkofanit, ottakaa tukeva asento, sillä nyt perataan Liigan tuoreimmat ja kuumimmat pelitapahtumat suoraan kaukalosta! Syynissä on ottelu {clean_title}, ja tästä kamppailusta ei draamaa puuttunut! 

Ottelun intensiteetti oli aivan tapissa heti avauskiekosta lähtien, ja molemmat joukkueet laittoivat pystyyn sellaisen taklaus- ja vauhtirallin, että heikompaa hirvitti. Kun katsotaan virallisia pelitapahtumia, kentällä nähtiin huikeita taktiikan muutoksia. Toisessa erässä peli repesi liitoksistaan, kun hyökkäyspeli alkoi rullata kunnolla ja maalivahdit joutuivat venymään aivan uskomattomiin paraatipelastuksiin pitääkseen lukemat tasaisina!

Ja muistetaan myös pelin kuumat tunteet – Liigassa pelataan tällä hetkellä niin kovaa, että hanskat tippuvat ja kurinpito joutuu jakamaan pelikieltoja kovalla kädellä. Jokainen taklaus syynätään tarkasti, ja se näkyy myös joukkueiden kokoonpanoissa seuraavilla kierroksilla!

Virallisten Liiga.fi-raporttien ja uutisten mukaan sarjataulukossa kuhisee juuri nyt kovasti:
{liiga_data[:400]}...

Tämä peli osoitti, että marraskuun pimeinä iltoina pisteet eivät irtoa helpolla. Voittaja otti henkisen yliotteen, ja hävinnyt joukkue joutuu palaamaan fläppitaulun ääreen miettimään puolustuspeliään uusiksi. Katso ottelun viralliset maalit, highlightsit ja ratkaisuhetket suoraan alta löytyvästä videolinkistä – tästä ei lätkä parane!" """
    return käsikirjoitus

def hae_uusimmat_liiga_videot():
    if not youtube:
        return []
    
    # Haetaan taustalle tuore uutisdata Liiga.fi-sivustolta
    print("Haetaan uutta uutisdataa Liiga.fi sivustolta...")
    liiga_data = hae_liigan_viralliset_uutiset()
    
    try:
        request = youtube.search().list(
            part="snippet", channelId=LIIGA_CHANNEL_ID, maxResults=5, order="date", type="video"
        )
        response = request.execute()
        liiga_videot = []
        for item in response.get("items", []):
            if "id" in item and "videoId" in item["id"]:
                title = item["snippet"].get("title", "Liiga-video")
                video_id = item["id"]["videoId"]
                kuvaus = item["snippet"].get("description", "")
                
                # Yhdistetään YouTube ja Liiga.fi tiedot pitkäksi selostukseksi
                käsikirjoitus = luo_2min_radioselostus(title, kuvaus, liiga_data)

                liiga_videot.append({
                    "otsikko": title,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "juonto": käsikirjoitus
                })
        return liiga_videot
    except Exception as e:
        print(f"Virhe haussa: {e}")
        return []

def aja_automaatio():
    print("Ajetaan yhdistetty YouTube + Liiga.fi automaatio...")
    videot = hae_uusimmat_liiga_videot()
    if not videot:
        print("Uusia videoita ei löytynyt.")
        return
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(videot, f, ensure_ascii=False, indent=4)
        print("Valmista! data.json päivitetty kaikilla tiedoilla.")
    except Exception as e:
        print(f"Virhe tallennuksessa: {e}")

if __name__ == "__main__":
    aja_automaatio()
