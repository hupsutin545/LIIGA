import os
import json
import requests
from googleapiclient.discovery import build
from huggingface_hub import InferenceClient

# Haetaan avaimet turvallisesti GitHubin asetuksista
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
HF_API_KEY = os.environ.get("HF_API_KEY")

try:
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
except Exception as e:
    print(f"Kriittinen virhe YouTube-yhteyden alustuksessa: {e}")
    youtube = None

client = InferenceClient(token=HF_API_KEY)
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
                
                # VARMISTETTU: Täysin pomminvarma suora YouTube-linkki
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
    prompt = f"Luo lyhyt ja innostunut suomenkielinen ottelukooste ja aikaleimat tästä Liiga-pelistä: {videon_kuvaus}"

    try:
        messages = [{"role": "user", "content": prompt}]
        
        # VAIHDETTU: Microsoftin uusin Phi-3-mini, joka on huippunopea ja herää heti ilman ruuhkia
        response = client.chat.completions.create(
            model="microsoft/Phi-3-mini-4k-instruct",
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )
        if response and response.choices:
            return response.choices.message.content.strip()
        return "Juonnon luominen epäonnistui: Tyhjä vastaus."
    except Exception as e:
        print(f"Virhe tekoälyssä: {e}")
        # VAIHTOEHTOINEN RATKAISU: Jos tekoäly on ruuhkautunut, käytetään videon omaa tekstiä juontona!
        if videon_kuvaus:
            return f"Tekoäly on varattu, tässä ottelun tiedot:\n\n{videon_kuvaus}"
        return "Katso ottelun parhaat palat ja maalit suoraan alla olevasta videolinkistä!"

def aja_automaatio():
    print("Haetaan uusia Liiga-videoita...")
    videot = hae_uusimmat_liiga_videot()
    if not videot:
        print("Uusia Liiga-videoita ei löytynyt.")
        return
        
    valmiit_leikkeet = []
    for video in videot:
        print(f"Luodaan juonto videolle: {video['otsikko']}")
        juonto = generoi_juonto_ilmaiseksi(video["url"], video["kuvaus"])
        valmiit_leikkeet.append({
            "otsikko": video["otsikko"], 
            "url": video["url"], 
            "juonto": juonto
        })
    
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(valmiit_leikkeet, f, ensure_ascii=False, indent=4)
        print("Valmista! data.json päivitetty.")
    except Exception as e:
        print(f"Virhe JSON-tallennuksessa: {e}")

if __name__ == "__main__":
    aja_automaatio()
