from parser import *
import time
import sys

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}
        self.variable_types = {}

    def no_found_visit_error(self, node):
        raise Exception(f"Not found visit_{type(node).__name__}")

    def visit_SliceNode(self, node):
        return self.visit(node.value)[self.visit(node.first):self.visit(node.second)]

    def visit(self, node):
        return getattr(self, f"visit_{type(node).__name__}", self.no_found_visit_error)(node)

    def infer_type_from_value(self, value):
        types = {
            'int': "TYPE_INT",
            'float': "TYPE_FLOAT",
            'str': "TYPE_STRING",
            'bool': "TYPE_BOOL"
        }
        return types.get(type(value).__name__)

    def visit_IntNumberNode(self, node):
        return node.value

    def visit_FloatNumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_TypeCastNode(self, node):
        expression_value = self.visit(node.expression)
        target_type = node.target_type
        types = {
            "TYPE_INT": lambda x: int(x),
            "TYPE_FLOAT": lambda x: float(x),
            "TYPE_STRING": lambda x: str(x),
            "TYPE_BOOL": lambda x: bool(x)
        }
        if target_type in types:
            return types[target_type](expression_value)


    def visit_BinOpNode(self, node):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        left_type = self.variable_types.get(node.left.name) if isinstance(node.left, VariableNode) else None
        right_type = self.variable_types.get(node.right.name) if isinstance(node.right, VariableNode) else None

        if node.op == "PLUS":
            if left_type == "TYPE_BOOL" and right_type == "TYPE_BOOL":
                return left_value or right_value
            else:
                return left_value + right_value

        elif node.op == "MINUS":
            return left_value - right_value

        elif node.op == "DIVIDE":
            if right_value != 0:
                return left_value / right_value
            raise ZeroDivisionError("Division by zero")

        elif node.op == "MULTIPLY":
            return left_value * right_value
        else:
            raise Exception(f"Unknown binary operator: {node.op}")

    def visit_VariableDeclarationNode(self, node):
        var_name = node.name
        var_value = self.visit(node.value)
        current_variable_debug = [f"Var name: {var_name}", f"Var value: {var_value}", f"Var type: {node.type}"]
        if node.type is None:
            var_type = self.infer_type_from_value(var_value)
            current_variable_debug.append("Динамическая типизация")
            if var_type is None:
                raise Exception(f"InterpreterVarDecErr: Cannot infer type for variable '{var_name}'")
        else:
            current_variable_debug.append("Статическая типизация")
            var_type = node.type

        if var_type == "TYPE_INT" and not isinstance(var_value, (int, float)):
            raise TypeError(f"Expected TYPE_INT, got {type(var_value)}")
        elif var_type == "TYPE_FLOAT" and not isinstance(var_value, (int, float)):
            raise TypeError(f"Expected TYPE_FLOAT, got {type(var_value)}")
        elif var_type == "TYPE_STRING" and not isinstance(var_value, str):
            raise TypeError(f"Expected TYPE_STRING, got {type(var_value)}")
        elif var_type == "TYPE_BOOL" and not isinstance(var_value, bool):
            raise TypeError(f"Expected TYPE_BOOL got {type(var_value)}")

        if var_name not in self.variables:
            self.variables[var_name] = var_value
            self.variable_types[var_name] = var_type
            return var_value
        else:
            raise InterpreterErrors("Invalid Syntax", f"Variable '{var_name}' already exists")
    def visit_VariableNode(self, node):
        var_name = node.name
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            raise Exception(f"The name '{var_name}' is not defined in the current scope")
    def visit_ConcatenationNode(self, node):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return str(left_value) + str(right_value)

    def visit_StdoutNode(self, node):
        if node.expression is None: return None
        if isinstance(node.expression, MultiValueNode):
            output = self.visit_MultiValueNode(node.expression)
        elif isinstance(node.expression, FloatNumberNode):
            output = float(self.visit(node.expression))
        else:
            output = str(self.visit(node.expression))

        return output
    def visit_UnaryOpNode(self, node):
        value = self.visit(node.node)
        return -value

    def visit_MultiValueNode(self, node):
        values = (str(self.visit(value_node)) for value_node in node.values)
        return node.separator.join(values)

    def visit_AssignmentNode(self, node):
        var_name = node.variable_name
        var_value = self.visit(node.expression)

        if var_name not in self.variables:
            raise Exception(f"The name '{var_name}' is not defined in the current scope")

        inferred_type = self.infer_type_from_value(var_value)

        self.variables[var_name] = var_value
        self.variable_types[var_name] = inferred_type
        return var_value

    def visit_BooleanNode(self, node):
        return node.value

    def visit_GetTypeNode(self, node):
        target_type = type(self.visit(node.object)).__name__
        names = {
            'str': "String",
            'int': "Int",
            'bool': "Bool",
            'float': "Float"
        }
        return names[target_type]

    def visit_AbsNode(self, node):
        return abs(self.visit(node.value))

    def visit_LengthNode(self, node):
        value = self.visit(node.value)
        return len(value) if isinstance(value, str) else None

    def visit_NoneType(self, node):
        return None

    def get_vars_and_types(self):
        return self.variables, self.variable_types
def interpret(ast):
    interpreter = Interpreter(ast)
    results = []
    start_time = time.time()
    for node in ast:
        result = interpreter.visit(node)
        if isinstance(node, StdoutNode):
            results.append(result)

    end_time = time.time()
    execution_time = end_time - start_time
    variables = interpreter.get_vars_and_types()
    return results
