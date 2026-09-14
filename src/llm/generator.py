import time
from google import genai
from google.genai import errors

client = genai.Client(api_key="API_KEY")
m = ["gemini-2.5-flash", "gemini-3.5-flash", "gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash" ]


def generate_answer(frage: str, kontext_chunks: list[str], max_retries: int = 3) -> str:
    kontext = "\n\n".join(kontext_chunks)
    i=0
    prompt = f"""Beantworte die Frage NUR basierend auf folgendem Kontext: {kontext}
Antworte auf {frage}
Wenn die Antwort nicht im Kontext steht, sage "Dazu habe ich keine Information."
"""

    while i<len(m):
        try:
            response = client.models.generate_content(
                model=m[i],
                contents=prompt)
            return response.text
        except errors.ServerError:
            # 503 - Server überlastet
                i+=1
                time.sleep(5)
                continue
            
        except errors.ClientError as e:
            # 429 - Kontingent überschritten
            if "RESOURCE_EXHAUSTED" in str(e):
                i+=1
                time.sleep(5)
                continue
            

    return "Die Anfrage konnte nicht verarbeitet werden."