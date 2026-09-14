from embeddings.embedder import embed_text
from vectorstore.store import search
from llm.generator import generate_answer
from config import TOP_K


def answer_question(frage: str) -> str:
    frage_vektor = embed_text(frage)
    ergebnisse = search(frage_vektor, top_k=TOP_K)
    kontext_chunks = ergebnisse["documents"][0]
    return generate_answer(frage, kontext_chunks)