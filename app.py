import os
from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

@app.route("/")
def home():
    return "Hello from GenAI!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    response = client.models.generate_content(
        model="gemini-2.5-flash",  # or whatever model you're using
        contents=prompt,
    )
    return jsonify({"text": response.text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
