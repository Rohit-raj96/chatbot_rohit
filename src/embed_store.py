import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

def load_chunks(chunk_folder="chunks"):
    chunks = []
    for fname in sorted(os.listdir(chunk_folder)):
        with open(os.path.join(chunk_folder, fname), "r", encoding="utf-8") as f:
            chunks.append(f.read())
    return chunks

def embed_and_store(chunks, db_path="vectordb/faiss.index", model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    faiss.write_index(index, db_path)
    with open("vectordb/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

if __name__ == "__main__":
    chunks = load_chunks()
    embed_and_store(chunks)
    print(f"{len(chunks)} chunks embedded and stored in vectordb.")
