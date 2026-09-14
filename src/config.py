import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "dokumente"

CHUNK_SIZE = 500
OVERLAP = 50
TOP_K = 6