import chromadb
from config import CHROMA_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def add_documents(chunks: list[str], vectors: list[list[float]], metadatas: list[dict], ids: list[str]):
    collection.add(documents=chunks, embeddings=vectors, metadatas=metadatas, ids=ids)


def search(query_vector: list[float], top_k: int = 5):
    return collection.query(query_embeddings=[query_vector], n_results=top_k)