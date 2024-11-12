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
        """Perform even/odd analysis on the CFG and collect results for each line."""
        variable_states = {}
        analysis_report = []
        for node in nx.topological_sort(self.cfg):
            code = self.cfg.nodes[node]["code"]
            result = self._analyze_statement(code, variable_states)
            # Store the results after each statement
            analysis_report.append((node, code, result.copy()))
        return analysis_report

    def _analyze_statement(self, statement, variable_states):
        if "=" in statement:
            var, expr = statement.split("=")
            var, expr = var.strip(), expr.strip()
            
            # Check if expr is a digit (constant)
            if expr.isdigit():
                variable_states[var] = self._get_parity(int(expr))
            # If expr is a variable directly, assign its parity
            elif expr in variable_states:
                variable_states[var] = variable_states[expr]
            else:
                # Regex to match simple binary expressions
                match = re.match(r"(\w+)\s*([\+\*])\s*(\w+|\d+)", expr)
                if match:
                    var1, op, var2 = match.groups()

                    # Determine the parity of var1 and var2 (either from variable states or constants)
                    parity1 = variable_states.get(var1, "Top") if not var1.isdigit() else self._get_parity(int(var1))
                    parity2 = variable_states.get(var2, "Top") if not var2.isdigit() else self._get_parity(int(var2))

                    # Apply the operation and update variable state
                    if op == "+":
                        variable_states[var] = self._apply_addition(parity1, parity2)
                    elif op == "*":
                        variable_states[var] = self._apply_multiplication(parity1, parity2)
        
        return variable_states

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
