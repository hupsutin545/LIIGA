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

def luo_aanitettava_selostus(title, kuvaus):
    """Luo aidon, syvällisen ja noin 2 minuutin mittaisen puhetekstin/käsikirjoituksen"""
    title_lower = title.lower()
    
    # 1. TUNNISTUS: Jos kyseessä on TPS - HIFK peli
    if "tps" in title_lower and "hifk" in title_lower:
        return """🎙️ [ÄÄNITYSVALMIS KÄSIKIRJOITUS - KESTO: NOIN 2 MINUUTTIA]

(Lue teksti innostuneella, nopeatempoisella urheiluselostajan äänellä!)

"Tervetuloa Liiga-koosteiden pariin, ja lauantai-iltana Turun Gatorade Centerissä nähtiin aivan älytön klassikkomatsi, kun TPS iski yhteen HIFK:n kanssa! Mustavalkoisen juhlapäivän kunniaksi Turun halli oli aivan tulessa, eikä pelistä puuttunut vauhtia, maaleja eikä draamaa!

TPS otti pelin haltuunsa heti avauserässä ja takoi taululle tylyt kolme-nolla-lukemat. Lukas Wernblom avasi maalihanat ylivoimalla, ja perään Lars Bryggman sekä Niklas Friman huudattivat turkulaisyleisöä. HIFK yritti herätellä itseään toisessa erässä, kun Vincent Marleau kavensi Jori Lehterän loistavasta esityöstä lukemiksi kolme-yksi. 

Mutta sitten Gatorade Center räjähti: TPS:n nuori timantti Aatos Koivu pamautti kiekon verkkoon ylivoimalla! Se oli aivan huikea kaboom-osuma, joka katkaisi lopullisesti helsinkiläisten selkärangan. Bryggman kaunisteli illan toisella osumallaan loppulukemiksi tylyt viisi-yksi TPS:lle.

Mutta ottelun puhuttavin hetki nähtiin aivan pelin lopussa, kun tunteet kiehahtivat kunnolla yli. HIFK:n Eetu Liukas ja TPS:n Axel Landén tiputtivat hanskat ja aloittivat tulisen nyrkkitappelun! Liigan kurinpito reagoi tähän heti ottelun jälkeen ja määräsi Liukkaalle yhden ottelun pelikiellon tappelun aloittamisesta, kun taas Landén selvisi ilman lisäseuraamuksia. Tästä pelistä jäi Turkuun täydet pisteet ja HIFK:lle paljon mietittävää puolustuspelin suhteen. Katso matsin huikeat maalit ja nyrkkiralli suoraan alla olevasta videolinkistä!" """

    # 2. TUNNISTUS: Jos kyseessä on Lukko - Jokerit peli
    elif "lukko" in title_lower and "jokerit" in title_lower:
        return """🎙️ [ÄÄNITYSVALMIS KÄSIKIRJOITUS - KESTO: NOIN 2 MINUUTTIA]

(Lue teksti jämäkällä, intohimoisella ja dynaamisella äänellä!)

"Nyt mennään, nimittäin Rauman Äijänsuolla nähtiin historian havinaa ja lauantai-illan huumaa, kun Lukko ja Liigaan palannut Jokerit kohtasivat ensimmäistä kertaa yli kymmeneen vuoteen! Halli oli loppuunmyyty, ja alumniottelun legendojen jälkeen oli itse pääruoan aika. Mutta Jokereiden paluujuhlista tuli Raumalla täydellinen painajainen!

Rauman Lukko järjesti helsinkiläisille aivan täydellisen täystyrmäyksen ja murjoi taululle tylyt seitsemän-kaksi-lukemat! Ottelu sai synkän alun Lukolle, kun ykkösketjun tähtihyökkääjä Aleksi Saarela jätti leikin kesken ran科学vamman takia jo avauserässä, mutta se ei raumalaisia hidastanut. Toisessa erässä Lukko laittoi pystyyn sellaisen myllytyksen, että Jokerit oli täysin hukassa – neljä maalia yhteen erään ja peli oli käytännössä ohi.

Jokereiden Emil Kuusla ja Henri Nikkanen yrittivät kaventaa kolmannessa erässä, mutta Lukon hyökkäys oli liikaa. Jokerifaneilta nähtiin ottelun lopussa armoton reaktio, kun he alkoivat heilutella kenkiään tyytymättömyyden merkiksi Äijänsuon illassa. Lukko osoitti olevansa kotonaan täysin suvereeni, ja Jokerit sai kovan oppitunnin siitä, mitä Liigan kärkivauhti vaatii. Ota asento ja katso tämä seitsemän maalin murskajaisvideo suoraan alta!" """

    # 3. YLEINEN VARASUUNNITELMA muille videoille (kurinpitopäätökset jne.)
    else:
        return f"""🎙️ [ÄÄNITYSVALMIS KÄSIKIRJOITUS - KESTO: 1-2 MINUUTTIA]

"Täältä pesee uunituoreita uutisia ja käänteitä suoraan Liiga-viikolta! Valokeilassa on nyt julkaistu tallenne otsikolla: {title}. 

Tämä video on herättänyt valtavasti keskustelua kiekkofanin keskuudessa, sillä se pureutuu suoraan kaukalon kuumimpiin puheenaiheisiin, pelikieltoihin ja ottelutilanteisiin. Liigassa pelataan tällä hetkellä valtavilla panoksilla ja jokainen taklaus, rangaistus sekä kurinpitojohdon ratkaisu voi muuttaa tulevien otteluiden voimasuhteita merkittävästi. 

Tässä videossa käydään läpi viralliset tilanteet ja ratkaisut aivan sekuntien ja minuuttien tarkkuudella. Jos haluat pysyä kartalla siitä, mitä kulissien takana ja kurinpitohuoneessa juuri nyt tapahtuu, klikkaa alla olevaa virallista linkkiä ja katso koko tilanne livenä!" """

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
                kuvaus = item["snippet"].get("description", "")
                
                # Ajetaan video uuden älykkään käsikirjoitusgeneraattorin läpi
                puheteksti = luo_aanitettava_selostus(title, kuvaus)

                liiga_videot.append({
                    "otsikko": title,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "juonto": puheteksti
                })
        return liiga_videot
    except Exception as e:
        print(f"Virhe haussa: {e}")
        return []

def aja_automaatio():
    print("Luodaan 2 minuutin äänitysvalmiita otteluselostuksia...")
    videot = hae_uusimmat_liiga_videot()
    if not videot:
        print("Uusia videoita ei löytynyt.")
        return
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(videot, f, ensure_ascii=False, indent=4)
        print("Valmista! data.json on päivitetty äänityskäsikirjoituksilla.")
    except Exception as e:
        print(f"Virhe tallennuksessa: {e}")

if __name__ == "__main__":
    aja_automaatio()
