from lark import Lark
from show import show_program

# Load the grammar from the CQ.lark file
parser = Lark.open("CQ.lark", start="program")

# Read the initialize.cq file
with open("initialize.cq", "r") as file:
    program_code = file.read()

# Parse the program
tree = parser.parse(program_code)

# Display the resulting AST
print("Abstract Syntax Tree (AST):")
print(tree.pretty())

# Show the program
print("\nProgram:")
print(show_program(tree))