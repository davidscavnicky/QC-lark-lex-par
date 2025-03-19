import networkx as nx
from lark.tree import Tree
from lark.lexer import Token
from typing import Any
from cnotrouting import add_cnot_routing


# Define a linear topology
topology: nx.Graph = nx.Graph()
topology.add_edges_from([(0, 1), (1, 2), (2, 3)])


# Example circuit with a non-adjacent CNOT gate
statements = [
    Tree[Any](Token('RULE', 'qupdate'), [
        Tree[Any](Token('RULE', 'gate'), [Token('CX', 'CX')]),
        Tree[Any](Token('RULE', 'lval'), [Token('ID', '0')]),  # Control qubit
        Tree[Any](Token('RULE', 'lval'), [Token('ID', '3')])   # Target qubit
    ])
]
# Apply CNOT routing
routed_statements = add_cnot_routing(statements, topology)

# Print the routed circuit
for stmt in routed_statements:
    print(stmt.pretty())