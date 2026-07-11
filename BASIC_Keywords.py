import BASIC_Errors

class BASIC_ReturnData:
    def __init__(
            self, pcSet: int=None, variableSet: tuple[str,float]=None, stopExecution=False, createdLoop=None,
            continueLoopVarName: str=None, addAddressToReturnStack: bool=False,
            returnToAddressFromReturnStack: bool=False
    ):
        self.pcSet = pcSet # NewPcValue
        self.variableSet = variableSet # (VariableName, NewValue)
        self.stopExecution = stopExecution
        
        self.createdLoop = createdLoop
        self.continueLoopVarName = continueLoopVarName
        
        self.addAddressToReturnStack = addAddressToReturnStack
        self.returnToAddressFromReturnStack = returnToAddressFromReturnStack

class BASIC_Loop:
    def __init__(self, variableName: str, start: float, end: float, increment: float=1):
        self.setPc = -1
        self.variableName = variableName
        self.start = start
        self.end = end
        self.increment = increment
    
    def setReturnPC(self, setPc):
        self.setPc = setPc

class VARIABLE:
    variables = {} # should be shared with the interpreter.py
    def __init__(self, name: str, isNegative=False):
        self.name = name
        self.isNegative = isNegative
    
    def __str__(self): return str(self.getValue())

    def getName(self) -> str:
        return self.name

    def getValue(self) -> float:
        value = self.variables.get(self.name, 0) # default value is 0, since it would be all 0 bits i guess
        if self.isNegative: value *= -1

        return value

class ChainedKeywords:
    def __init__(self, keywords: list):
        if type(keywords[0]) != GROUPING_OPEN_Operator:
            # Wrap the keywords in a grouping to make it easier to parse
            keywords = [GROUPING_OPEN_Operator()] + keywords + [GROUPING_CLOSE_Operator()]

        self.keywords = keywords
        self.validate()
    
    def isTypeOperation(self, kwType):
        operators = [
            ADD_Operator, SUB_Operator, MULT_Operator, DIV_Operator, EXP_Function, EQUAL_Operator,
            LESS_Operator, LESSEQUAL_Operator, GREATER_Operator, GREATEREQUAL_Operator
        ]
        if kwType in operators: return True
        return False
    
    def isTypeVarOrLiteral(self, kwType):
        varOrLiteral = [ VARIABLE, float ]
        if kwType in varOrLiteral: return True
        return False

    def validate(self):
        openGroups: int = 0
        closeGroups: int = 0
        prevKwType = None

        for kw in self.keywords:
            kwType = type(kw)
            isOperation = self.isTypeOperation(kwType)
            isVarOrLiteral = self.isTypeVarOrLiteral(kwType)

            if prevKwType != None:
                if isOperation and self.isTypeOperation(prevKwType):
                    raise BASIC_Errors.InvalidExpressionException("Cannot have two operations in a row!")
                if isVarOrLiteral and self.isTypeVarOrLiteral(prevKwType):
                    raise BASIC_Errors.InvalidExpressionException("Cannot have two variables/literals in a row!")
            
            if type(kw) == GROUPING_OPEN_Operator: openGroups += 1
            elif type(kw) == GROUPING_CLOSE_Operator: closeGroups += 1
            
            if closeGroups > openGroups: raise BASIC_Errors.InvalidExpressionException("Invalid pairing of open-close group characters")

            prevKwType = kwType

        # after we've gone through all the keywords check if it's valid
        if closeGroups != openGroups: raise BASIC_Errors.InvalidExpressionException("Invalid pairing of open-close group characters")
        return True # We've made it here, our chain of keywords is valid!

    def evaluate(self) -> float:
        openGroups: int = 0
        closeGroups: int = 0
        prevKwType = None

        outEquation = ""
        for kw in self.keywords:
            kwType = type(kw)
            isOperation = self.isTypeOperation(kwType)
            isVarOrLiteral = self.isTypeVarOrLiteral(kwType)

            if prevKwType != None:
                if isOperation and self.isTypeOperation(prevKwType):
                    raise BASIC_Errors.InvalidExpressionException("Cannot have two operations in a row!")
                if isVarOrLiteral and self.isTypeVarOrLiteral(prevKwType):
                    raise BASIC_Errors.InvalidExpressionException("Cannot have two variables/literals in a row!")
            
            if type(kw) == GROUPING_OPEN_Operator: openGroups += 1
            elif type(kw) == GROUPING_CLOSE_Operator: closeGroups += 1
            
            if closeGroups > openGroups: raise BASIC_Errors.InvalidExpressionException("Invalid pairing of open-close group characters")
            
            toAdd = f" {str(kw)}"
            if isVarOrLiteral: toAdd = f" ({toAdd[1:]})" # surround literals w/ parentheses so -3 ** 2 = 9 not -9
            outEquation += toAdd

            prevKwType = kwType

        # after we've gone through all the keywords check if it's valid
        if closeGroups != openGroups: raise BASIC_Errors.InvalidExpressionException("Invalid pairing of open-close group characters")
        
        result = eval(outEquation) # yes ik eval is evil but i REALLY dont want to write a parser atm 😭
        return result

# Statements
class DEF_Statement:
    def __init__(self):
        pass

class DIM_Statement:
    def __init__(self):
        pass

class END_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        return STOP_Statement().execute(keywords) # same thing, just this cant be restarted by a debugger. idrc

class STOP_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        return BASIC_ReturnData(stopExecution=True)

class FOR_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        # index 0 is the `for`
        # index 1 is the variable
        # index 2 is the `=` sign
        # index 3 is the starting
        # index 4 is the `to``
        # index 5 is the ending
        # (optional)
        # index 6 is the `step`
        # index 7 is the step size
        index1Type = type(keywords[1])
        index2Type = type(keywords[2])
        index3Type = type(keywords[3])
        index4Type = type(keywords[4])
        if index1Type != VARIABLE:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a variable name, instead got a {index1Type}")
        if index2Type != EQUAL_Operator:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected an equal sign, instead got a {index2Type}")
        if index3Type != float:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a literal, instead got a {index3Type}")
        if index4Type != TO_Statement:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a `to`, instead got a {index4Type}")

        end, increment = keywords[4].execute(keywords[4:])
        loop = BASIC_Loop(keywords[1].getName(), keywords[3], end, increment)
        return BASIC_ReturnData(variableSet=(loop.variableName, loop.start), createdLoop=loop)

class TO_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        # index 0 is the `to`
        # index 1 is the end
        # index 2 is optionally a `step`
        increment: float = 1
        end: float = keywords[1]

        index1Type = type(keywords[1])
        if index1Type != float:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a literal, instead got a {index1Type}")
        if len(keywords) > 2:
            index2Type = type(keywords[2])
            if index2Type != STEP_Statement:
                raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a `step`, instead got a {index2Type}")
            
            increment = keywords[2].execute(keywords[2:])

        return end, increment

class STEP_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        # index 0 is the `step`
        # index 1 is the step size
        index1Type = type(keywords[1])
        if index1Type != float:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a literal, instead got a {index1Type}")
        return keywords[1]

class NEXT_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        # index 0 is the `next` keyword
        # index 1 is the variable to increment
        index1Type = type(keywords[1])
        if index1Type != VARIABLE:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a variable name, instead got a {index1Type}")

        var: VARIABLE = keywords[1]
        return BASIC_ReturnData(continueLoopVarName=var.getName())

class GOSUB_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        # index 0 is the `gosub` keyword
        # index 1 is the literal or variable to go to
        index1Type = type(keywords[1])
        address = -1
        if index1Type == VARIABLE: address = keywords[1].getValue()
        elif index1Type == float: address = keywords[1]
        else:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a literal or variable name, instead got a {index1Type}")

        return BASIC_ReturnData(pcSet=address, addAddressToReturnStack=True)

class RETURN_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        # index 0 is the `return` keyword
        return BASIC_ReturnData(returnToAddressFromReturnStack=True)

class GOTO_Statement:
    def __init__(self):
        pass
    def execute(self, keywords):
        # index 0 is the this statement
        # index 1 is the address
        jumpAddressKeyword = keywords[1]
        jumpAddress = jumpAddressKeyword
        if type(jumpAddressKeyword) == VARIABLE: jumpAddress = jumpAddressKeyword.getValue()
        return BASIC_ReturnData(pcSet=jumpAddress)

class IF_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        thenIndex = -1
        for i,kw in enumerate(keywords):
            if type(kw) == THEN_Statement:
                thenIndex = i
                break
        if thenIndex == -1:
            raise BASIC_Errors.ExpectedKeywordTypeException("Expected THEN after IF statement!")

        chained = ChainedKeywords(keywords[1:thenIndex])
        result = chained.evaluate()
        if result: return keywords[thenIndex].execute(keywords[thenIndex:])
        return None

class THEN_Statement:
    def __init__(self):
        pass
    def execute(self, keywords):
        # this is quite literally a copy of the goto statement
        return GOTO_Statement().execute(keywords)

class LET_Statement:
    def __init__(self):
        pass
    def execute(self, keywords: list):
        # index 0 is our let statement
        # index 1 should be the variable name
        # index 2 should be an "=" aka EQUAL_Operator
        # index 3 should be the literal value
        setValue = 0

        typeKeyword1 = type(keywords[1])
        typeKeyword2 = type(keywords[2])
        typeKeyword3 = type(keywords[3])
        if typeKeyword1 != VARIABLE:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a variable name, instead got a {typeKeyword1}")
        if typeKeyword2 != EQUAL_Operator:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected an equals sign, instead got a {typeKeyword2}")
        
        if typeKeyword3 == float:
            setValue = keywords[3]
        elif typeKeyword3 == VARIABLE:
            setValue = keywords[3].getValue()
        else:
            raise BASIC_Errors.ExpectedKeywordTypeException(f"Expected a float or variable name, instead got a {typeKeyword3}")

        # 3 to say we read 3 keywords
        return BASIC_ReturnData(None, (keywords[1].getName(), setValue))

class PRINT_Statement:
    def __init__(self):
        pass

    def execute(self, keywords: list):
        # index 0 is our print class
        # all the other indexes is what we print
        chained = ChainedKeywords(keywords[1:])
        result = chained.evaluate()
        print(result)
        return None # This will just get replaced with an empty BASIC_ReturnData in the lexer

class DATA_Statement:
    def __init__(self):
        pass

class READ_Statement:
    def __init__(self):
        pass

class REM_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        # How is this running? This is to write comments in BASIC
        pass


# Operators
class ADD_Operator:
    def __init__(self):
        pass
    def __str__(self): return "+"

class SUB_Operator:
    def __init__(self):
        pass
    def __str__(self): return "-"

class MULT_Operator:
    def __init__(self):
        pass
    def __str__(self): return "*"

class DIV_Operator:
    def __init__(self):
        pass
    def __str__(self): return "/"

class EXP_Operator:
    def __init__(self):
        pass
    def __str__(self): return "**"

class EQUAL_Operator:
    def __init__(self):
        pass
    def __str__(self): return "=="

class NOTEQUAL_Operator:
    def __init__(self):
        pass
    def __str__(self): return "!="

class LESS_Operator:
    def __init__(self):
        pass
    def __str__(self): return "<"

class LESSEQUAL_Operator:
    def __init__(self):
        pass
    def __str__(self): return "<="

class GREATER_Operator:
    def __init__(self):
        pass
    def __str__(self): return ">"

class GREATEREQUAL_Operator:
    def __init__(self):
        pass
    def __str__(self): return ">="

class GROUPING_OPEN_Operator:
    def __init__(self):
        pass
    def __str__(self): return "("

class GROUPING_CLOSE_Operator:
    def __init__(self):
        pass
    def __str__(self): return ")"

# Functions
import math
import random

class ABS_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain
    
    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        value = abs(value)

        return str(value)

class ATN_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain
    
    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        value = math.atan(value)

        return str(value)

class COS_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain
    
    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        value = math.cos(value)

        return str(value)

class EXP_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain
    
    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        value = math.exp(value) # e^x

        return str(value)

class INT_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain
    
    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        value = math.floor(value)

        return str(value)

class LOG_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain
    
    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        value = math.log(value) # base e, ln

        return str(value)

class RND_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain
    
    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        if value > 0:
            # return a random number
            pass
        elif value == 0:
            # return the same random number as last time
            pass
        elif value < 0:
            # reseed the rng with the input value and return a random number
            pass

        value = random.randrange(0, 1, 0.001) # just make a random number for rn, ignoring seed and stuff

        return str(value)

class SIN_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain
    
    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        value = math.sin(value)

        return str(value)

class SQR_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain

    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        value = math.sqrt(value)

        return str(value)

class TAN_Function():
    def __init__(self, innerChain):
        self.innerChain = innerChain

    def __str__(self):
        chain: ChainedKeywords = ChainedKeywords(self.innerChain)
        value = chain.evaluate()
        value = math.tan(value)

        return str(value)