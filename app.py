import os
from flask import Flask, request, jsonify
from google.generativeai import Client
from dotenv import load_dotenv

# Load environment variables from .env locally
load_dotenv()

app = Flask(__name__)

# Example: initialize Google Generative AI client
# Make sure you set your API key in .env as GOOGLE_API_KEY
client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# Example route
@app.route("/")
def home():
    return "Hello! Flask app is running on Render 🚀"

# Example route using generative AI
@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    # Example usage of Google Generative AI (adjust as needed)
    response = client.generate_text(model="text-bison-001", prompt=prompt)
    return jsonify({"result": response.text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT; fallback to 5000 locally
    app.run(host="0.0.0.0", port=port)
