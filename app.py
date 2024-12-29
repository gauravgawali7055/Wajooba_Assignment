import sqlite3
import openai
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()
def init_db():
    # Connect to SQLite database (it will create the database file if it doesn't exist)
    conn = sqlite3.connect("faq_system.db")
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # SQL command to create the 'logs' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each entry
        question TEXT,                         -- User's question
        response TEXT,                         -- ChatGPT's response
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP -- Timestamp of entry
    )
    """)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database initialized successfully!")
# Get user input
def get_user_input():
    question = input("Enter your question (or type 'exit' to quit): ")
    return question

# Get ChatGPT response
openai.api_key = os.getenv("OPENAI_API_KEY") 
 # Replace with your OpenAI API key. 
 #  The API key requires a valid OpenAI account with a paid subscription for usage.

def get_chatgpt_response(question):
    try:
        response = openai.Completion.create(
            engine="gpt-4o-mini",
            prompt=f"You are a support assistant. Answer the following question in one paragraph: {question}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error while fetching response from ChatGPT: {e}")
        return "Sorry, I couldn't process your query at the moment."

# Log data to the database
def log_to_database(question, response):
    try:
        conn = sqlite3.connect("faq_system.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (question, response) VALUES (?, ?)", (question, response))
        conn.commit()
        conn.close()
        print("Data logged successfully!")
    except Exception as e:
        print(f"Error while logging data to the database: {e}")

# Main execution
if __name__ == "__main__":
    init_db()
    
    while True:
        user_question = get_user_input()
        if user_question.lower() == "exit":
            print("Exiting the FAQ system. Goodbye!")
            break
        
        chatgpt_response = get_chatgpt_response(user_question)
        print(f"ChatGPT's Response: {chatgpt_response}")
        log_to_database(user_question, chatgpt_response)
