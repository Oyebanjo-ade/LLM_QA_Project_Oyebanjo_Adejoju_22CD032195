import os
from flask import Flask, request, jsonify, render_template_string
from google import genai  # Make sure requirements.txt has 'google-genai'

app = Flask(__name__)

# Initialize Google GenAI client with API key from environment variable
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# ----------------- ROUTES -----------------

@app.route("/")
def home():
    return "Hello from GenAI!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or request.form  # Handle JSON or form submissions
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Generate text with Google GenAI
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # Use the model of your choice
        contents=prompt,
    )
    return jsonify({"text": response.text})

@app.route("/chat", methods=["GET", "POST"])
def chat():
    result = ""
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        if prompt:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            result = response.text

    # Simple HTML form
    html = f"""
    <h1>Chat with GenAI</h1>
    <form method="post">
        <input name="prompt" placeholder="Type your prompt here" style="width:300px;">
        <button type="submit">Generate</button>
    </form>
    <p><b>Result:</b> {result}</p>
    """
    return render_template_string(html)

# ----------------- RUN -----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets this automatically
    app.run(host="0.0.0.0", port=port)
