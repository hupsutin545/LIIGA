import os
import json
import google.generativeai as genai
from googleapiclient.discovery import build

# 1. Alustetaan API-avaimet ympäristömuuttujista
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# MTV Urheilun YouTube-kanavan ID (Kanava, joka julkaisee viralliset Liiga-koosteet)
MTV_URHEILU_CHANNEL_ID = "UC70NfP88pG69f6K7v3bMv_g" 

def hae_uusimmat_liiga_videot():
    """Hakee kanavan 5 uusinta videota ja suodattaa Liiga-pelit"""
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=MTV_URHEILU_CHANNEL_ID,
            maxResults=5,
            order="date",
            type="video"
        )
        response = request.execute()
        
        liiga_videot = []
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            video_url = f"https://youtube.com{video_id}"
            
            # Varmistetaan, että kyseessä on Liiga-ottelun kooste
            if "Liiga" in title or "kohokohdat" in title.lower():
                liiga_videot.append({
                    "otsikko": title,
                    "url": video_url,
                    "kuvaus": item["snippet"]["description"]
                })
        
        return liiga_videot
    except Exception as e:
        print(f"Virhe YouTube-haussa: {e}")
        return []

def generoi_juonto(video_url, videon_kuvaus):
    """Pyytää Gemini-tekoälyä luomaan otteluraportin ja aikaleimat"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Tehtäväsi on luoda innostunut ja asiantunteva suomenkielinen ottelukooste ja juonto jääkiekon Liiga-ottelusta.
    Tässä on videon linkki: {video_url}
    Tässä on videon alkuperäinen kuvausteksti avuksi: {videon_kuvaus}
    
    Luo teksti, joka sisältää:
    1. Lyhyen, mukaansatempaavan alkujuonnon ottelusta.
    2. Selkeät aikaleimat sekuntien tarkkuudella (esim. 01:23) tärkeimmistä tilanteista (Maalit, jäähyt, isot torjunnat) ja lyhyt kuvaus mitä siinä tapahtuu.
    3. Lyhyen loppuyhteenvedon.
    
    Muotoile vastaus siististi ranskalaisilla viivoilla aikaleimojen osalta.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Virhe Gemini-generoinnissa: {e}")
        return "Juonnon luominen epäonnistui."

def aja_automaatio():
    print("Haetaan uusia Liiga-videoita YouTubesta...")
    videot = hae_uusimmat_liiga_videot()
    
    if not videot:
        print("Uusia Liiga-videoita ei löytynyt juuri nyt.")
        return
        
    valmiit_leikkeet = []
    
    # Käydään läpi löydetyt videot ja luodaan juonnot
    for video in videot:
        print(f"Luodaan juonto videolle: {video['otsikko']}")
        juonto = generoi_juonto(video["url"], video["kuvaus"])
        
        valmiit_leikkeet.append({
            "otsikko": video["otsikko"],
            "url": video["url"],
            "juonto": juonto
        })
    
    # Tallennetaan kaikki uudet leikkeet data.json-tiedostoon verkkosivua varten
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(valmiit_leikkeet, f, ensure_ascii=False, indent=4)
        
    print("Kaikki valmista! data.json on päivitetty.")

if __name__ == "__main__":
    aja_automaatio()
