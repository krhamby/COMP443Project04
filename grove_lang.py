## Parse tree nodes for the Calc language
import importlib
import sys
var_table = {}


class GroveError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Expr:
    pass


class Num(Expr):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class StringLiteral(Expr):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class Addition(Expr):
    def __init__(self, child1, child2):
        if not isinstance(child1, Expr):
            raise GroveError(
                "GROVE: expected expression but received " + str(type(child1)))
        if not isinstance(child2, Expr):
            raise GroveError(
                "GROVE: expected expression but received " + str(type(child2)))
        self.child1 = child1
        self.child2 = child2

    def eval(self):
        return self.child1.eval() + self.child2.eval()


class Name(Expr):
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def eval(self):
        if self.name in var_table:
            return var_table[self.name]
        else:
            raise GroveError("GroveError: undefined variable " + self.name)


class Stmt:
    pass


class Import(Stmt):
    def __init__(self, moduleName):
        self.moduleName = moduleName

    def eval(self):
        try:
            globals()[self.moduleName] = importlib.import_module(
                self.moduleName)
        except Exception:
            raise GroveError("Invalid module name for import")
    
class SimpleAssignment(Stmt):
    def __init__(self, varName, expr):
        if not isinstance(varName, Name):
            raise GroveError(
                "GroveError: expected variable name but received " + str(type(varName)))
        if not isinstance(expr, Expr):
            raise GroveError(
                "GroveError: expected expression but received " + str(type(expr)))
        self.varName = varName
        self.expr = expr

    def eval(self):
        var_table[self.varName.getName()] = self.expr.eval()
        
 # TODO: implement MethodCall
class MethodCall(Expr):
    pass


# some testing code
if __name__ == "__main__":

    assert(Num(3).eval() == 3)
    assert(Addition(Num(3), Num(10)).eval() == 13)

    caught_error = False
    try:
        print(Name("nope").eval())
    except GroveError:
        caught_error = True
    assert(caught_error)

    assert(StringLiteral("hi").eval() == "hi")

    assert(SimpleAssignment(Name("foo"), Num(10)).eval() is None)
    assert(Name("foo").eval() == 10)

    # Try something more complicated
    # assert(Stmt(Name("foo"), Addition(Num(200), Subtraction(Num(4), Num(12)))).eval() is None)
    # assert(Name("foo").eval() == 192)
