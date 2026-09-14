from embedder import embed_text
import numpy as np

def cosinus(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

basis = embed_text("who was killer")
mit_titel = embed_text("who was killer in Sparkling Cyanide")
mit_titel_russisch = embed_text("who was killer in Sparkling Cyanide in Russian")
russisch_zusatz = embed_text("who was killer answer in Russian")
nur_russisch_zusatz = embed_text("who was killer in Russian")



print("Basis vs. mit Titel:        ", cosinus(basis, mit_titel))
print("Basis vs. Titel+Russisch:   ", cosinus(basis, mit_titel_russisch))
print("Basis vs. Russisch:         ", cosinus(basis, russisch_zusatz))
print("Basis vs. nur Russisch:     ", cosinus(basis, nur_russisch_zusatz))