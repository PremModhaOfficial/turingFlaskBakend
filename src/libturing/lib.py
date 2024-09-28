from dataclasses import InitVar, dataclass, field


@dataclass
class TableEntry:
    state: str = ""
    repl: str = ""
    dire: str = ""

    def __str__(self) -> str:
        if self.state.strip():
            return f"{self.state} {self.repl} {self.dire}"
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

    def get_entry(self, state: str, var: str):
        return f"{self.rows[state].variable[var]}".split(" ")

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
    tape: list[str] = field(default_factory=list)
    blankSymbol: str = field(default="*")
    pointer: int = field(default=2)
    accepted: bool = field(default=False, init=False)

    right_padding: int = field(default=0)
    left_padding: int = field(default=0)

    def exec(self, repl, move):
        self.tape[self.pointer] = repl
        if move == "R":
            self.seek_right()
            return True
        if move == "L":
            self.seek_left()
            return True
        if move == "S":
            return False

    def change_blank(self, new_blank):
        self.tape = [new_blank if x == self.blankSymbol else x for x in self.tape]
        self.blankSymbol = new_blank

    def padd_tape(self):
        padd = list(self.blankSymbol * 2)
        temp = []
        temp.extend(padd)
        temp.extend(self.tape)
        temp.extend(padd)

        self.tape = temp
        del temp

        self.right_padding += 2
        self.left_padding += 2

    def seek_left(self):
        if self.pointer <= 2:

            temp = self.tape
            self.tape = [self.blankSymbol]
            self.tape.extend(temp)
            del temp
            self.left_padding += 1
        else:
            self.pointer -= 1

    def seek_right(self):
        if self.pointer >= len(self.tape) - 2:
            self.tape.append(self.blankSymbol)
            self.right_padding += 1
        else:
            self.pointer += 1

    def current_symbol(self):
        try:
            return self.tape[self.pointer]
        except Exception as e:
            print(e)
            return self.blankSymbol

    def set_blank(self, blank):
        self.blankSymbol = blank
        if len(self.tape) > 0:
            self.change_blank(blank)


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
    log: list[str] = field(default_factory=list, init=False)
    final_states: set[str] = field(default_factory=set, init=False)

    def fromJson(self, jsonTable):
        self.states, self.vars = self.transitionTable.make_table(jsonTable)

    def set_tape(self, tape: str, blankSymbol="*"):
        self.tape = TuringTape(list(tape), blankSymbol=blankSymbol)
        self.tape.padd_tape()

    def logg(self, active_state):
        if not self.log:
            self.log = []

        log = f"{active_state}:{self.tape.tape}:{self.tape.pointer}"
        self.log.append(log)

    def run(self):
        self.log = []
        active_state = "q0"

        # self.logg(active_state)
        isRunning = True
        while isRunning:
            # ic(active_state)
            symbol = self.tape.current_symbol()
            try:
                active_state, repl, move = self.transitionTable.get_entry(
                    active_state, symbol
                )
                self.logg(active_state)
            except ValueError:
                break
            except KeyError:
                break
            except IndexError:
                break
            isRunning = self.tape.exec(repl, move)

            # break
        self.tape.accepted = not isRunning
        return self.log, not isRunning
