# self.blank: str = config["BlankSymbol"]
# self.transitionTable = config["TransitionTable"]


class State:
    def __init__(self, name: str) -> None:
        self.name = name


class Move:
    def __init__(self, state: State, repl: str, dire: str) -> None:
        self.state = state
        self.repl = repl
        self.dire = dire

    def __repr__(self):
        return self.normalize()

    def __str__(self) -> str:
        return self.__repr__()

    def normalize(self):
        return f"{self.state} {self.repl} {self.dire}"


class TrabsitionTable:
    def __init__(self, table: dict[State, Move]) -> None:
        self.table = table

    def normalize(self):
        return dict(
            map(
                lambda state: (state[0], state[1].normalize()),
                self.table.items(),
            )
        )


class TuringConfig:
    def __init__(
        self,
        name: str,
        initialState: str,
        blankSymbol: str,
        finalStates: list[str],
        transitionTable: TrabsitionTable,
    ) -> None:
        self.name = name
        self.initialState = initialState
        self.blankSymbol = blankSymbol
        self.finalStates = finalStates
        self.transitionTable = transitionTable.normalize()
