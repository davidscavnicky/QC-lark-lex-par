from copy import deepcopy
from typing import List
from lark import Token, Tree
from lark.tree import Branch
from show import show_qupdate, show_statement
from helpers import node_rule, make_constant
from PEjames import evaluate_exp
import numpy as np
import cmath
import networkx as nx
from cnotrouting import *


def synthesize(program: Tree, topology: nx.Graph) -> Tree:

    [procedure] = program.children
    [_, _, procedure_stmt] = procedure.children 
    [block] = procedure_stmt.children
    [_, statements] = block.children

    synthesized_statements = []

    for statement in statements.children:

        synthesized_statements.extend(synthesize_statement(statement, topology))

    synthesized_program = deepcopy(program)

    synthesized_program.children[0].children[2].children[0].children[1].children = synthesized_statements

    return synthesized_program

def synthesize_statement(statement: Tree, topology: nx.Graph) -> List[Branch[Token]]:
        """
        Synthesize a quantum statement, including CNOT routing.
        """    

        rule = node_rule(statement, "statement")

        match rule:
            case ['qupdate'] | ['qupdate','IF','lval']:

                qupdate = statement.children[0]

                s_qupdates = synthesize_qupdate(qupdate)

                #return [wrap_qupdate(statement, sq) for sq in s_qupdates]
                return [Tree(Token('RULE', 'qupdate'), sq.children) for sq in add_cnot_routing(s_qupdates, topology)]

            case ['MEASURE','lval','lval']:

                raise Exception(f"Synthesize: Measure not yet implemented")

            case _:

                raise Exception(f"Synthesize: Unrecognized rule {rule} in {show_statement(statement)}")

def synthesize_qupdate(qupdate: Tree) -> List[Tree[Token]]:

    [gate, lval] = qupdate.children

    rule = node_rule(gate)

    match rule:

        case ['H']:
            return synthesize_H(lval)

        case ['NOT']:
            return synthesize_Rx(np.pi, lval)

        case ['rgate', _]:

            [rgate, angle_exp] = gate.children
            [axis] = rgate.children
            angle = evaluate_exp(angle_exp, [])

            match (axis.value if isinstance(axis, Token) else None):
                case 'Rx':
                    return synthesize_Rx(angle, lval)
                case 'Ry':
                    return synthesize_Ry(angle, lval)
                case 'Rz':
                    return [make_Rz(angle, lval)]
                case _:
                    raise Exception(f"Synthesize Qupdate: Missing implementation for {show_qupdate(qupdate)}")
        
        case _:
            raise Exception(f"Synthesize Qupdate: Missing implementation for {show_qupdate(qupdate)}")

def wrap_qupdate(statement: Tree[Token], qupdate: Tree[Token]) -> Tree[Token]:

    s_statement = deepcopy(statement)
    s_statement.children[0] = qupdate

    return s_statement


def synthesize_H(lval: Tree) -> List[Tree[Token]]:

    return [
        make_X(lval),
        *synthesize_Ry(np.pi / 2, lval),
    ]


def synthesize_Rx(angle: float, lval: Tree) -> List[Tree[Token]]:

    return [
        make_Rz(np.pi / 2, lval),
        *synthesize_Ry(angle, lval),
        make_Rz(-np.pi / 2, lval),
    ]


def synthesize_Ry(angle: float, lval: Tree) -> List[Tree[Token]]:

    return [
        make_SX(lval),
        make_SX(lval),
        make_SX(lval),
        make_Rz(angle, lval),
        make_SX(lval),
    ]


def make_gate(name: str) -> Tree[Token]:

    return Tree(Token('RULE', 'gate'), [
        Token(name, name)
    ])


def make_SX(lval: Tree) -> Tree[Token]:

    gate = make_gate('SX')
    return make_qupdate(gate, lval)


def make_X(lval: Tree) -> Tree[Token]:

    gate = make_gate('X')
    return make_qupdate(gate, lval)


def make_Rz(rotation: float, lval: Tree) -> Tree[Token]:

    gate = Tree(Token('RULE', 'gate'), [
        Tree(Token('RULE', 'rgate'), [Token('__ANON_1', 'Rz')]),
        make_constant(rotation)
    ])
    return make_qupdate(gate, lval)


def make_qupdate(gate: Tree, lval: Tree) -> Tree[Token]:

    return Tree(Token('RULE', 'qupdate') , [
        gate,
        deepcopy(lval)
    ])