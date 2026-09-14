import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "..")

sys.path.insert(0, SRC_DIR)
sys.path.insert(0, os.path.join(SRC_DIR, "embeddings"))
sys.path.insert(0, os.path.join(SRC_DIR, "vectorstore"))

from loader import load_pdf, load_docx, load_xlsx, load_pptx, load_txt, load_csv
from chunker import chunk_text
from embedder import embed_chunks
from store import add_documents
from config import CHUNK_SIZE, OVERLAP

DATA_DIR = os.path.join(CURRENT_DIR, "..", "..", "data")


def load_file(path: str) -> str:
    if path.endswith(".pdf"):
        return load_pdf(path)
    elif path.endswith(".docx"):
        return load_docx(path)
    elif path.endswith(".xlsx"):
        return load_xlsx(path)
    elif path.endswith(".pptx"):
        return load_pptx(path)
    elif path.endswith(".txt"):
        return load_txt(path)
    elif path.endswith(".csv"):
        return load_csv(path)
    else:
        print(f"Format nicht unterstützt, übersprungen: {path}")
        return ""


def main():
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        print(f"Verarbeite: {filename}")

        text = load_file(filepath)
        if not text:
            continue

        chunks = chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP)
        vectors = embed_chunks(chunks)

        ids = [f"{filename}_chunk{i}" for i in range(len(chunks))]
        metadatas = [{"source_file": filename} for _ in chunks]

        add_documents(chunks, vectors, metadatas, ids)
        print(f"  → {len(chunks)} Chunks gespeichert.")


if __name__ == "__main__":
    main()