import numpy as np

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

# Example usage:
# Decompose a Hadamard gate on qubit 0
decomposed_gates = decompose_single_qubit_gate('H', 1)
print(decomposed_gates)