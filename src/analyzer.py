from pycfg import CFGBuilder

class ParityAnalyzer:
    def __init__(self):
        # Lattice structure for each variable
        self.lattice = {"Even": 0, "Odd": 1, "Top": 2}

    def analyze(self, code):
        # Build CFG for the input code
        cfg = CFGBuilder().build_from_src("test", code)
        variable_states = {}
        # Traverse CFG nodes
        for block in cfg:
            for statement in block.statements:
                # Analyze each statement
                self._analyze_statement(statement, variable_states)
        return variable_states

    def _analyze_statement(self, statement, variable_states):
        # Analyzing assignments and updating lattice state
        if "=" in statement:
            var, expr = statement.split("=")
            var, expr = var.strip(), expr.strip()
            if expr.isdigit():
                variable_states[var] = self._get_parity(int(expr))
            elif expr in variable_states:
                variable_states[var] = variable_states[expr]

    def _get_parity(self, value):
        return "Even" if value % 2 == 0 else "Odd"

    def _apply_addition(self, parity1, parity2):
        if parity1 == "Even" and parity2 == "Even":
            return "Even"
        elif parity1 == "Odd" and parity2 == "Odd":
            return "Even"
        else:
            return "Odd"

    def _apply_multiplication(self, parity1, parity2):
        if parity1 == "Odd" and parity2 == "Odd":
            return "Odd"
        return "Even"
