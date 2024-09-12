from flask import Flask, jsonify, request
from flask_cors import CORS

from turing_machine.turing import TuringMachine

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        data = request.json
        print(data)
        return jsonify(data)
    return jsonify({})


if __name__ == "__main__":
    app.run(debug=True, port=8000)


def interCepter(config):
    return TuringMachine(config)
