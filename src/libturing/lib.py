from dataclasses import InitVar, dataclass, field
from os import truncate

from icecream import ic

# from icecream import ic


@dataclass
class TableEntry:
    state: str = ""
    repl: str = ""
    dire: str = ""

    def __str__(self) -> str:
        if self.state.strip():
            return f"'{self.state} {self.repl} {self.dire}'"
        return "''"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class StateRow:
    """
         var1 var2 var3 var4
    sta1 srd  srd  srd  srd
    sta2 srd  srd  srd  srd
    """

    currentState: str
    #              var   tableEntry
    variable: dict[str, TableEntry]

    def __repr__(self) -> str:
        return f"{self.variable}"

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class TransitionTable:
    rows: dict[str, StateRow] = field(default_factory=dict[str, StateRow])

    def __str__(self):
        return f"TransitionTable: {self.rows}"

    def parseFromJson(self, jsn: dict):
        states = list(jsn.keys())
        allvars = []
        for state in states:
            colums: dict[str, TableEntry] = {}
            for var in jsn[state].keys():
                allvars.append(var)
                print(f"{state}: {var}? ")
                try:
                    [nstate, repl, ndire] = jsn[state][var].__str__().split(" ")
                    move = TableEntry(state=nstate, repl=repl, dire=ndire)
                except ValueError:
                    move = TableEntry()
                    """ [nstate, repl, ndire] = ["", "", ""] """
                colums.update({var: move})
            self.rows.update({state: StateRow(state, variable=colums)})

        return set(states), set(allvars)

    def make_table(self, tableJson=None):
        if tableJson:
            return self.parseFromJson(tableJson)
        else:
            states = []
            vars = []
            while not vars and not states:

                vars = [
                    input(f"name of variable {i}: ")
                    for i in range(int(input("how many variables? ")))
                ]
                states = [
                    ("q" + str(i)) for i in range(int(input("how many states? ")))
                ]
            for state in states:
                colums: dict[str, TableEntry] = {}
                for var in vars:
                    print(f"{state}: {var}? ")
                    nstate = "q" + input("next state")
                    repl = input("next repl")
                    ndire = input("next dire")
                    move = TableEntry(state=nstate, repl=repl, dire=ndire)
                    colums.update({var: move})
                self.rows.update({state: StateRow(state, variable=colums)})

            return set(states), set(vars)

    def raw_table(self):
        return f"{self.rows}"


@dataclass
class TuringTape:
    tape: str = ""
    blankSymbol: str = field(default="*")
    pointer: int = field(default=0)

    right_padding: int = field(default=0)
    left_padding: int = field(default=0)

    def padd_tape(self):
        padd = self.blankSymbol * 2
        self.tape = padd + self.tape + padd

        self.right_padding += 2
        self.left_padding += 2

    def seek_left(self):
        if self.pointer <= 2:
            self.tape = self.blankSymbol + self.tape
            self.left_padding += 1
        else:
            self.pointer -= 1

    def seek_right(self):
        if self.pointer >= len(self.tape) - 2:
            self.tape = self.tape + self.blankSymbol
            self.right_padding += 1
        else:
            self.pointer += 1

    def currebt_symbol(self):
        return self.tape[self.pointer]


@dataclass
class TuringMachine:
    name: str
    vars: set[str] = field(default_factory=set, init=False)
    # TODO : make initial state a state variable
    # initialState: str = field(default_factory=str, init=False)
    states: set[str] = field(default_factory=set, init=False)
    transitionTable: TransitionTable = field(default_factory=TransitionTable)
    jsonTable: InitVar[dict[str, dict[str, str]] | None] = None
    tape: TuringTape = field(default_factory=TuringTape, init=True)

    def fromJson(self, jsonTable):
        self.states, self.vars = self.transitionTable.make_table(jsonTable)

    def set_tape(self, tape, blankSymbol="*"):
        self.tape = TuringTape(tape, blankSymbol=blankSymbol)
        self.tape.padd_tape()

    def run(self):
        active_state = "q0"

        while True:
            symbol = self.tape.currebt_symbol()
            ic(self.transitionTable.rows[active_state].variable[symbol])
            break
