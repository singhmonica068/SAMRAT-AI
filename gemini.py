import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 🔹 Gemini API Key
genai.configure(api_key=os.getenv("AIzaSyC7vCjhEUTq5aLIVlNyT492wqvuflJHRM4"))  # Corrected the key name

# 🔹 Dctionary to store individual chat histories for each user
chat_histories = {}

def get_gemini_response(user_id, user_message):
    model = genai.GenerativeModel("gemini-2.0-flash")

    # 🔹 If the user history doesn't exist, create a new list
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    # 🔹 Update user chat history with the new message
    chat_histories[user_id].append(f"User: {user_message}")

    # 🔹 Retain only the last 5 messages (you can change this as needed)
    if len(chat_histories[user_id]) > 5:
        chat_histories[user_id].pop(0)

    # 🔹 Send the complete chat history to the AI model for context
    full_prompt = "\n\n" + "\n".join(chat_histories[user_id])

    try:
        response = model.generate_content(full_prompt)

        # 🔹 If the AI response is empty, handle it gracefully
        if not response.text:
            return "Sorry, I couldn't process your message. Please try again."

        # 🔹 Store the AI's response in the chat history
        chat_histories[user_id].append(f"AI: {response.text}")

        return response.text
    
    except Exception as e:
        return f"An error occurred while processing the message: {str(e)}"