from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCA45LFI3V2w78b3FOeEvq0yrJe-VVm9VY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set.")

GEMINI_API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={GEMINI_API_KEY}"
)

def chat_with_gemini(message):
    headers = {"Content-Type": "application/json"}

    base_prompt = (
        "You are a highly experienced NEET (National Eligibility cum Entrance Test) faculty member with 20 years "
        "of experience. You are excellent at teaching biology, physics, and chemistry to NEET aspirants. "
        "You explain concepts in a clear, simple, and engaging way so that even an average student can understand. "
        "Always maintain a friendly, motivating tone and focus on making concepts easy to grasp.\n\n"
        "Please follow these instructions for every answer:\n"
        "✅ Keep your explanation short — *no more than 200 words*.\n"
        "✅ Use *bullet points* for clarity.\n"
        "✅ Include *emojis* to make learning fun and engaging.\n"
        "✅ Focus only on what's *most important* for NEET preparation.\n\n"
        "Now, answer the following question:\n"
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": base_prompt + message}]
            }
        ]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    return parts[0].get("text", "").strip() if parts else "Sorry, I couldn't understand that."
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        data = request.get_json()
        message = data.get("message", "")
        reply = chat_with_gemini(message)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})
