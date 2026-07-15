# Error messages on page 35 of this manual: `https://swcomputingservices.com/hhhcdata/gebasicm.pdf`

class CurrentExecutionInformation:
    lineNumber: int = 0
    lineText: str = ""

    @classmethod
    def generateLineInfo(cls) -> str:
        return f"Error on line {cls.lineNumber}: \"{cls.lineText}\""


class BASIC_Exception(Exception):
    def __init__(self, message, basicErrorMessage: str):
        self.message = message + "\n" + CurrentExecutionInformation.generateLineInfo()
        self.basicErrorMessage = basicErrorMessage
        if basicErrorMessage != None:
            self.message += f"\n{basicErrorMessage} IN {CurrentExecutionInformation.lineNumber}"
        super().__init__(self.message)

class CompilationException(BASIC_Exception):
    def __init__(self, message, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class RuntimeException(BASIC_Exception):
    def __init__(self, message, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

# Lexing/Compilation Errors
class LineOutOfOrderException(CompilationException):
    def __init__(self, message, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class LineRefedinitionException(CompilationException):
    def __init__(self, message, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class UnknownKeyworkException(CompilationException):
    def __init__(self, message, basicErrorMessage: str):
        self.message = message
        self.basicErrorMessage = basicErrorMessage
        super().__init__(self.message, basicErrorMessage)

class TooMuchDataException(CompilationException):
    def __init__(self, message, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class PrematureENDException(CompilationException):
    def __init__(self, message, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class QuoteNotEndedException(CompilationException):
    def __init__(self, message, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

# Runtime Errors
class ExpectedKeywordTypeException(RuntimeException):
    def __init__(self, message: str, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class InvalidExpressionException(RuntimeException):
    def __init__(self, message: str, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class NoMoreDataException(RuntimeException):
    def __init__(self, message: str, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class NotInSubroutubeException(RuntimeException):
    def __init__(self, message: str, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class NotInForLoopException(RuntimeException):
    def __init__(self, message: str, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class UndefinedLineException(RuntimeException):
    def __init__(self, message: str, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class TooManyForLoopsException(RuntimeException):
    def __init__(self, message: str, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

class GOSUBNestedTooDeeplyException(RuntimeException):
    def __init__(self, message: str, basicErrorMessage: str):
        self.message = message
        super().__init__(self.message, basicErrorMessage)

