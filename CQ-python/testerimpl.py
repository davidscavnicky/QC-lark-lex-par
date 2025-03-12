from lark.tree import Tree
from lark.lexer import Token
import numpy as np
from singlequbittosequence import decompose_single_qubit_gate, decompose_controlled_gate, PE_gate

# Example usage:
# Decompose a Hadamard gate on qubit 0
decomposed_gates = decompose_single_qubit_gate('H', 0)
print(decomposed_gates)

# Decompose a controlled-X gate with control qubit 0 and target qubit 1
decomposed_controlled_gates = decompose_controlled_gate(0, 1, 'X')
print(decomposed_controlled_gates)

# Test PE_gate functionpyt
g1 = Tree('gate', [Token('NOT', 'X'), Token('ID', 'q0')])
env1 = [{}]
print(PE_gate(g1, env1))

g2 = Tree('gate', [Token('H', 'H'), Token('ID', 'q0')])
env2 = [{}]
print(PE_gate(g2, env2))

g3 = Tree('gate', [Tree('qupdate', [Token('gate', 'H'), Tree('lval', [Token('ID', 'q0')])]), Token('IF', 'if'), Tree('lval', [Token('ID', 'c')])])
env3 = [{'c': 1}]
print(PE_gate(g3, env3))