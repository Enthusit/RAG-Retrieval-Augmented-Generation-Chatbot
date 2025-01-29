import unittest
from app import app, db, ChatHistory  # Import app and db from your app

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        # Set up the application context for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:0603241622@localhost/chat_db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        with app.app_context():
            # Clear the database before each test
            db.create_all()  # Create the tables
            db.session.query(ChatHistory).delete()  # Clear existing chat history
            db.session.commit()  # Commit the transaction

    def test_chat(self):
        # Your test code for the /chat endpoint
        pass

    def test_history(self):
        # Your test code for the /history endpoint
        pass

if __name__ == '__main__':
    unittest.main()
