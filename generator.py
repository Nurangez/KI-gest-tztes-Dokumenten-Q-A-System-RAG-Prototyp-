import time
from google import genai
from google.genai import errors
from config import API_KEY

client = genai.Client(api_key=API_KEY)
m = ["gemini-2.5-flash", "gemini-3.5-flash", "gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash"]


def generate_answer(frage: str, kontext_chunks: list[str]) -> str:
    kontext = "\n\n".join(kontext_chunks)
    prompt = f"""Beantworte die Frage NUR basierend auf folgendem Kontext: {kontext}
Antworte auf {frage}
Wenn die Antwort nicht im Kontext steht, sage "Dazu habe ich keine Information."
"""

    for modell in m:
        try:
            response = client.models.generate_content(model=modell, contents=prompt)
            return response.text
        except errors.ServerError as e:
            print(f"{modell}: Server überlastet ({e}), nächstes Modell...")
            time.sleep(2)
            continue
        except errors.ClientError as e:
            print(f"{modell}: Fehler ({e}), nächstes Modell...")
            time.sleep(2)
            continue

    return "Die Anfrage konnte nicht verarbeitet werden."