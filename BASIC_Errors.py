class LineOutOfOrderException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class LineRefedinitionException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UnknownKeyworkException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ExpectedKeywordTypeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidExpressionException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

