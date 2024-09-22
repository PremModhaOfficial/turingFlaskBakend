import unittest

from lib import TransitionTable


class TableTest(unittest.TestCase):

    def test_from_dict(self):
        conf = {
            "q0": {"a": "qo o o", "b": "qo o o"},
            "q1": {"a": "qo o o", "b": "qo o o"},
        }

        t = TransitionTable()
        t.make_table(conf)
        print(t.raw_table())
        print(str(conf))
        self.assertEqual(t.raw_table(), str(conf))

    def test_stress(self):
        conf = {
            "q0": {"0": "q0 1 R", "1": "q0 0 R", "*": "q1 * L"},
            "q1": {"0": "q1 0 L", "1": "q1 1 L", "*": "q2 * R"},
            "q2": {"0": "", "1": "", "*": ""},
        }

        t = TransitionTable()
        t.make_table(conf)
        print(t.raw_table())
        print(str(conf))
        self.assertEqual(t.raw_table(), str(conf))
