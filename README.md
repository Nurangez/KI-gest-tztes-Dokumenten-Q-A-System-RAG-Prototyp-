# 🤖 KI-gestütztes Dokumenten-Q&A-System (RAG-Prototyp)

Ein Prototyp, der es ermöglicht, in natürlicher Sprache Fragen zu internen
Firmendokumenten (PDF, Word, Excel, CSV, PowerPoint) zu stellen. Entstanden
als Vorbereitung/Selbsttest im Rahmen einer Bewerberaufgabe zum Thema
"RAG-System für ~5.000 interne Unternehmensdokumente".

## 🌟 Highlights

- 📄 Unterstützt 6 Dateiformate: PDF, Word, Excel, CSV, PowerPoint, TXT
- 🌍 Mehrsprachiges Embedding-Modell für zuverlässige Suche über Sprachgrenzen hinweg
- 🔁 Automatischer Fallback über mehrere Gemini-Modelle bei Serverfehlern (503/429)
- 🧪 Datengestützt getestet und iteriert (Chunk-Größe, Retrieval-Tiefe, Embedding-Modell)
- ⚛️ Eigenständiges React-Frontend + Django-API, klar getrennt

## ℹ️ Überblick

Dieses Projekt ist ein RAG-System (Retrieval-Augmented Generation): Mitarbeitende
sollen Fragen zu tausenden internen Dokumenten stellen können, ohne dass das
gesamte Unternehmenswissen bei jeder Anfrage neu an ein Sprachmodell geschickt
werden muss. Erstellt als praktische Umsetzung und Selbsttest zu einer Bewerberaufgabe.

## 📋 Aufgabenstellung

Ein mittelständisches Unternehmen möchte, dass Mitarbeitende Fragen zu rund
5.000 internen Dokumenten in natürlicher Sprache stellen können – mit zwei
Wochen Zeit bis zur ersten Kunden-Demo. Dieses Repository dokumentiert meinen
Lösungsansatz, meine Testergebnisse und die dabei gewonnenen Erkenntnisse.

## 🏗️ Architektur

```
Dokument → Loader → Chunker → Embedder → Vectorstore (Chroma) → LLM (Gemini) → Antwort
```

- **📂 Loader** (`src/ingestion/loader.py`) – extrahiert Text aus PDF, Word,
  Excel, CSV, PowerPoint, TXT
- **✂️ Chunker** (`src/ingestion/chunker.py`) – teilt Dokumente in überlappende
  Textabschnitte (konfigurierbare Chunk-Größe/Overlap)
- **🧬 Embedder** (`src/embeddings/embedder.py`) – wandelt Text mit einem
  mehrsprachigen Sentence-Transformer-Modell in Vektoren um
- **🗄️ Vectorstore** (`src/vectorstore/store.py`) – speichert Chunks + Vektoren
  in Chroma, führt die Ähnlichkeitssuche durch
- **✨ Generator** (`src/llm/generator.py`) – erstellt aus Frage + gefundenem
  Kontext eine Antwort über die Gemini API, mit Fallback über mehrere Modelle
  bei Serverfehlern (503/429)
- **🔧 Backend** (`webapp/`) – Django-API mit einem Endpunkt (`/ask/`)
- **💻 Frontend** (`frontend/`) – eigenständige React-App (Vite), stellt Fragen
  per REST-Aufruf an das Backend

## 🚀 Setup

```bash
# Python-Abhängigkeiten
pip install -r requirements.txt

# Dokumente in data/ ablegen, dann einlesen
cd src/ingestion
python3 ingestall.py

# Backend starten
cd webapp
python3 manage.py runserver

# Frontend starten (separates Terminal)
cd frontend
npm install
npm run dev
```

## 🖼️ Demo
1.
![My Project Screenshot](<Screenshot 2026-09-13 at 17.42.37.png>)
2.
![My Project Screenshot](<Screenshot 2026-09-13 at 18.02.47.png>)



## 🤔 Warum RAG statt "alles ins Modell werfen"?

Bei ~5.000 Dokumenten übersteigt der Gesamttext das Kontextfenster jedes
LLMs bei Weitem. RAG reduziert den Kontext pro Anfrage auf die wenigen
tatsächlich relevanten Textabschnitte – das macht das System wirtschaftlich
und technisch praktikabel, statt bei jeder Anfrage den gesamten
Dokumentenbestand neu zu verarbeiten.

## 🔬 Erkenntnisse aus dem Testen

**✂️ Chunk-Größe & Overlap:** Ohne Overlap wurden zusammengehörige Informationen
(z. B. Name und ID in strukturierten Daten) an Chunk-Grenzen auseinandergerissen.

**🧬 Embedding-Modell:** Ein kleines, rein englisch trainiertes Modell
(`all-MiniLM-L6-v2`) lieferte bei gemischtsprachigen Anfragen ("... answer in
Russian") andere, teils falsche Ergebnisse als bei der reinen Frage. Der
Wechsel zu einem größeren, mehrsprachig trainierten Modell
(`paraphrase-multilingual-mpnet-base-v2`) verbesserte die Konsistenz,
löste das Problem aber nicht vollständig.

**🔍 Retrieval-Tiefe (top_k):** Mit `top_k=3` fehlte bei mehreren Testfragen der
Chunk mit der eigentlichen Antwort in den Ergebnissen, obwohl er im Dokument
vorhanden war. Eine Erhöhung auf `top_k=6` verbesserte die Trefferquote klar
messbar.

**❓ Offene Beobachtung:** Bei Anfragen, die Sprachanweisungen im selben Satz
wie die eigentliche Frage enthalten (z. B. "who was killer in Russian"),
fehlt der entscheidende Chunk teils auch bei höherem `top_k` weiterhin in den
Ergebnissen – unabhängig von der reinen Vektor-Ähnlichkeit zur Basisfrage.(Demo/1)
Das deutet darauf hin, dass zusätzliche Meta-Informationen im Anfragetext das
Retrieval stärker beeinflussen, als die Ähnlichkeitswerte allein vermuten
lassen. Ein sauberer nächster Schritt wäre, Sprachanweisungen und andere
Meta-Informationen vor dem Embedding von der eigentlichen Suchanfrage zu
trennen (Query-Cleaning), statt sie im selben Prompt zu vermischen.

## 🚧 Bewusste Grenzen / nicht umgesetzt

- 🖨️ Kein OCR für gescannte Dokumente oder Zeichnungen
- 🔐 Keine rollenbasierte Zugriffskontrolle (Login/Abteilungsrechte wurden
  probeweise umgesetzt, dann zugunsten der RAG-Kernfunktionalität wieder
  zurückgebaut)
- 💬 Kein persistenter Chatverlauf
- ☁️ Kein produktionsreifes Deployment (lokale Entwicklungsumgebung)
- 🧹 Automatisches Query-Cleaning vor dem Retrieval noch nicht umgesetzt

## 🧪 Testdaten

Da keine echten Firmendokumente vorlagen, wurden synthetische Testdaten
generiert (`generate_sample_data.py`): 20 fiktive Mitarbeiter (Excel) und
30 fiktive Kunden (CSV), ergänzt um einen frei verfügbaren Romantext als
Beispiel für unstrukturierten Fließtext.

## 🛠️ Tech-Stack

Python · sentence-transformers · ChromaDB · Google Gemini API · Django ·
React (Vite)

## ✍️ Autorin

Nurangez Qurbonova