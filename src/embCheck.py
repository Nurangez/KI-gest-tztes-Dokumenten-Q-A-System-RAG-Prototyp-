import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "embeddings"))
sys.path.append(os.path.join(os.path.dirname(__file__), "vectorstore"))
from config import TOP_K

from embedder import embed_text
from store import search

ergebnisse = search(embed_text("who was killer"), top_k=TOP_K)
print("=== OHNE Russian ===")
for doc in ergebnisse["documents"][0]:
    print(doc)
    print("---")

ergebnisse2 = search(embed_text("who was killer answer in Russian"), top_k=TOP_K)
print("\n=== MIT Russian ===")
for doc in ergebnisse2["documents"][0]:
    print(doc)
    print("---")