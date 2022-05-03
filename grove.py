#exec(open("calc_lang.py").read())
import sys
from grove_lang import *
import re

# Utility methods for handling parse errors


def check(condition, message="Unexpected end of expression"):
    """ Checks if condition is true, raising a GroveError otherwise """
    if not condition:
        raise GroveError("GroveError: " + message)


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
    # if ((s[0] != "\"") | (s[-1] != "\"")):
    #     return False
    if len(s.split()) > 1:
        # raise GroveError("Strings literals should not have spaces in them")
        return False
    if len(s.split("\""))>3:
        # raise GroveError("Extra quotation marks in string")
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
    methods = dir(var)
    print(type(var)) # debugging
    print(methods) # debugging
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
        check(is_string_literal(start), "invalid string literal")
        return (StringLiteral(start), tokens[1:])
    elif start in ["+", "-"]:
        check(len(tokens) > 0)
        expect(tokens[1], "(")
        (child1, tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 1)
        expect(tokens[0], ")")
        expect(tokens[1], "(")
        (child2, tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 0)
        expect(tokens[0], ")")
        if start == "+":
            return (Addition(child1, child2), tokens[1:])
        # else:
        #     return ( Subtraction(child1, child2), tokens[1:] )
    elif start == "set":
        check(len(tokens) > 0)
        check(tokens[1][0].isalpha(), "Variable names must start with alphabetic characters")
        check(re.match(r'^\w+$', tokens[1]), "Variable names must be alphanumeric characters or _ only")
        (varname, tokens) = parse_tokens(tokens[1:])
        check(len(tokens) > 0)
        expect(tokens[0], "=")
        (child, tokens) = parse_tokens(tokens[1:])
        return (SimpleAssignment(varname, child), tokens)
    
    #TODO: do for import
    elif start == "import":
        pass
    
    # TODO: implement method calls
    elif start == "call":
        check(len(tokens) > 0)
        expect(tokens[1], "(")
        check(is_global_var(Name(tokens[2])), "'" + tokens[2] + "' is not a variable") # TODO: pick up debugging here
        (varname, tokens) = parse_tokens(tokens[2:])  
        check(len(tokens) > 0)
        check(method_exists(varname, tokens[0]), "Method '" + tokens[0] + "' does not exist")
        (method, tokens) = parse_tokens(tokens[1:])
        args = []
        while tokens[0] != ")" and tokens[1:] != []:
            (result , tokens) = parse_tokens(tokens[1:])
            check(is_expr(result))
            args.append(result)
        # TODO: these args need to be evaluated
        # or something needs to be returned with MethodCall
            
              

    else:
        check(start[0].isalpha(), "Variable names must start with alphabetic characters")
        check(re.match(r'^\w+$', start), "Variable names must be alphanumeric characters or _ only")

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