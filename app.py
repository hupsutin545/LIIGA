import os
import json
import google.generativeai as genai

# Määritetään tekoälyn asetukset (Gemini API on usein ilmainen tiettyynrajaan asti)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generoi_juonto(video_url):
    # Pyydetään tekoälyä analysoimaan video linkin pohjalta
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Katso tämä YouTube-video Liiga-highlighteista: {video_url}
    Luo videosta suomenkielinen, innostunut ottelukooste aikaleimoineen.
    Muotoile vastaus lyhyiksi ranskalaisiksi viivoiksi, joissa on sekuntiaika (esim. 01:23) ja lyhyt kuvaus siitä mitä tapahtuu (esim. Maali, jäähy, torjunta).
    """
    
    response = model.generate_content(prompt)
    return response.text

def paivita_sivusto():
    # Tähän kohtaan automatisoidaan myöhemmin YouTube-haku.
    # Testataan ensin yhdellä esimerkkivideolla:
    testi_video_url = "https://youtube.com" 
    
    print("Analysoidaan videota tekoälyllä...")
    juonto = generoi_juonto(testi_video_url)
    
    # Luodaan uusi data-objekti
    uusi_leike = {
        "otsikko": "Liiga Ottelukooste",
        "url": testi_video_url,
        "juonto": juonto
    }
    
    # Tallennetaan tiedot JSON-tiedostoon, jota verkkosivu lukee
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump([uusi_leike], f, ensure_ascii=False, indent=4)
    print("Päivitetty data.json onnistuneesti!")

if __name__ == "__main__":
    paivita_sivusto()
