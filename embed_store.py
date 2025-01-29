import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json

# Embedding and FAISS setup functions here
def load_chunks(input_path="processed_corpus.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_faiss_index(embeddings, dim):
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index

def save_faiss_index(index, output_path="faiss_index.bin"):
    faiss.write_index(index, output_path)

def load_faiss_index(input_path="faiss_index.bin"):
    return faiss.read_index(input_path)

def retrieve_top_k(query, model, index, text_mapping, k=3):
    query_embedding = model.encode([query], convert_to_tensor=False)
    distances, indices = index.search(np.array(query_embedding), k)
    return [text_mapping[idx] for idx in indices[0]]

# Example Usage
if __name__ == "__main__":
    # Load chunks
    chunks = load_chunks()
    text_mapping = {i: chunk for i, chunk in enumerate(chunks)}

    # Generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks, convert_to_tensor=False)

    # Create and save FAISS index
    index = create_faiss_index(embeddings, len(embeddings[0]))
    save_faiss_index(index)

    # Test retrieval
    query = "What is the architecture of a modern GPU?"
    top_k_chunks = retrieve_top_k(query, model, index, text_mapping)
    print("Top retrieved chunks:")
    for chunk in top_k_chunks:
        print(chunk)
