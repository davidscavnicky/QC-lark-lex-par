from copy import deepcopy
from lark.tree import Tree
from lark.lexer import Token
import numpy as np

from helpers import *
from show import *
from type import *
from simulate import procedure_qbits_env
from PEjames import evaluate_exp
from pyzx.circuit import Circuit
from fractions import Fraction

# zx_program takes a #CQ- program as input: A single procedure with a single flat block of declarations and qupdate statements
# This is the result of partially evaluating all the classical parts away from a CQ program and flattening using flatten.py.
# Currently measurement and cbits are not included. The result is a PyZX gate circuit that can be used for analysis and optimization

# qbits_env is maps variable names to their index in the d-qubit basis set, where d is the total number of qubits in the program (input + auxiliary in block scope)

def zx_program(P):
    procedures = P.children
    assert(len(procedures) == 1) # Only one procedure should be left after partial evaluation
    
    main = procedures[0]
    main_name, main_params, main_stat = main.children
    main_block = main_stat.children[0]
    assert(main_block.data == 'block')
    
    qbits_env = procedure_qbits_env(main)

    d = len(qbits_env)
    C = Circuit(d)
    
    decls, stats = main_block.children    
    for s in stats.children:
        zx_statement(s, qbits_env, C)

    return C
    
# 1+2-qubit matrix helper functions
# Single-qubit gate semantics
def zx_qupdate(qupdate: Tree, qbits_env: dict, C: Circuit):
    rule = node_rule(qupdate, "qupdate")
        
    match(rule):
        case ['lval','SWAP','lval']:
            [lval_i, _, lval_j] = qupdate.children
            qbit_i, qbit_j = qbits_env[show_lval(lval_i)], qbits_env[show_lval(lval_j)]
            return C.add_gate("SWAP",qbit_i,qbit_j)

        case ['gate','lval']:
            [gate,lval] = qupdate.children
        
            gate_rule = node_rule(gate)
            qbit_k = qbits_env[show_lval(lval)]

            match(gate_rule):
                case ['X'] | ['NOT'] | ['SX'] | ['H']: 
                    return C.add_gate(show_gate(gate).upper(), qbit_k)
            
                case ['rgate','exp']: 
                    [rgate, angle_exp] = gate.children
                    rtoken = rgate.children[0]

                    try:
                        angle = evaluate_exp(angle_exp, {})                
                        angle_fraction = angle/np.pi # PyZX uses angles in fractions of pi
                    except Exception as e:
                        raise Exception(f"zx_qupdate: Cannot evaluate angle {show_exp(angle_exp)} in {show_gate(gate)}")
            
                    match(rtoken.value):
                        case 'Rx':
                            return C.add_gate('XPhase',qbit_k,phase=angle_fraction)
                    
                        case 'Ry':
                            return C.add_gate('YPhase',qbit_k,phase=angle_fraction)                    
                    
                        case 'Rz':
                            return C.add_gate('ZPhase',qbit_k,phase=angle_fraction)
                case _:
                    raise Exception(f"zx_qupdate: Unrecognized rule {rule} in {show_gate(gate)}")

def zx_controlled_qupdate(qupdate: Tree, control_lval: Tree, qbits_env: dict, C: Circuit):
    [gate, target_lval] = qupdate.children
    rule = node_rule(gate)
    control_qbit = qbits_env[show_lval(control_lval)]
    target_qbit  = qbits_env[show_lval(target_lval)]

    match(rule):
        case ['X'] | ['NOT']: 
            return C.add_gate('CNOT',control_qbit, target_qbit)
            
        case ['SX'] | ['H']:
            raise Exception(f"zx_controlled_update: controlled {show_gate(gate)} not implemented")
        case ['rgate','exp']: 
            [rgate, angle_exp] = gate.children
            rtoken = rgate.children[0]

            try:
                angle = evaluate_exp(angle_exp, {})              
                angle_fraction = Fraction(angle/np.pi)
            except Exception as e:
                raise Exception(f"zx_controlled_update: Cannot evaluate angle {show_exp(angle_exp)} in {show_gate(gate)}")
            
            match(rtoken.value):
                case 'Rx':
                    raise Exception(f"zx_controlled_qupdate: Rx not implemented")
                case 'Ry':
                    C.add_gate(f"YPhase",target_qbit,phase=angle_fraction/2)
                    C.add_gate(f"CNOT",control_qbit,target_qbit)
                    C.add_gate(f"YPhase",target_qbit,phase=-angle_fraction/2)
                    C.add_gate(f"CNOT",control_qbit,target_qbit)
                    return C
                case 'Rz':
                    C.add_gate(f"ZPhase",target_qbit,phase=angle_fraction/2)
                    C.add_gate(f"CNOT",control_qbit,target_qbit)
                    C.add_gate(f"ZPhase",target_qbit,phase=-angle_fraction/2)
                    C.add_gate(f"CNOT",control_qbit,target_qbit)                    
                    return 
        case _:
            raise Exception(f"zx_controlled_update: Unrecognized rule {rule} in {show_gate(gate)}")    



def zx_statement(s: Tree, qbits_env, C: Circuit):
    rule = node_rule(s, "statement")
    
    try:
        match(rule):
            case ['lval', 'EQ', 'exp']: # Assignment
                [lval,EQ,exp]    = s.children
                raise Exception(f"simulate_statement: Assignment {show_lval(lval)} = {show_exp(exp)} not implemented")

            case ['IF', 'exp', 'statement', 'statement'] | ['WHILE', 'exp', 'statement'] | ['block'] | ['procedure_call']: 
                raise Exception(f"simulate_statement: Control flow {show_statement(s)} not implemented")                
                
            case ['qupdate']: # Single-qubit update
                [qupdate] = s.children
                return zx_qupdate(qupdate, qbits_env, C)
                            
            case ['qupdate','IF','lval']:
                [qupdate,_,control_lval] = s.children
                return zx_controlled_qupdate(qupdate, control_lval, qbits_env, C)
                
            case ['MEASURE','lval','lval']:
                raise Exception(f"simulate_statement: MEASURE {show_statement(s)} not implemented")
            
            case _:
                raise Exception(f"simulate_statement: Unrecognized rule {rule} in {show_statement(s)}")
    except Exception as e:
        print(f"simulate_statement: {e} when evaluating {rule} in {s.pretty()}")
        raise e

