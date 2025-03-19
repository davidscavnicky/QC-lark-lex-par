from typing import List, Tuple
import networkx as nx
from lark.tree import Tree
from lark.lexer import Token

def add_cnot_routing(statements: List[Tree], topology: nx.Graph) -> List[Tree]:
    """
    Add CNOT routing to the quantum circuit based on the given topology.

    Parameters:
    - statements: List of quantum gate statements (Tree objects).
    - topology: A NetworkX graph representing the hardware topology.

    Returns:
    - A new list of statements with CNOT routing applied.
    """
    routed_statements = []

    for statement in statements:
        if is_cnot(statement):
            control, target = get_cnot_qubits(statement)

            # Check if control and target are adjacent
            if not topology.has_edge(control, target):
                # Add SWAP gates to make control and target adjacent
                swap_sequence = route_cnot(control, target, topology)
                routed_statements.extend(swap_sequence)

            # Add the CNOT gate
            routed_statements.append(statement)
        else:
            # Add other gates as-is
            routed_statements.append(statement)

    return routed_statements


def is_cnot(statement: Tree) -> bool:
    """
    Check if a statement is a CNOT gate.
    """
    return (
        statement.data == 'qupdate' and
        isinstance(statement.children[0], Tree) and
        isinstance(statement.children[0].children[0], Token) and
        statement.children[0].children[0].value == 'CX'
    )


def get_cnot_qubits(statement: Tree) -> Tuple[int, int]:
    """
    Extract the control and target qubits from a CNOT statement.
    """
    _, lval_control, lval_target = statement.children
    control = int(lval_control.children[0].value) if isinstance(lval_control.children[0], Token) else None
    target = int(lval_target.children[0].value) if isinstance(lval_target.children[0], Token) else None

    if control is None or target is None:
        raise ValueError("Invalid CNOT statement: control or target qubit is missing or malformed.")
    return control, target


def route_cnot(control: int, target: int, topology: nx.Graph) -> List[Tree]:
    """
    Generate a sequence of SWAP gates to route the control and target qubits
    to be adjacent in the given topology.

    Parameters:
    - control: The control qubit index.
    - target: The target qubit index.
    - topology: A NetworkX graph representing the hardware topology.

    Returns:
    - A list of SWAP gate statements.
    """
    swap_sequence = []
    path = nx.shortest_path(topology, source=control, target=target)

    # Add SWAP gates along the path
    for i in range(len(path) - 1):
        swap_sequence.append(make_swap(path[i], path[i + 1]))

    return swap_sequence


def make_swap(q1: int, q2: int) -> Tree:
    """
    Create a SWAP gate statement for qubits q1 and q2.
    """
    gate = Tree(Token('RULE', 'gate'), [Token('SWAP', 'SWAP')])
    lval_q1 = Tree(Token('RULE', 'lval'), [Token('ID', str(q1))])
    lval_q2 = Tree(Token('RULE', 'lval'), [Token('ID', str(q2))])
    return Tree(Token('RULE', 'qupdate'), [gate, lval_q1, lval_q2])