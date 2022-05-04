## Parse tree nodes for the Calc language
import importlib
import pickle
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

    # def __str__(self):
    #     str(self.name)


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

class ComplexAssignment(Stmt):
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
        if self.expr.name.__contains__("."):
            # TODO: finish this
            var_table[self.varName.getName()] = self.expr
        else:
            # TODO: this does not throw an error but does not work
            var_table[self.varName.getName()] = self.expr

# class Argument(Expr):
#     def __init__(self, value):
#         self.argName = argName

#     def eval(self, value):
#         if self.argName in var_table:
#             return Name(self.value().eval())
#         else if glo

 # TODO: implement MethodCall
class MethodCall(Expr):
    def __init__(self, varName, method, args):
        self.varName = varName
        self.method = method
        self.args = args

    def eval(self):
        evald_args = [ar.eval() for ar in self.args]
        return self.varName.eval().__getattribute__(self.method.name)(*evald_args)


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
