import os
import json
from googleapiclient.discovery import build

# API-avain suoraan koodissa
YOUTUBE_API_KEY = "AIzaSyCzqFkntOh2A7ZaWfaCQPoeMU1V5DFh14k"

try:
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
except Exception as e:
    print(f"Virhe YouTubessa: {e}")
    youtube = None

LIIGA_CHANNEL_ID = "UCGxrUE2U-ncnBf4vDww-gAQ" 

def hae_uusimmat_liiga_videot():
    if not youtube:
        return []
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
                kuvaus = item["snippet"].get("description", "Katso ottelun kooste videosta!")
                
                # Täysin puhdas juontomuotoilu videon omista tiedoista
                liiga_videot.append({
                    "otsikko": title,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "juonto": f"🏒 **Ottelun viralliset tapahtumat:**\n\n{kuvaus}"
                })
        return liiga_videot
    except Exception as e:
        print(f"Virhe haussa: {e}")
        return []

def aja_automaatio():
    print("Päivitetään Liiga-sivustoa...")
    videot = hae_uusimmat_liiga_videot()
    if not videot:
        return
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(videot, f, ensure_ascii=False, indent=4)
        print("Valmista!")
    except Exception as e:
        print(f"Virhe tallennuksessa: {e}")

if __name__ == "__main__":
    aja_automaatio()
