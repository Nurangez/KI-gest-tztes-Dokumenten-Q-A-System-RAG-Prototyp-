import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # für config.py
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "embeddings"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "vectorstore"))

from embedder import embed_text
from store import search

frage = "who was killer in Russian"
ergebnisse = search(embed_text(frage), top_k=6)
print("Nur Russisch ohne 'answer': ")
print(frage + "\n")
for doc in ergebnisse["documents"][0]:
    print(doc[:200])
    print("---")


print("\n\n\n")

frage = "who was killer answer in Russian"
ergebnisse = search(embed_text(frage), top_k=6)
print("Russisch mit 'answer': ")
print(frage + "\n")
for doc in ergebnisse["documents"][0]:
    print(doc[:200])
    print("---")

