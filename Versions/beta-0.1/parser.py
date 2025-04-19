from ast_classes import *
from exception import *

init()

class Parser:
    def __init__(self, tokens : list) -> None:
        self.tokens = tokens
        self.position = -1
        self.current_token = None
        self.last_token = None
        self.advance()

    def raise_error(self, name, details) -> Error:
        raise Error(name, details, self.last_token.line, self.last_token.column)

    def advance(self) -> None:
        self.position += 1
        self.last_token = self.current_token
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def peek(self, offset=1):
        return self.tokens[self.position + offset]

    def parse(self) -> list:
        statements = []
        while self.current_token is not None: statements.append(self.parse_statement())
        return statements

    def parse_statement(self) -> (None, ASTNode):
        if self.current_token is None: return None
        statement_parse_enter_point = {} # TODO Заменить if elif else на структуру
        if self.current_token.type == "STDOUT":
            statement = self.parse_stdout()
        elif self.current_token.type == "VAR_KEYWORD":
            statement = self.parse_var_declaration()
        elif self.current_token.type == "IDENTIFIER":
            variable_name = self.current_token.value
            self.advance()
            if self.current_token is not None and self.current_token.type == "ASSIGN":
                self.advance()
                expression = self.parse_expression()
                if self.current_token is not None and self.current_token.type == "SEMI_COLON":
                    self.advance()
                return AssignmentNode(variable_name, expression)
            else:
                if self.current_token is not None and self.current_token.type == "SEMI_COLON":
                    self.advance()
                else:
                    self.raise_error("Statement Error", "Excepted ';' at the end of statement")
                return VariableNode(variable_name)
        else:
            statement = self.parse_expression()


        if self.current_token is None or self.current_token.type != "SEMI_COLON":
            self.raise_error("Statement Error", "Excepted ';' at the end of statement")

        self.advance()
        return statement

    def parse_var_declaration(self) -> VariableDeclarationNode:
        self.advance()

        if self.current_token is None or self.current_token.type != "IDENTIFIER":
            self.raise_error("Invalid Syntax","Excepted variable name after keyword var.",)

        var_name = self.current_token.value
        var_type = None
        self.advance()

        if self.current_token.type == "COLON":
            self.advance()

            if self.current_token is None or self.current_token.type not in Types:
                self.raise_error("Invalid Variable Declaration","Excepted type after ':'")

            var_type = self.current_token.type
            self.advance()

            if self.current_token.type != "ASSIGN":
                self.raise_error("Invalid Syntax","Excepted '=' after type declaration")
            self.advance()

        elif self.current_token.type == "DYNAMIC_ASSIGN":
            self.advance()
        elif self.current_token.type == "ASSIGN":
            self.raise_error("Invalid Syntax", "You can't use '=' to declare a variable. Use ':=' or ': type ='")
        else:
            self.raise_error("Invalid Syntax","Expected ':=' after variable id")

        value = self.parse_expression()

        return VariableDeclarationNode(var_name, var_type, value)

    def parse_stdout(self) -> StdoutNode:
        self.advance()

        if self.current_token is not None and self.current_token.type == "SEMI_COLON":
            return StdoutNode(None)

        elif self.current_token.type == "VAR_KEYWORD":
            self.raise_error("SyntaxError","an attempt to declare a variable inside 'stdout'")
        first_value = self.parse_expression()

        if self.current_token is not None and self.current_token.type == "COMMA":
            values = [first_value]
            while self.current_token is not None and self.current_token.type == "COMMA":
                self.advance()
                values.append(self.parse_expression())

            return StdoutNode(MultiValueNode(values))
        else:
            return StdoutNode(first_value)

    """
    !!! -ФУНКЦИЙ- !!!
    """

    def parse_type(self) -> GetTypeNode:
        expression = self.function("type", self.parse_expression)
        return GetTypeNode(expression)

    def parse_abs(self) -> AbsNode:
        result = self.function("abs", self.parse_expression)
        return AbsNode(result)

    def parse_length(self) -> LengthNode:
        length = self.function("length", self.parse_expression)
        return LengthNode(length)

    def parse_slice(self, string_to_method) -> SliceNode:
        slice_func = self.function("slice", self.parse_expression)
        if isinstance(slice_func, ASTNode):
            self.raise_error("Index Error", f"Function 'slice' excepted 2 args but got 1")
        else:
            if len(slice_func) != 2:
                self.raise_error("Index Error", f"Function 'slice' expected 2 args, but got {len(slice_func)}")
        return SliceNode(StringNode(string_to_method), slice_func[0], slice_func[1])

    """
    !!! - КОНЕЦ ФУНКЦИЙ- !!!
    """
    def parse_expression(self):
        left = self.parse_term()
        while self.current_token is not None and self.current_token.type in ("PLUS", "MINUS"):
            op = self.current_token
            self.advance()
            right = self.parse_term()

            if (isinstance(left, StringNode) and isinstance(right, StringNode) or
                    isinstance(left, ConcatenationNode) or isinstance(right, ConcatenationNode)):
                left = ConcatenationNode(left, right)
            else:
                left = BinOpNode(op.type, left, right)

        if self.current_token is not None and self.current_token.type == "ARROW":
            left = self.parse_cast(left)

        return left

    def parse_cast(self, expression):
        self.advance()

        if self.current_token is None or self.current_token.type not in Types:
            self.raise_error("SyntaxError","Expected type after '->'")
        target_type = self.current_token.type
        self.advance()
        return TypeCastNode(expression, target_type)

    def parse_term(self):
        left = self.parse_factor()

        while self.current_token is not None and self.current_token.type in ('MULTIPLY', 'DIVIDE'):
            op = self.current_token
            self.advance()

            if self.current_token is None or (self.current_token.type not in (
            "INTEGER", "FLOAT", "LEFT_PAREN", "STRING", "IDENTIFIER", "FALSE", "TRUE") and self.current_token.type != "MINUS"):
                self.raise_error("SyntaxError", f"Expected factor after operator: {op.type}")

            if self.current_token is not None and self.current_token.type == "MINUS":
                unary_op = self.current_token.type
                self.advance()
                right = UnaryOpNode(unary_op, self.parse_factor())
            else:
                right = self.parse_factor()

            if isinstance(left, StringNode) or isinstance(right, StringNode):
                self.raise_error("TypeError",
                                 f"Multiplication or division of a string is not allowed: {left.__class__.__name__}[{left.value}] and {right.__class__.__name__}[\"{right.value}\"]",)

            left = BinOpNode(op.type, left, right)

        return left

    def create_factor(self, node_class):
        self.advance()
        return node_class

    def parse_factor(self):

        if self.current_token is None: self.raise_error("Factor Exception", "Expected factor, but got end of input")

        if self.current_token.type == "MINUS":
            op = self.current_token.type
            self.advance()
            node = self.parse_factor()
            return UnaryOpNode(op, node)

        based_factors = {
            "INTEGER": lambda: self.create_factor(IntNumberNode(self.current_token.value)),
            "FLOAT": lambda: self.create_factor(FloatNumberNode(self.current_token.value)),
            "TRUE": lambda: self.create_factor(BooleanNode(True)),
            "FALSE": lambda: self.create_factor(BooleanNode(False)),
            "IDENTIFIER": lambda: self.create_factor(VariableNode(self.current_token.value)),
            "LEFT_PAREN": lambda: self.parse_parens()
        }

        function_factors = {
            "TYPE": lambda: self.parse_type(),
            "ABS": lambda: self.parse_abs(),
            "LENGTH": lambda: self.parse_length()
        }

        if self.current_token.type in based_factors:
            return based_factors[self.current_token.type]()

        elif self.current_token.type in function_factors:
            return function_factors[self.current_token.type]()

        elif self.current_token.type == "STRING":
            factor = StringNode(self.current_token.value)
            string_to_method = self.current_token.value
            self.advance()
            if self.current_token and self.current_token.type == "DOT":
                self.advance()
                if self.current_token and self.current_token.type == "SLICE":
                    return self.parse_slice(string_to_method)
            return factor
        elif self.current_token.type == "SEMI_COLON": self.advance()
        elif self.current_token.type == "VAR_KEYWORD": self.advance()
        else: self.raise_error("Parsing error", f"Unexpected factor: {self.current_token.type}")

    def parse_parens(self):
        self.advance()
        if self.current_token.type == "RIGHT_PAREN":
            self.advance()
            return None
        node = self.parse_expression()
        if self.current_token is None or self.current_token.type != "RIGHT_PAREN":
            self.raise_error("SyntaxError", "Expected ')' after expression")
        self.advance()
        return node

    def function(self, function_name, expression_function):
        self.advance() # Пропускаем имя функций

        if self.current_token is None or self.current_token.type != "LEFT_PAREN": # Проверяем есть ли левая скобка
            self.raise_error("Invalid Syntax",f"Expected '(' after '{function_name}' function, Current Token : {self.current_token} Next Token : {self.peek()}")

        self.advance() # Если есть, пропускаем левую скобку и переходим к обработке аргументов

        expression = expression_function()
        values = None
        is_mnogo_argumentov = False
        if self.current_token is not None and self.current_token.type == "COMMA":
            values = [expression]
            while self.current_token is not None and self.current_token.type == "COMMA":
                self.advance()
                values.append(expression_function())

            is_mnogo_argumentov = True

        if self.current_token is None or self.current_token.type != "RIGHT_PAREN":
            self.raise_error("Invalid Syntax",f"Expected ')' after '{expression}'")

        self.advance()
        print(f"Values: {values}")
        if is_mnogo_argumentov:
            print(f"Expression: {expression}")
            return values
        else:
            return expression

def parse(tokens):
    parser = Parser(tokens)
    ast = parser.parse()
    return ast
