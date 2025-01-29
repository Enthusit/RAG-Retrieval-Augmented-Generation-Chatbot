# RAG-Retrieval-Augmented-Generation-Chatbot

# RAG Chatbot  

This project implements a Retrieval-Augmented Generation (RAG) chatbot using a vector database for semantic search and a MySQL database for storing chat history. The chatbot is served via a Flask API.  

## Features  
- **Retrieval-Augmented Generation (RAG)**: Uses vector search to retrieve relevant text chunks before generating responses.  
- **Semantic Search**: Embeds text chunks using `sentence-transformers` and stores them in a FAISS vector database.  
- **Flask API**: Provides endpoints for chatting and retrieving chat history.  
- **MySQL Database**: Stores chat history with timestamps and user roles.  

---

## Install Dependencies
pip install -r requirements.txt

#Set Up MySQL Database
Create a MySQL database:

CREATE DATABASE chat_db;
USE chat_db;
Create the chat history table:

CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(10),  -- 'user' or 'system'
    content TEXT
);
Update app.py with your MySQL credentials:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:PASSWORD@localhost/chat_db'
Running the Chatbot
#Start the Flask API

python app.py
Flask will run on http://127.0.0.1:5000/.

## Open the Chat Interface
Open http://127.0.0.1:5000/ in your browser.
Enter a query and click "Send" to chat with the bot.
API Endpoints
1. Chat with the Bot
Endpoint:

{
    "query": "What is GPU?"
}
Response (JSON):

{
    "answer": "GPU is a ...",
    "retrieved_chunks": ["Chunk 1 text...", "Chunk 2 text...", "Chunk 3 text..."]
}
2. Get Chat History
Endpoint:
GET /history
Response (JSON):

json
Copy
Edit
[
    {
        "id": 1,
        "timestamp": "2024-01-29T12:34:56",
        "role": "user",
        "content": "What is RAG?"
    },
    {
        "id": 2,
        "timestamp": "2024-01-29T12:34:57",
        "role": "system",
        "content": "RAG stands for Retrieval-Augmented Generation..."
    }
]
Testing
1. Run Unit Tests

pytest tests/
2. Test API Endpoints with cURL
Send a chat query
bash
Copy
Edit
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"query": "What is RAG?"}'
Fetch chat history

curl -X GET http://127.0.0.1:5000/history
Environment Variables
Create a .env file (optional) for your database credentials:

DB_USER=root  
DB_PASSWORD=yourpassword  
DB_HOST=localhost  
DB_NAME=chat_db  

## File Structure

rag-chatbot/
│── app.py                  # Flask API  
│── api_handler.py          # Handles LLM responses  
│── rag_chatbot.py          # RAG retrieval functions  
│── requirements.txt        # Python dependencies  
│── templates/  
│   └── index.html          # Chat UI  
│── static/                 # (Optional: for CSS/JS files)  
│── tests/                  # Unit tests  
└── README.md               # Project documentation  

## Future Improvements
User Authentication: Add user authentication for personalized history.
Deploy on Cloud: Host the chatbot on AWS/GCP/Azure.
Improve Answer Generation: Use a more powerful LLM model.

