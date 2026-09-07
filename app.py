import os
import json
import requests
from googleapiclient.discovery import build
from huggingface_hub import InferenceClient

# 1. API-avaimet suoraan koodissa (toimii ilman GitHub Secrets -säätöä)
YOUTUBE_API_KEY = "AIzaSyCzqFkntOh2A7ZaWfaCQPoeMU1V5DFh14k"
HF_API_KEY = "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"

# Käynnistetään YouTube-yhteys
try:
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
except Exception as e:
    print(f"Kriittinen virhe YouTube-yhteyden alustuksessa: {e}")
    youtube = None

# Luodaan tekoälyasiakas Hugging Facen omalla virallisella työkalulla
client = InferenceClient(token=HF_API_KEY)

# Liigan virallinen oma YouTube-kanava ID
LIIGA_CHANNEL_ID = "UCGxrUE2U-ncnBf4vDww-gAQ" 

def hae_uusimmat_liiga_videot():
    if not youtube:
        return []
    try:
        request = youtube.search().list(
            part="snippet", 
            channelId=LIIGA_CHANNEL_ID, 
            maxResults=5, 
            order="date", 
            type="video"
        )
        response = request.execute()
        liiga_videot = []
        for item in response.get("items", []):
            if "id" in item and "videoId" in item["id"]:
                title = item["snippet"].get("title", "Liiga-video")
                video_id = item["id"]["videoId"]
                liiga_videot.append({
                    "otsikko": title,
                    "url": f"https://youtube.com{video_id}",
                    "kuvaus": item["snippet"].get("description", "")
                })
        return liiga_videot
    except Exception as e:
        print(f"Virhe YouTube-haussa: {e}")
        return []

def generoi_juonto_ilmaiseksi(video_url, videon_kuvaus):
    """Käyttää Hugging Facen virallista kirjastoa juonnon luomiseen"""
    prompt = f"""Tehtäväsi on luoda innostunut suomenkielinen ottelukooste jääkiekon Liiga-ottelusta.
    Videon linkki: {video_url}
    Videon kuvausteksti avuksi: {videon_kuvaus}
    
    Luo lyhyt teksti, jossa on:
    1. Lyhyt alkujuonto.
    2. Aikaleimat (esim. 01:23) tärkeistä tilanteista ranskalaisilla viivoilla.
    3. Lyhyt loppuyhteenveto.
    Vastaa pelkällä suomenkielisellä koosteella ilman alkutekstejä."""

    try:
        messages = [{"role": "user", "content": prompt}]
        
        # Käytetään tehokasta Qwen 2.5 -mallia chat-muodossa
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        if response and response.choices:
            return response.choices.message.content.strip()
        return "Juonnon luominen epäonnistui: Tyhjä vastaus tekoälyltä."
    except Exception as e:
        print(f"Virhe tekoälyssä videolle {video_url}: {e}")
        return "Juonnon luominen epäonnistui teknisen virheen vuoksi."

def aja_automaatio():
    print("Haetaan uusia Liiga-videoita...")
    videot = hae_uusimmat_liiga_videot()
    if not videot:
        print("Uusia Liiga-videoita ei löytynyt kanavalta juuri nyt.")
        return
        
    valmiit_leikkeet = []
    for video in videot:
        print(f"Luodaan ilmainen juonto videolle: {video['otsikko']}")
        juonto = generoi_juonto_ilmaiseksi(video["url"], video["kuvaus"])
        valmiit_leikkeet.append({
            "otsikko": video["otsikko"], 
            "url": video["url"], 
            "juonto": juonto
        })
    
    # Tallennetaan valmiit tiedot JSON-muotoon
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(valmiit_leikkeet, f, ensure_ascii=False, indent=4)
        print("Valmista! data.json päivitetty.")
    except Exception as e:
        print(f"Virhe JSON-tallennuksessa: {e}")

if __name__ == "__main__":
    aja_automaatio()
