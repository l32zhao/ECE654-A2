import networkx as nx
import re

class ParityAnalyzer:
    def __init__(self):
        # Initialize an empty directed graph for CFG
        self.cfg = nx.DiGraph()
        # Lattice structure for parity
        self.lattice = {"Even": 0, "Odd": 1, "Top": 2}

    def build_cfg(self, code):
        """Manually parse the code and build a CFG using networkx."""
        lines = code.strip().split("\n")
        previous_node = None
        for i, line in enumerate(lines):
            line = line.strip()
            node_name = f"line_{i+1}"
            self.cfg.add_node(node_name, code=line)
            if previous_node:
                self.cfg.add_edge(previous_node, node_name)
            previous_node = node_name

    def analyze(self):
        """Perform even/odd analysis on the CFG."""
        variable_states = {}
        for node in nx.topological_sort(self.cfg):
            code = self.cfg.nodes[node]["code"]
            self._analyze_statement(code, variable_states)
        return variable_states

    def _analyze_statement(self, statement, variable_states):
        # Analyze assignment operations
        if "=" in statement:
            var, expr = statement.split("=")
            var, expr = var.strip(), expr.strip()
            # Check if expr is a digit
            if expr.isdigit():
                variable_states[var] = self._get_parity(int(expr))
            elif expr in variable_states:
                variable_states[var] = variable_states[expr]
            else:
                match = re.match(r"(\w+)\s*([\+\*])\s*(\w+)", expr)
                if match:
                    var1, op, var2 = match.groups()
                    parity1 = variable_states.get(var1, "Top")
                    parity2 = variable_states.get(var2, "Top")
                    if op == "+":
                        variable_states[var] = self._apply_addition(parity1, parity2)
                    elif op == "*":
                        variable_states[var] = self._apply_multiplication(parity1, parity2)
        print(f"Statement: {statement} - Variable States: {variable_states}")

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