import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from api_handler import get_response  # Importing your Llama API handler


def generate_answer_rag(query, model, vector_db_index, embedding_model, text_mapping, k=3):

    # Step 1: Convert the query to an embedding
    query_embedding = embedding_model.encode([query], convert_to_tensor=False)

    # Step 2: Retrieve top-k relevant chunks
    distances, indices = vector_db_index.search(np.array(query_embedding), k)
    retrieved_chunks = [text_mapping[idx] for idx in indices[0]]

    # Step 3: Concatenate the retrieved chunks
    context = " ".join(retrieved_chunks)

    # Step 4: Generate the answer using the context and query
    prompt = f"""
    Context: {context}
    
    Question: {query}
    
    Answer the question using the given context. Be concise and clear.
    """
    answer = model(prompt)  # Calls your LLM (e.g., Llama API or local model)
    
    return answer, retrieved_chunks


def load_faiss_index(index_path):

    return faiss.read_index(index_path)


def load_text_chunks(json_path):

    with open(json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return {i: chunk for i, chunk in enumerate(chunks)}



if __name__ == "__main__":
    # Load resources
    print("Loading resources...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Embedding model
    faiss_index = load_faiss_index("faiss_index.bin")  # FAISS index
    text_mapping = load_text_chunks("/Users/basiljoy/my_project/processed_corpus.json")  # Text chunks

    print("Resources loaded. Ready to process queries.")

    # Example query
    query = "Explain the concept of SIMT in CUDA architecture."

    # Run the RAG pipeline
    answer, retrieved_chunks = generate_answer_rag(
        query=query,
        model=get_response,  # Llama API handler function
        vector_db_index=faiss_index,
        embedding_model=embedding_model,
        text_mapping=text_mapping,
        k=3  # Retrieve top-3 relevant chunks
    )

    # Display results
    print("\nUser Query:")
    print(query)

    print("\nTop Retrieved Chunks:")
    for i, chunk in enumerate(retrieved_chunks, 1):
        print(f"{i}: {chunk}\n")

    print("\nGenerated Answer:")
    print(answer)
