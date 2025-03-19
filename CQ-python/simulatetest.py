from synthesis import synthesize, synthesize_statement
from flatten import *
from show import *
from simulate import *
from PEjames import *
import networkx as nx

static_input = {'d':4}

cqparse = Lark.open("CQ.lark",parser='lalr', start="program")
program = read_file("../CQ-programs/qft2.cq")
program_tree=prune_tree(cqparse.parse(program, start="program"))

print(show_program(program_tree))

pt_res = PE_program(program_tree,static_input) 

topology: nx.Graph = nx.Graph()
topology.add_edges_from([(0, 1), (1, 2), (2, 3)])

print(show_program(synthesize(flatten_program(pt_res), topology)))