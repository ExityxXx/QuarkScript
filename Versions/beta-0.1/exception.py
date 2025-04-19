
class Error(BaseException):
    def __init__(self, error_name, details, code_line, column):
        self.error_name = error_name
        self.details = details
        self.code_line = code_line
        self.column = column

    def __str__(self):
        return f"{self.error_name}: {self.details} at line {self.code_line} column {self.column}"

class InvalidCharacterError(Error):
    def __init__(self, details, code_line, column):
        super().__init__("InvalidCharacterError", details, code_line, column)
    def __str__(self):
        return super().__str__()

class StringError(Error):
    def __init__(self, details, code_line, column):
        super().__init__("UnterminatedString", details, code_line, column)
    def __str__(self):
        return super().__str__()

class InterpreterErrors(Exception):
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
    def __str__(self):
        return f"{self.error_name}: {self.details}"
