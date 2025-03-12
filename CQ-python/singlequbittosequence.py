import numpy as np
from copy import deepcopy
from flatten import *

def decompose_single_qubit_gate(gate, target):
    """
    Decompose a single-qubit gate into a sequence of elementary gates.
    
    Parameters:
    gate (str): The name of the single-qubit gate (e.g., 'H', 'T', 'S', etc.).
    target (int): The target qubit index.
    
    Returns:
    list: A list of tuples representing the sequence of elementary gates.
    """
    elementary_gates = []
    
    if gate == 'H':
        # Hadamard gate decomposition: H = RZ(pi/2) * SX * RZ(pi/2)
        elementary_gates.append(('RZ', target, np.pi / 2))
        elementary_gates.append(('SX', target))
        elementary_gates.append(('RZ', target, np.pi / 2))
    
    elif gate == 'T':
        # T gate decomposition: T = RZ(pi/4)
        elementary_gates.append(('RZ', target, np.pi / 4))
    
    elif gate == 'S':
        # S gate decomposition: S = RZ(pi/2)
        elementary_gates.append(('RZ', target, np.pi / 2))
    
    elif gate == 'X':
        # X gate is already an elementary gate
        elementary_gates.append(('X', target))
    
    elif gate == 'Y':
        # Y gate decomposition: Y = RZ(pi/2) * X * RZ(pi/2)
        elementary_gates.append(('RZ', target, np.pi / 2))
        elementary_gates.append(('X', target))
        elementary_gates.append(('RZ', target, np.pi / 2))
    
    elif gate == 'Z':
        # Z gate decomposition: Z = RZ(pi)
        elementary_gates.append(('RZ', target, np.pi))
    
    elif gate == 'SX':
        # SX gate is already an elementary gate
        elementary_gates.append(('SX', target))
    
    else:
        raise ValueError(f"Unsupported gate: {gate}")
    
    return elementary_gates

def decompose_controlled_gate(control, target, gate):
    """
    Decompose a controlled gate into a sequence of elementary gates.
    
    Parameters:
    control (int): The control qubit index.
    target (int): The target qubit index.
    gate (str): The name of the single-qubit gate (e.g., 'X', 'H', etc.).
    
    Returns:
    list: A list of tuples representing the sequence of elementary gates.
    """
    elementary_gates = []
    
    if gate == 'X':
        # Controlled-X (CX) gate is already an elementary gate
        elementary_gates.append(('CX', control, target))
    
    elif gate == 'H':
        # Controlled-H gate decomposition
        elementary_gates.extend(decompose_single_qubit_gate('H', target))
        elementary_gates.append(('CX', control, target))
        elementary_gates.extend(decompose_single_qubit_gate('H', target))
    
    elif gate == 'T':
        # Controlled-T gate decomposition
        elementary_gates.append(('RZ', target, np.pi / 4))
        elementary_gates.append(('CX', control, target))
        elementary_gates.append(('RZ', target, -np.pi / 4))
        elementary_gates.append(('CX', control, target))
    
    elif gate == 'S':
        # Controlled-S gate decomposition
        elementary_gates.append(('RZ', target, np.pi / 2))
        elementary_gates.append(('CX', control, target))
        elementary_gates.append(('RZ', target, -np.pi / 2))
        elementary_gates.append(('CX', control, target))
    
    else:
        raise ValueError(f"Unsupported controlled gate: {gate}")
    
    return elementary_gates

def PE_gate(g, env):
    rule = node_rule(g, "gate")
    result = deepcopy(g)
    try:
        match(rule):
            case ['NOT']:
                return decompose_single_qubit_gate('X', g.children[0].value)
            case ['H']:
                return decompose_single_qubit_gate('H', g.children[0].value)
            case ['rgate', 'exp']:
                [rgate, angle_exp] = g.children
                (a, a_static) = PE_exp(angle_exp, env)
                result.children = [rgate, a]
                return result
            case ['qupdate', 'IF', 'lval']:
                qupdate_node, _, lval_node = g.children
                qupdate_res = PE_qupdate(qupdate_node, env)
                lval_res, lval_name, lval_index, lval_static = PE_lval(lval_node, env)
                
                if lval_static:
                    condition = evaluate_lval(lval_name, lval_index, env)
                    if condition:
                        return qupdate_res
                    else:
                        return make_skip_statement()
                else:
                    result.children[0] = qupdate_res
                    result.children[2] = lval_res
                    return result
            case _:
                raise Exception(f"PE_gate: Unrecognized rule {rule} in {showcq_gate(g)}")
    except Exception as ex:
        print(f"PE_gate: Error {ex} evaluating rule {rule} for gate-node {g}")
        raise ex