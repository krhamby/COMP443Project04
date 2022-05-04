#exec(open("calc_lang.py").read())

# from sqlalchemy import null
from grove_lang import *
import re
import sys

# Utility methods for handling parse errors


def check(condition, message="Unexpected end of expression"):
    """ Checks if condition is true, raising a GroveError otherwise """
    if not condition:
        raise GroveError("GROVE: " + message)


def expect(token, expected):
    """ Checks that token matches expected
        If not, throws a GroveError with explanatory message """
    if token != expected:
        check(False, "Expected '" + expected + "' but found '" + token + "'")


def is_expr(x):
    if not isinstance(x, Expr):
        check(False, "Expected expression but found " + str(type(x)))
# Checking for integer


def is_int(s):
    """ Takes a string and returns True if it can be converted to an integer """
    try:
        int(s)
        return True
    except Exception:
        return False


def is_string_literal(s):
    """ Takes a string and returns True if in can be converted to a string literal """
    
    if len(s.split()) > 1:
        raise GroveError("GROVE: string literals should not have spaces in them")
        return False
    if len(s.split("\"")) > 3:
        raise GroveError("GROVE: extra quotation marks in string")
        return False
    else:
        return True


def is_global_var(s):
    """ Takes a string and returns True if it can be converted to a global variable """
    if s in var_table:
        return True
    else:
        return False


def method_exists(var, method):
    """ Returns True if the method exists for the var """
    methods = dir(var.eval())
    if method in methods:
        return True
    else:
        return False


def parse(s):
    """ Return an object representing a parsed command
        Throws GroveError for improper syntax """   
    (root, remaining_tokens) = parse_tokens(s.split())
    check(len(remaining_tokens) == 0,
          "Expected end of command but found '" + " ".join(remaining_tokens) + "'")
    return root


def parse_tokens(tokens):
    """ Returns a tuple:
        (an object representing the next part of the expression,
         the remaining tokens)
    """

    check(len(tokens) > 0)

    start = tokens[0]

    if is_int(start):
        return (Num(int(start)), tokens[1:])
    
    # checks if string literal
    elif start[0] == "\"":
        expect (start[-1], "\"")
        check(is_string_literal(start), "GROVE: invalid string literal")
        return (StringLiteral(start.strip("\"")), tokens[1:])
    
    elif start == "+":
        check(len(tokens) > 0)
        expect(tokens[1], "(")
        (child1, tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 1)
        expect(tokens[0], ")")
        expect(tokens[1], "(")
        (child2, tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 0)
        expect(tokens[0], ")")
        return (Addition(child1, child2), tokens[1:])
    
    elif start == "set":
        check(len(tokens) > 0)
        check((tokens[1][0].isalpha() or tokens[1][0] == "_"),
            "GROVE: variable names must start with alphabetic characters")
        check(re.match(
            r'^\w+$', tokens[1]), "GROVE: variable names must be alphanumeric characters or _ only")
        (varname, tokens) = parse_tokens(tokens[1:])
        check(len(tokens) > 0)
        expect(tokens[0], "=")
        (child, tokens) = parse_tokens(tokens[1:])
        
        # NOTE: tokens will have a length of one
        # TODO: add a complex variable assignment
        if type(child) == Name and child.name == "new":
            check(len(tokens) > 0)
            # (child, tokens) = parse_tokens(tokens)
            return (ComplexAssignment(varname, tokens[0]), tokens[1:])
        else:
            return (SimpleAssignment(varname, child), tokens)

    #TODO: do for import
    elif start == "import":
        check(len(tokens) > 1, "no import specified")
        check((tokens[1][0].isalpha() or tokens[1][0] == "_"),
            "GROVE: import module names must start with alphabetic characters or underscores")
        check(re.match(
            r'^\w+$', tokens[1]), "GROVE: import module names must be composed of alphanumeric characters or _ only")
        check(len(tokens[2:]) == 0, "Expected one argument in import statement, found " + str(len(tokens[1:])))
        (module, tokens) = parse_tokens(tokens[1:])
        
        
        return (Import(module), tokens[2:])
    elif (start in ["quit", "exit"]):
        sys.exit()
        
    # parsing for method call objecss    
    elif start == "call":
        check(len(tokens) > 1, "no method name specified")
        expect(tokens[1], "(")
        # TODO: pick up debugging here
        check(len(tokens) > 2, "no arguments specified")
        check(is_global_var(tokens[2]), "'" +
              tokens[2] + "' is not a variable")
        (varName, tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 0)
        check(method_exists(varName, tokens[0]),
              "Method '" + tokens[0] + "' does not exist")
        (method, tokens) = parse_tokens(tokens[0:])
        args = []
        while tokens[0] != ")" and tokens[1:] != []:
            (result, tokens) = parse_tokens(tokens[0:])
            is_expr(result)
            args.append(result)
        return (MethodCall(varName, method, args), tokens[1:])
    elif start == "quit" or start == "exit":
        sys.exit()
    else:
        # print(start[0])
        check((start[0].isalpha() or start[0] == "_"),
              "GROVE: variable names must start with alphabetic characters or _")
        check(re.match(r'^\w+$', start),
              "GROVE: variable names must be composed of alphanumeric characters or _ only")

        return (Name(start), tokens[1:])

    # TODO: parse the next part of the expression


# Testing code
if __name__ == "__main__":

    while True:
        try:
            ln = input("Grove>> ")
            root = parse(ln)
            res = root.eval()
            if not res is None:
                print(res)
        except GroveError:
            print(str(sys.exc_info()[1]))