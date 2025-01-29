from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from api_handler import get_response  # Assuming get_response is your Llama API handler
from rag_chatbot import generate_answer_rag, load_faiss_index, load_text_chunks  # Importing your RAG functions
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# Configure MySQL (adjust with your credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:0603241622@localhost/chat_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Chat history model
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(10))  # 'user' or 'system'
    content = db.Column(db.Text)

# Initialize the database within the app context
with app.app_context():
    db.create_all()

# Load resources
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Embedding model
faiss_index = load_faiss_index("faiss_index.bin")  # FAISS index
text_mapping = load_text_chunks("/Users/basiljoy/my_project/processed_corpus.json")  # Text chunks

# Route to serve HTML page
@app.route('/')
def home():
    return render_template('index.html')  # Renders the index.html file from templates folder

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_query = data.get('query')

    if not user_query:
        return jsonify({"error": "Query not provided"}), 400

    # Run the RAG pipeline
    answer, retrieved_chunks = generate_answer_rag(
        query=user_query,
        model=get_response,  # Llama API handler function
        vector_db_index=faiss_index,
        embedding_model=embedding_model,
        text_mapping=text_mapping,
        k=3  # Retrieve top-3 relevant chunks
    )

    # Save the user query and system response to the database
    user_message = ChatHistory(role='user', content=user_query)
    system_message = ChatHistory(role='system', content=answer)

    db.session.add(user_message)
    db.session.add(system_message)
    db.session.commit()

    # Return the generated response
    return jsonify({
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    })

@app.route('/history', methods=['GET'])
def history():
    chat_history = ChatHistory.query.all()
    history_list = []
    for entry in chat_history:
        history_list.append({
            "id": entry.id,
            "timestamp": entry.timestamp,
            "role": entry.role,
            "content": entry.content
        })
    return jsonify(history_list)

if __name__ == '__main__':
    app.run(debug=True)
