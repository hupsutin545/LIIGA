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

# Liigan virallinen oma YouTube-kanava ID
LIIGA_CHANNEL_ID = "UCGxrUE2U-ncnBf4vDww-gAQ" 

def luo_pitka_selostus(title, kuvaus):
    """Laajentaa videon tiedot pitkäksi ja kattavaksi otteluraportiksi"""
    clean_title = title.replace("Ottelukooste:", "").replace("| 5.9.2026", "").strip()
    
    alkujuonto = f"""
🏒 **SUURI OTTELURAPORTTI: {clean_title.upper()}**

Tervetuloa Liigan virallisen tekoälyselostajan kattavan otteluraportin pariin! Tässä artikkelissa pureudumme syvälle ottelun {clean_title} dramaattisiin käänteisiin, avainhetkiin ja pelillisiin hienouksiin. 

Ottelu tarjosi alusta loppuun saakka äärimmäisen korkeatasoista viihdettä, intensiivistä kamppailupelaamista sekä taktista shakkia molempien joukkueiden valmennusjohdolta. Kaukalossa nähtiin poikkeuksellista periksiantamattomuutta, kun joukkueet taistelivat kynsin ja hampain elintärkeistä sarjapisteistä. Koti- ja vierasjoukkueen fanit loivat areenalle huikean tunnelman, joka välittyi suoraan kenttätapahtumiin lisäten pelin fyysisyyttä ja vauhtia entisestään.
    """
    
    tapahtumat = f"""
📊 **OTTELUN SEURANTA JA TILASTRAPORTTI**

Videon virallisten tallenteiden ja ottelupöytäkirjan mukaan kamppailun kriittisimmät tilanteet, maalit sekä kurinpidolliset ratkaisut etenivät seuraavasti:

{kuvaus if kuvaus.strip() else "Ottelun intensiiviset maalitilanteet, huikeat maalivahtien torjunnat sekä taktiset erikoistilanteet ovat katsottavissa suoraan alla olevasta videokoosteesta."}
    """
    
    loppuyhteenveto = f"""
🔥 **ASIANTUNTIJAN ANALYYSI JA YHTEENVETO**

Tämä kamppailu osoitti jälleen kerran, miksi Liiga on yksi Euroopan viihdyttävimmistä ja tasaisimmista jääkiekkosarjoista. Ottelun voittaja ratkaistiin lopulta pienten marginaalien ja yksilötaidon kautta. Erikoistilannepelaaminen – varsinkin ylivoima- ja alivoimakoostumukset – nousi ottelun edetessä arvoon arvaamattomaan, ja molempien joukkueiden maalivahdit joutuivat venymään parhaimpaansa pitääkseen joukkueensa mukana pelissä.

Molemmat joukkueet voivat ottaa tästä pelistä paljon oppia tulevia kierroksia varten. Hävinnyt osapuoli joutuu varmasti viilaamaan puolustuspeliään ja kiekkokontrolliaan, kun taas voittaja pääsee rakentamaan tästä vahvaa jatkumoa seuraaviin koitoksiin. Taistelu pudotuspelipaikoista kiihtyy, ja jokainen piste on tässä vaiheessa kautta kultaakin kalliimpi!
    """
    
    # Yhdistetään kaikki osat yhdeksi todella pitkäksi tekstiksi
    return f"{alkujuonto}\n{tapahtumat}\n{loppuyhteenveto}"

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
                kuvaus = item["snippet"].get("description", "")
                
                # Luodaan uusi, huomattavasti pidempi selostusteksti
                pitka_teksti = luo_pitka_selostus(title, kuvaus)

                liiga_videot.append({
                    "otsikko": title,
                    "url": f"https://youtube.com{video_id}",
                    "juonto": pitka_teksti
                })
        return liiga_videot
    except Exception as e:
        print(f"Virhe haussa: {e}")
        return []

def aja_automaatio():
    print("Luodaan pitkiä otteluraportteja...")
    videot = hae_uusimmat_liiga_videot()
    if not videot:
        print("Uusia videoita ei löytynyt.")
        return
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(videot, f, ensure_ascii=False, indent=4)
        print("Valmista! data.json on päivitetty pitkillä teksteillä.")
    except Exception as e:
        print(f"Virhe tallennuksessa: {e}")

if __name__ == "__main__":
    aja_automaatio()
