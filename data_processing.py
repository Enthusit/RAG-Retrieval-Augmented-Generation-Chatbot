import os
from PyPDF2 import PdfReader
from docx import Document

def load_documents(folder_path):
    corpus = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                corpus.append(file.read())
        elif filename.endswith('.pdf'):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            corpus.append(text)
        elif filename.endswith('.docx'):
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            corpus.append(text)
    return corpus

# Example usage
folder_path = "/Users/basiljoy/my_project/dc"  # Replace with your folder name
documents = load_documents(folder_path)
print(f"Loaded {len(documents)} documents.")

import re
from nltk.tokenize import sent_tokenize
import nltk

#nltk.download('punkt_tab')  # Download NLTK tokenizer if not already done

def clean_text(text):
    # Remove unwanted characters and extra spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    return text.strip()

def chunk_text(text, max_length=300):
    # Tokenize text into sentences
    sentences = sent_tokenize(text)
    chunks, current_chunk = [], ""

    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) > max_length:
            chunks.append(current_chunk)
            current_chunk = sentence  # Start a new chunk
        else:
            current_chunk += " " + sentence

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Process all documents
all_chunks = []
for doc in documents:
    cleaned_text = clean_text(doc)
    chunks = chunk_text(cleaned_text)
    all_chunks.extend(chunks)

print(f"Total chunks created: {len(all_chunks)}")


with open("processed_corpus.txt", "w", encoding="utf-8") as f:
    for chunk in all_chunks:
        f.write(chunk + "\n\n")

import json

with open("processed_corpus.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f)
