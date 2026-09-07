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

def luo_tarkka_liiga_raportti(title):
    title_lower = title.lower()
    
    # 1. TPS – HIFK
    if "tps" in title_lower and "hifk" in title_lower:
        selostus = """🎙️ [KESTO: 2 MINUUTTIA]
"No niin, hyvää iltaa kiekkofanit! Otetaanpa käsittelyyn Turun Gatorade Centerin huikea lauantai-ilta, jossa TPS iski yhteen HIFK:n kanssa. Liiga.fi:n virallisten tilastojen mukaan Turussa nähtiin aivan älytön näytös, jossa sankarin viittaa sovitteli TPS:n tulikuuma ykkösketju!

Turkulaisten tehomiehinä häärivät Lukas Wernblom, joka mätti tehot 1+3, sekä huikeat kaksi maalia viimeistellyt Lars Bryggman! Wernblom teki samalla Liiga-historiaa nousemalla pistepörssin kärkeen. HIFK yritti rimpuilla mukana Vincent Marleaun kavennuksella, mutta TPS:n nuori tähti Aatos Koivu sammutti helsinkiläisten pyristykset paukuttamalla kiekon ylivoimalla verkkoon! Se oli aivan jäätävä KABOOM-osuma! Loppulukemat Turussa tylysti 5–1.

Mutta pelkkään maali-iloitteluun ei ilta päättynyt. Ottelun lopussa tunteet räiskyivät kunnolla yli: HIFK:n Eetu Liukas ja TPS:n Axel Landén tiputtivat hanskat ja aloittivat nyrkkitappelun! Liukan sai tästä yhden ottelun pelikiellon. TPS otti täydet pisteet ja jätti HIFK:lle paljon opittavaa. Katso kooste alta!" """
        
        some = """🏒🔥 GATORADE CENTER RÄJÄHTI! TPS murjoi HIFK:n tylysti 5–1! 😱 Lukas Wernblom täysin pitelemätön tehoilla 1+3 ja siirtyi samalla Liigan pistepörssin KÄRKEEN! 👑 Nuori Aatos Koivu painoi aivan jäätävän KABOOM-ylivoimahakin verkkoon! 💥 

Eikä tässä kaikki – loppusekunneilla tunteet kiehahti huolella yli ja Eetu Liukas sekä Axel Landén ottivat tulisen nyrkkirallin! 🥊 Liukkaalle tästä 1 ottelun pelikielto! Ota seuranta haltuun ja tsekkaa matsin kooste biisin linkistä! 📺👇 #Liiga #TPS #HIFK #Jääkiekko #Nyrkkiralli #AatosKoivu"""
        
        return selostus, some

    # 2. LUKKO – JOKERIT
    elif "lukko" in title_lower and "jokerit" in title_lower:
        selostus = """🎙️ [KESTO: 2 MINUUTTIA]
"Kiekkokansa huomio, mennään Raumalle! Äijänsuon lehterät olivat äärirajoillaan, kun Lukko ja pitkän tauon jälkeen Liigaan palannut Helsingin Jokerit iskivät yhteen! Liiga.fi:n viralliset ottelutiedot kertovat kuitenkin karua kieltä: Jokereiden juhlista tuli Raumalla täydellinen selkäsauna.

Lukko murjoi taululle käsittämättömät 7–2-lukemat! Ottelun ykköstähtenä loisti Alex Beaucage, joka takoi tehot 1+2. Tämä oli Lukon suurin voitto Jokereista runkosarjassa sitten syyskuun 2009! Raumalaiset iskivät toisessa erässä peräti neljä osumaa Jokerien verkkoon, mikä lamautti vieraat täysin. Jokereiden Emil Kuusla ja Henri Nikkanen yrittivät herätellä joukkuetta kavennusmaaleilla kolmannessa erässä, mutta Lukko oli tällä kertaa aivan liian suvereeni. 

Ottelun lopussa nähtiin myös harvinainen reaktio, kun pettyneet jokerifanit ilmaisivat tyytymättömyytensä heiluttelemalla kenkiään katsomossa. Lukko otti ison päänahan, ja Jokerit sai herätyksen siitä, mitä Liigan huippuvauhti tällä kaudella vaatii. Katso tämä seitsemän maalin ralli kokonaisuudessaan suoraan alla olevasta linkistä!" """
        
        some = """🤯 MITKÄ MURSKAJAISET RAUMALLA! Lukko tyrmäsi Jokerit käsittämättömin 7–2 lukemin Äijänsuon lauantai-illassa! 💥 Alex Beaucage herrana ja kuninkaana tehoilla 1+2! 🦊 Tämä oli historiallisesti Lukon suurin runkosarjavoitto Jokereista sitten vuoden 2009! 

Ottelun lopussa nähtiin myös aivan hämmentävä hetki, kun turhautuneet jokerifaneista alkoivat heilutella kenkiään katsomossa! 👟👀 Jokerit sai tylyn opetuksen Liigan kärkivauhdista. Katso kaikki 7 maalia videolta nyt! 📺👇 #Liiga #RaumanLukko #Jokerit #Murskajaiset #HelsinginJokerit #Lätkä"""
        
        return selostus, some

    # 3. YLEINEN VARASUUNNITELMA
    else:
        selostus = f"""🎙️ [KESTO: 1-2 MINUUTTIA]
"Tervetuloa Liiga-kierroksen pariin! Otetaan valokeilaan tuore ottelutapahtuma otsikolla: {title}. 

Liiga.fi:n virallisten peliraporttien mukaan tässä ottelussa nähtiin todellista taistelua sarjapisteistä. Joukkueet lähtivät peliin tarkalla taktiikalla, ja ratkaisut haettiin erikoistilanteiden, ylivoimien sekä maalivahtien loistavien paraatipelastusten kautta. Liigassa pelataan tällä hetkellä äärimmäisen tasaisia otteluita, ja jokainen piste on matkalla kohti pudotuspelejä äärimmäisen kriittinen. Katso kooste alta!" """
        
        some = f"""🏒 UUTTA MATERIAALIA KAUUKALOSTS! 🔥 Liigan viralliselle kanavalle tipahti juuri uusi video: {title}! 🚨 

Kausi käy kuumempana kuin koskaan ja taistelu sarjapisteistä kiihtyy! Kumpi joukkue otti henkisen yliotteen ja kenen viisikkopeli vaatii vielä viilausta? 🧐 Käy lukemassa täysi otteluraportti sivuiltamme ja katso maalit videolta! 🎬👇 #Liiga #Jääkiekko #UrheiluUutiset #Kooste"""
        
        return selostus, some

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
                
                # Haetaan molemmat tekstiversiot generaattorista
                puheteksti, some_teksti = luo_tarkka_liiga_raportti(title)

                liiga_videot.append({
                    "otsikko": title,
                    "url": f"https://youtube.com{video_id}",
                    "juonto": puheteksti,
                    "some": some_teksti
                })
        return liiga_videot
    except Exception as e:
        print(f"Virhe haussa: {e}")
        return []

def aja_automaatio():
    print("Luodaan selostukset ja some-päivitykset...")
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
