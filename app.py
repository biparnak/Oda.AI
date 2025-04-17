from flask import Flask, request, jsonify
from chatbot import get_response  # Your chatbot logic

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    reply = get_response(message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
