from colorama import Fore, init
init()
class ASTNode:
    pass
Types = (
    "TYPE_INT"
    "TYPE_STRING"
    "TYPE_BOOL"
    "TYPE_FLOAT"
)


class StdoutNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"StdoutNode(expression={self.expression})"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"StringNode(value={Fore.YELLOW}\"{self.value}\"{Fore.RESET})"

class IntNumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"IntNumberNode(value={Fore.BLUE}{self.value}{Fore.RESET})"

class FloatNumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"FloatNumberNode(value={Fore.BLUE}{self.value}{Fore.RESET})"
class BinOpNode(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinOpNode(op='{Fore.MAGENTA}{self.op}{Fore.RESET}', left={self.left}, right={self.right})"
class UnaryOpNode(ASTNode):
    def __init__(self, op, node):
        self.op = op
        self.node = node
    def __repr__(self):
        return f"UnaryOpNode(op='{Fore.MAGENTA}{self.op}{Fore.RESET}', node={self.node})"

class ConcatenationNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"ConcatenationNode(left={self.left}, right={self.right})"

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"VariableNode(name={Fore.CYAN}{self.name}{Fore.RESET})"

class VariableDeclarationNode(ASTNode):
    def __init__(self, variable_name, variable_type, variable_value):
        self.name = variable_name
        self.type = variable_type
        self.value = variable_value
    def __repr__(self):
        return f"VariableDeclarationNode(variable_name={Fore.RED}\"{self.name}\"{Fore.RESET}, type={Fore.RED}{self.type}{Fore.RESET}, value={self.value})"
class MultiValueNode(ASTNode):
    def __init__(self, values, separator=" "):
        self.values = values
        self.separator = separator
    def __repr__(self):
        return f"MultiValueNode(values={self.values}, sep={self.separator})"
class AssignmentNode(ASTNode):
    def __init__(self, variable_name, expression):
        self.variable_name = variable_name
        self.expression = expression
    def __repr__(self):
        return f"AssignmentNode(variable_name={self.variable_name}, expression={self.expression})"
class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BooleanNode(value={Fore.YELLOW}{self.value}{Fore.RESET})"

class TypeCastNode(ASTNode):
    def __init__(self, expression, target_type):
        self.expression = expression
        self.target_type = target_type
    def __repr__(self):
        return f"TypeCastNode(expression={self.expression}, target_type={self.target_type})"

class GetTypeNode(ASTNode):
    def __init__(self, object_):
        self.object = object_
    def __repr__(self):
        return f"GetTypeNode(object={self.object})"

class AbsNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"AbsNode(value={self.value})"

class LengthNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"LengthNode(value={self.value})"

class SliceNode(ASTNode):
    def __init__(self, value, first, second):
        self.value = value
        self.first = first
        self.second = second
    def __repr__(self):
        return f"SliceNode(value={self.value}, first={self.first}, second={self.second})"

class Object(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Object(name={self.name})"

class BuiltInFunctionRepresentation(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"BuiltInFunction(name={self.name})"
