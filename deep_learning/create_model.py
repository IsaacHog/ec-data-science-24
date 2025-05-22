import pandas as pd
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

df = pd.read_csv("context.csv")
texts = df["text"].dropna().tolist()

# Initialize sentence transformer model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Create vector representations
vectors = model.encode(texts)

# Create FAISS index
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors))

# Save everything to disk
np.save("vectors.npy", vectors)  # Save embeddings
faiss.write_index(index, "faiss_index.bin")  # Save FAISS index

# Save text data and model info
with open("texts.pkl", "wb") as f:
    pickle.dump(texts, f)

print("✅ Model embeddings, FAISS index, and text data have been saved successfully!")
