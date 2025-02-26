from lark import Lark, Transformer
from helpers import evaluate_binop, evaluate_unop, evaluate_fun, named_constants

class CQInterpreter(Transformer):
    def __init__(self):
        super().__init__()

    def add(self, args):
        return evaluate_binop['+'](args[0], args[1])

    def sub(self, args):
        return evaluate_binop['-'](args[0], args[1])

    def mul(self, args):
        return evaluate_binop['*'](args[0], args[1])

    def div(self, args):
        return evaluate_binop['/'](args[0], args[1])

    def NUMERICAL_VALUE(self, value):
        return literal_eval(value)

    def NAMED_CONSTANT(self, value):
        return named_constants[value]

    def BUILTIN_FUN1(self, args):
        func = evaluate_fun[args[0]]
        return func(args[1])

    def BUILTIN_FUN2(self, args):
        func = evaluate_fun[args[0]]
        return func(args[1], args[2])

def evaluate_expression(expression):
    parser = Lark.open("expression-ambiguous.lark", start="exp", parser="lalr", transformer=CQInterpreter())
    return parser.parse(expression)

# Test the interpreter with unambiguous examples
unambiguous1 = "(3 + (5 * 2))"
unambiguous2 = "(0x1A + 0b1010)"
unambiguous3 = "(3.14 * 2.71)"
unambiguous4 = "sin(pi / 2)"

print("Result for unambiguous1:", evaluate_expression(unambiguous1))
print("Result for unambiguous2:", evaluate_expression(unambiguous2))
print("Result for unambiguous3:", evaluate_expression(unambiguous3))
print("Result for unambiguous4:", evaluate_expression(unambiguous4))