# Report

* GitHub Repository: [Link to Repository](https://github.com/l32zhao/ECE654-A2)
* CI Executions: [Link to CI Executions](https://github.com/l32zhao/ECE654-A2/actions)

## CFG Tool
The networkx library provides robust graph-handling capabilities suitable for constructing and traversing custom CFGs. However, networkx does not provide support for CFGs out of the box, so the CFG will have to be implemented by hand and managed, which can be cumbersome for larger programs with control flow branches or loops.

## Description
1. **Lattice**: The lattice has three values: Even, Odd and Top. The definite states are Even and Odd and Top denotes an unknown state which is useful when the parity of the variables are undefined.
2. **Direction of Analysis**: The analysis is forward; it looks at each statement in sequence starting from the beginning of the program.
3. **May/Must Analysis**: This is a may analysis, since it keeps track of the potential but not necessarily actual parities after every operation without asserting absolute certainty.


### Abstract Operations
Addition:

* Even + Even = Even

* Odd + Odd = Even

* Even + Odd or Odd + Even = Odd

Multiplication:

* Odd * Odd = Odd

* Any other combination with Even results in Even.

### Analysis Result
The result of the analyze function now includes a list with detailed output, which comes as a tuple (line_number, code, variable_states) for each line of code. By this one will be able to fully comprehend the state of all the variables at any point in the program. An example of what would be returned when analyzing:
```python
# test_mixed_operations
code = """
        a = 3
        b = 6
        c = a + b
        d = a * b
        """
```
The output might look like this:
```
Analysis Result for test_mixed_operations:
('line_1', 'a = 3', {'a': 'Odd'})
('line_2', 'b = 6', {'a': 'Odd', 'b': 'Even'})
('line_3', 'c = a + b', {'a': 'Odd', 'b': 'Even', 'c': 'Odd'})
('line_4', 'd = a * b', {'a': 'Odd', 'b': 'Even', 'c': 'Odd', 'd': 'Even'})

```

## AST vs. CFG-Based Analysis
This analysis could easily be performed based on an Abstract Syntax Tree, but there are various trade-offs. CFG-based analysis makes the control flow explicit and is hence better suited for flow-sensitive analyses like this one, in which the state of variables evolves over time. AST-based analysis would probably be much faster but lacks explicit control-flow tracing, which may undermine its precision when dealing with complicated branching or loops.

For example:

* CFG gives the possibility to differentiate states of variables inside the body of a loop from those after it, thus fine grained updates can be specified.
* In an AST, capturing the state of variables along different control-flow paths can't be easily done without an explicit construction of flow-sensitive information, which would bring additional complication.

## Further Refinements
Perhaps we might be tracking the value ranges rather than just parity to refine the analysis. Say, we could know that a variable holds values from 0 to 10, which allows us to deduce certain properties.

## False Positives and False Negatives
In this context:

* False Positives: Cases where we make an incorrect inference about the parity of a variable. Example: We make an inference that some variable is Even though it could be Odd in branches of the program that have not been explored.

* False Negatives: These are situations where we would not be able to deduce a correct parity because of the limitations in CFG traversal. This could be when the analysis would use Top for values it cannot infer confidently, and in doing so, loses precision.