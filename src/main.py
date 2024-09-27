from flask import Flask, jsonify, request
from flask_cors import CORS
from icecream import ic

from libturing.lib import TuringMachine

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

TM = TuringMachine("batman")


class BLANK:

    def __init__(self, blank="*"):
        self.symbol = blank


@app.route("/api/name", methods=["GET", "POST"])
def name():
    if request.method == "POST":
        TM.name = request.json["name"] or "Not Set"
    if request.method == "GET":
        return jsonify({"name": TM.name})
    return jsonify({})


@app.route("/api/blank", methods=["GET", "POST"])
def blank():
    if request.method == "POST":
        BLANK = request.json["blank"] or BLANK
        ic(request.json)
    if request.method == "GET":
        return jsonify({"blank": BLANK or "*"})
    return jsonify({})


@app.route("/api/transitionTable", methods=["GET", "POST"])
def transiTiontable():
    if request.method == "POST":
        data = request.json
        ic(data)
        table = data["table"]
        for state, row in table.items():
            for var, entry in row.items():
                row[var] = f"{entry['m']} {entry['r']} {entry['d']}"
            table[state] = row
        TM.fromJson(table)
        ic(TM.transitionTable)
    if request.method == "GET":
        return jsonify(TM.transitionTable)
    return jsonify({})


@app.route("/api/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        data = request.json
        ic(data)
        table = data["table"]
        for state, row in table.items():
            for var, entry in row.items():
                row[var] = f"{entry['m']} {entry['r']} {entry['d']}"
            table[state] = row
        TM.fromJson(table)
        ic(TM.transitionTable)
    if request.method == "GET":
        return jsonify({})
    return jsonify({})


dummytt = (
    {
        "q0": {"0": "q0 1 R", "1": "q0 0 R", "*": "q1 * L"},
        "q1": {"0": "q1 0 L", "1": "q1 1 L", "*": "q2 * S"},
        "q2": {"0": "", "1": "", "*": ""},
    },
)


@app.route("/api/run", methods=["GET", "POST"])
def runner():
    if request.method == "POST":
        # data = request.json
        # tape = data["data"]
        tape = "1001"
        ic(tape)
        TM.fromJson(dummytt[0])
        TM.set_tape(tape)
        TM.run()
        # ic(TM.transitionTable)
        ic(TM.log)
        return jsonify(TM.log)
    if request.method == "GET":
        return jsonify(TM.log)
    return jsonify({})


@app.route("/api/set_tape", methods=["GET", "POST"])
def set_tape():
    if request.method == "POST":
        TM.set_tape(request.json["tape"], blankSymbol=BLANK)
    if request.method == "POST":
        return jsonify(TM.tape)
    return jsonify({})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
