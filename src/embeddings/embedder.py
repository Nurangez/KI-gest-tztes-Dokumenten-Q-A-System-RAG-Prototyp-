from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")


def embed_text(text: str) -> list[float]:
    return model.encode(text).tolist()


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    return model.encode(chunks).tolist()