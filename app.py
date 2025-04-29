from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Gemini API Key
GEMINI_API_KEY = "AIzaSyAml0YC6FFqknq1eMVi6IZ8ehG-H9bAdf4"

# Gemini API Function
def get_gemini_response(user_input):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_input}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, params=params)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {str(e)}"

# Routes
@app.route("/")
def home():
    return "Welcome to Gemini API! Use /chat?message=your_message"

@app.route("/chat", methods=["GET"])
def chat():
    user_message = request.args.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    reply = get_gemini_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)