from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/config", methods=["GET"])
def config():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
