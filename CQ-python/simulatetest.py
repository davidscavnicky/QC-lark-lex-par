from synthesis import synthesize, synthesize_statement
from flatten import *
from show import *
from simulate import *
from PEjames import *

static_input = {'d':4}

cqparse = Lark.open("CQ.lark",parser='lalr', start="program")
program = read_file("../CQ-programs/qft2.cq")
program_tree=prune_tree(cqparse.parse(program, start="program"))

print(show_program(program_tree))

pt_res = PE_program(program_tree,static_input) 

print(show_program(synthesize(flatten_program(pt_res))))
