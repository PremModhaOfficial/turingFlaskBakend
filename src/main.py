from flask import Flask, jsonify, request
from flask_cors import CORS
from icecream import ic

from libturing.lib import TuringMachine

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

TM = TuringMachine("batman")


@app.route("/api/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        data = request.json
        table = data["data"]
        for state, row in table.items():
            for var, entry in row.items():
                row[var] = f"{entry['m']} {entry['r']} {entry['d']}"
            table[state] = row
        TM.fromJson(table)
        ic(TM.transitionTable)
    if request.method == "GET":
        return jsonify({})
    return jsonify({})


@app.route("/api/run", methods=["GET", "POST"])
def runner():
    if request.method == "GET":
        # data = request.json
        # tape = data["data"]
        tape = "1001"
        ic(tape)
        TM.set_tape(tape)
        TM.run()
        ic(TM.transitionTable)
    if request.method == "GET":
        return jsonify(TM.transitionTable)
    return jsonify({})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
