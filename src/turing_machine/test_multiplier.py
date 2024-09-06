import unittest

from main import TuringMachine

config = {
    "name": "copy",
    "InitialState": "q2",
    "BlankSymbol": "*",
    "FinalStates": ["H"],
    "TransitionTable": {
        "q0": {"0": "q1 0 R", "1": "q3 1 R"},
        "q1": {"*": "q2 * L", "1": "q1 1 R", "0": "q1 0 R"},
        "q2": {"0": "q3 a R", "1": "q5 b R", "*": "H * S"},
        "q3": {"0": "q3 0 R", "1": "q3 1 R", "*": "q4 * R"},
        "q4": {"0": "q4 0 R", "1": "q4 1 R", "*": "q7 1 L"},
        "q5": {"0": "q5 0 R", "1": "q5 1 R", "*": "q6 * R"},
        "q6": {"0": "q6 0 R", "1": "q6 1 R", "*": "q7 1 L"},
        "q7": {
            "0": "q7 0 L",
            "1": "q7 1 L",
            "*": "q7 * L",
            "a": "q2 0 L",
            "b": "q2 1 L",
        },
        "H": {"0": [], "1": [], "*": []},
    },
}

copy = {
    "name": "copy",
    "InitialState": "0",
    "BlankSymbol": "*",
    "FinalStates": ["9"],
    "TransitionTable": {
        "0": {
            "*": "9 * S",
            "0": "1 a R",
            "1": "5 b R",
        },
        "1": {
            "*": "2 * R",
            "0": "1 0 R",
            "1": "1 1 R",
        },
        "2": {
            "*": "3 0 L",
            "0": "2 0 R",
            "1": "2 1 R",
        },
        "3": {
            "*": "4 * L",
            "0": "3 0 L",
            "1": "3 1 L",
        },
        "4": {
            "a": "0 0 R",
            "0": "4 0 L",
            "1": "4 1 L",
        },
        "5": {
            "*": "6 * R",
            "0": "5 0 R",
            "1": "5 1 R",
        },
        "6": {
            "*": "7 1 L",
            "0": "6 0 R",
            "1": "6 1 R",
        },
        "7": {
            "*": "8 * L",
            "0": "7 0 L",
            "1": "7 1 L",
        },
        "8": {
            "b": "0 1 R",
            "0": "8 0 L",
            "1": "8 1 L",
        },
        "9": {0: None, 1: None, "a": None, "b": None, "*": None},
    },
}


class CopyStringTest(unittest.TestCase):

    def testCopyString(self):
        tm = TuringMachine(config=copy)
        tm.setTape("01001")
        try:
            print(tm.run(withLogs=True))
        except ValueError:
            self.fail
        self.assertEqual(tm.trim_tape(), "01001 01001")
