import unittest

from lib import TuringMachine


class TableTest(unittest.TestCase):

    def test_stress_selfs(self):
        conf = {
            "q0": {"0": "q0 1 R", "1": "q0 0 R", "*": "q1 * L"},
            "q1": {"0": "q1 0 L", "1": "q1 1 L", "*": "q2 * R"},
            "q2": {"0": "", "1": "", "*": ""},
        }

        t1 = TuringMachine("1")
        t2 = TuringMachine("2")

        t1.transitionTable.make_table(conf)
        t2.transitionTable.make_table(conf)

        t2.set_tape("001100")
        t1.set_tape("001100")

        print(t2.run())
        print(t1.run())
        self.assertTrue(t1.run() == t2.run())
