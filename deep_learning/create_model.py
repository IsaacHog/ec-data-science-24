import pandas as pd
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

df = pd.read_csv("context.csv") # pandas läsin csv fil
texts = df["text"].dropna().tolist() # ta bort tomma rader och gör om till lista

model = SentenceTransformer("paraphrase-MiniLM-L6-v2") # modell för att läsa in subtitles (klassifiecring osv)
vectors = model.encode(texts)

# skapa Faiss index, effektiviserar sökningen. Förstår inte helt hur "vekteringen" fungerar
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors))

# Spara ned resultaten
np.save("vectors.npy", vectors)
faiss.write_index(index, "faiss_index.bin")

# lägg in texts i filen texts.pkl (create och write är ju två olika saker)
with open("texts.pkl", "wb") as f:
    pickle.dump(texts, f)
