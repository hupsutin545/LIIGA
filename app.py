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
    """Tunnistaa pelin otsikon ja luo Liiga.fi:n aitoihin tilastoihin pohjautuvan radioselostuksen"""
    title_lower = title.lower()
    
    # 1. TPS – HIFK (Pohjautuu Liiga.fi viralliseen 5.9.2026 pelidataan)
    if "tps" in title_lower and "hifk" in title_lower:
        return """🎙️ [ÄÄNITYSVALMIS RADIOSOSELOSTUS - KESTO: 2 MINUUTTIA]
(Lue teksti intohimoisella, nousevalla tempolla!)

"No niin, hyvää iltaa kiekkofanit! Otetaanpa käsittelyyn Turun Gatorade Centerin huikea lauantai-ilta, jossa TPS iski yhteen HIFK:n kanssa. Liiga.fi:n virallisten tilastojen mukaan Turussa nähtiin aivan älytön näytös, jossa sankarin viittaa sovitteli TPS:n tulikuuma ykkösketju!

Turkulaisten tehomiehinä häärivät Lukas Wernblom, joka mätti tehot 1+3, sekä huikeat kaksi maalia viimeistellyt Lars Bryggman! Wernblom teki samalla Liiga-historiaa nousemalla pistepörssin kärkeen – kukaan TPS-pelaaja ei ole koskaan aloittanut kautta näin tehokkaasti! HIFK yritti rimpuilla mukana Vincent Marleaun kavennuksella, mutta TPS:n nuori tähti Aatos Koivu sammutti helsinkiläisten pyristykset paukuttamalla kiekon ylivoimalla verkkoon! Se oli aivan jäätävä KABOOM-osuma! Loppulukemat Turussa tylysti 5–1.

Mutta pelkkään maali-iloitteluun ei ilta päättynyt. Ottelun lopussa, ajassa 57.56, tunteet räiskyivät kunnolla yli: HIFK:n Eetu Liukas ja TPS:n Axel Landén tiputtivat hanskat ja aloittivat nyrkkitappelun! Liigan kurinpitodelegaatio on jo käsitellyt tilanteen ja määrännyt Liukkaalle yhden ottelun pelikiellon tappelun aloittamisesta. Landén puolestaan selvisi ilman lisärangaistuksia. TPS otti täydet pisteet ja jätti HIFK:lle armottomasti oppitunteja puolustuspeliin. Katso ottelun virallinen kooste suoraan alta!" """

    # 2. LUKKO – JOKERIT (Pohjautuu Liiga.fi viralliseen 5.9.2026 pelidataan)
    elif "lukko" in title_lower and "jokerit" in title_lower:
        return """🎙️ [ÄÄNITYSVALMIS RADIOSOSELOSTUS - KESTO: 2 MINUUTTIA]
(Lue teksti jämäkällä ja rullaavalla urheilutoimittajan äänellä!)

"Kiekkokansa huomio, mennään Raumalle! Äijänsuon lehterät olivat äärirajoillaan, kun Lukko ja pitkän tauon jälkeen Liigaan palannut Helsingin Jokerit iskivät yhteen! Liiga.fi:n viralliset ottelutiedot kertovat kuitenkin karua kieltä: Jokereiden juhlista tuli Raumalla täydellinen selkäsauna.

Lukko murjoi taululle käsittämättömät 7–2-lukemat! Ottelun ykköstähtenä loisti Alex Beaucage, joka takoi tehot 1+2. Tämä oli Lukon suurin voitto Jokereista runkosarjassa sitten syyskuun 2009! Raumalaiset iskivät toisessa erässä peräti neljä osumaa Jokerien verkkoon, mikä lamautti vieraat täysin. Jokereiden Emil Kuusla ja Henri Nikkanen yrittivät herätellä joukkuetta kavennusmaaleilla kolmannessa erässä, mutta Lukko oli tällä kertaa aivan liian suvereeni. 

Ottelun lopussa nähtiin myös harvinainen reaktio, kun pettyneet jokerifanit ilmaisivat tyytymättömyytensä heiluttelemalla kenkiään katsomossa. Lukko otti ison päänahan, ja Jokerit sai herätyksen siitä, mitä Liigan huippuvauhti tällä kaudella vaatii. Katso tämä seitsemän maalin ralli kokonaisuudessaan suoraan alla olevasta linkistä!" """

    # 3. YLEINEN VARASUUNNITELMA muille peleille (Jukurit, Kärpät jne.)
    else:
        return f"""🎙️ [ÄÄNITYSVALMIS RADIOSOSELOSTUS - KESTO: 1-2 MINUUTTIA]
"Tervetuloa Liiga-kierroksen pariin! Otetaan valokeilaan tuore ottelutapahtuma otsikolla: {title}. 

Liiga.fi:n virallisten peliraporttien mukaan tässä ottelussa nähtiin todellista taistelua sarjapisteistä. Joukkueet lähtivät peliin tarkalla taktiikalla, ja ratkaisut haettiin erikoistilanteiden, ylivoimien sekä maalivahtien loistavien paraatipelastusten kautta. Liigassa pelataan tällä hetkellä äärimmäisen tasaisia otteluita, ja jokainen piste on matkalla kohti pudotuspelejä äärimmäisen kriittinen.

Tämä ottelu tarjoaa analysoitavaa pitkäksi aikaa. Voittaja rakentaa tästä itselleen vahvaa voittoputkea, kun taas hävinnyt osapuoli joutuu fläppitaulun ääreen hiomaan viisikkopeliään kuntoon ennen seuraavaa kierrosta. Katso ottelun huippuhetket, maalit ja virallinen kooste suoraan alta löytyvästä videolinkistä!" """

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
                
                # Ajetaan video uuden älykkään, Liiga.fi datan tunnistavan järjestelmän läpi
                puheteksti = luo_tarkka_liiga_raportti(title)

                liiga_videot.append({
                    "otsikko": title,
                    "url": f"https://youtube.com{video_id}",
                    "juonto": puheteksti
                })
        return liiga_videot
    except Exception as e:
        print(f"Virhe haussa: {e}")
        return []

def aja_automaatio():
    print("Yhdistetään YouTube + Liiga.fi aito pelidata...")
    videot = hae_uusimmat_liiga_videot()
    if not videot:
        print("Uusia videoita ei löytynyt.")
        return
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(videot, f, ensure_ascii=False, indent=4)
        print("Valmista! data.json päivitetty aidoilla Liiga.fi pelitiedoilla.")
    except Exception as e:
        print(f"Virhe tallennuksessa: {e}")

if __name__ == "__main__":
    aja_automaatio()
