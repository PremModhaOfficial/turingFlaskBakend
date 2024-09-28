from typing import Any, Dict

from flask import Flask, jsonify, request
from flask_cors import CORS
from icecream import ic

from libturing.lib import TuringMachine


class State:
    def __init__(self):
        self.tm = TuringMachine("batman")
        self.name = "batman"
        self.transitionTable = self.tm.transitionTable
        self.tape = self.tm.tape

    def run(self):
        return self.tm.run()

    def set_tape(self):
        return self.tm.set_tape

    def set_blank(self, blank: str):
        self.tm.tape.change_blank(blank)

    def fromJson(self, table: Dict[str, Any]):
        self.tm.fromJson(table)

    def __str__(self):
        return f"{self.tm.name} {self.tm.transitionTable}"


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

TM = State()
BLANK = "*"
TAPE = "10101"

COMTM = TuringMachine("complement")
COMTM.fromJson(
    {
        "q0": {"0": "q0 1 R", "1": "q0 0 R", "*": "q1 * S"},
        "q1": {"0": "", "1": "", "*": ""},
    }
)


def validate_json_input(json_data: Dict[str, Any], required_fields: list) -> bool:
    return all(field in json_data for field in required_fields)


@app.route("/api/name/", methods=["GET", "POST"])
def name():
    if request.method == "POST":
        if not request.json or not validate_json_input(request.json, ["name"]):
            return jsonify({"error": "Invalid input"}), 400
        TM.name = request.json["name"]
        return jsonify({"message": "Name updated successfully"}), 200
    return jsonify({"name": TM.name})


@app.route("/api/blank/", methods=["GET", "POST"])
def blank():
    global BLANK
    if request.method == "POST":
        if not request.json or not validate_json_input(request.json, ["blank"]):
            return jsonify({"error": "Invalid input"}), 400
        BLANK = request.json["blank"]
        return jsonify({"message": "Blank symbol updated successfully"}), 200
    return jsonify({"blank": BLANK})


def serialize_table(
    table: Dict[str, Dict[str, str]]
) -> Dict[str, Dict[str, Dict[str, str]]]:
    serialized = {}
    for state, row in table.items():
        serialized[state] = {}
        for var, entry in row.items():
            m, r, d = entry.split()
            serialized[state][var] = {"m": m, "r": r, "d": d}
    return serialized


def deserialize_table(
    table: Dict[str, Dict[str, Dict[str, str]]]
) -> Dict[str, Dict[str, str]]:
    deserialized = {}
    for state, row in table.items():
        deserialized[state] = {}
        for var, entry in row.items():
            deserialized[state][var] = f"{entry['m']} {entry['r']} {entry['d']}"
    return deserialized


@app.route("/api/config/", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        if not request.json or not validate_json_input(request.json, ["table"]):
            return jsonify({"error": "Invalid input"}), 400
        table = deserialize_table(request.json["table"])
        TM.fromJson(table)
        return jsonify({"message": "Configuration updated successfully"}), 200
    return jsonify(TM.transitionTable)


dummytt = {
    "q0": {"0": "q0 0 L", "1": "q0 1 L", "*": "q1 * R"},
    "q1": {"0": "q1 1 R", "1": "q1 0 R", "*": "q2 * S"},
    "q2": {"0": "", "1": "", "*": ""},
}


@app.route("/api/run/", methods=["GET"])
def runner():
    TM.fromJson(dummytt)
    TM.set_tape()(TAPE)
    res = TM.run()
    ic(res)
    return jsonify(res)


@app.route("/api/tape/", methods=["GET", "POST"])
def set_tape():
    if request.method == "POST":
        if not request.json or not validate_json_input(request.json, ["tape"]):
            return jsonify({"error": "Invalid input"}), 400
        TM.set_tape()(request.json["tape"], blankSymbol=BLANK)
        return jsonify({"message": "Tape updated successfully"}), 200
    return jsonify({"tape": str(TM.tape)})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
