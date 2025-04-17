from flask import Flask, request, jsonify
from oda_ai import get_response  # Make sure this is correct
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    reply = get_response(message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
