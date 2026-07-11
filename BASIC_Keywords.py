import BASIC_Errors

class BASIC_ReturnData:
    def __init__(self, pcSet: int=None, variableSet: tuple[str,float]=None, stopExecution=False):
        self.pcSet = pcSet # NewPcValue
        self.variableSet = variableSet # (VariableName, NewValue)
        self.stopExecution = stopExecution

class VARIABLE:
    variables = {} # should be shared with the interpreter.py
    def __init__(self, name: str, isNegative=False):
        self.name = name
        self.isNegative = isNegative
    
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
    
    def validate(self):
        openGroups: int = 0
        closeGroups: int = 0
        prevKwType = None

        for kw in self.keywords:
            kwType = type(kw)
            isGroupingType = (kwType == GROUPING_OPEN_Operator) or (kwType == GROUPING_CLOSE_Operator)

            if prevKwType != None:
                pass # check if we can do this
            
            if type(kw) == GROUPING_OPEN_Operator: openGroups += 1
            if type(kw) == GROUPING_CLOSE_Operator: closeGroups += 1
            if closeGroups > openGroups: raise BASIC_Errors.InvalidExpressionException("Invalid pairing of open-close group characters")

        # after we've gone through all the keywords
        if closeGroups != openGroups: raise BASIC_Errors.InvalidExpressionException("Invalid pairing of open-close group characters")

        pass

    def parseGroup(self):
        pass

    def evaluate(self) -> float:
        # A pratt parser using this as a guide: https://dawoodjee.com/blog/pratt-parsing/
        

        return 0

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

class STOP_Statement:
    def __init__(self):
        pass

    def execute(self, keywords):
        return BASIC_ReturnData(stopExecution=True)

class FOR_Statement:
    def __init__(self):
        pass

class TO_Statement:
    def __init__(self):
        pass

class STEP_Statement:
    def __init__(self):
        pass

        pass

class IF_Statement:
    def __init__(self):
        pass

class THEN_Statement:
    def __init__(self):
        pass

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
        return BASIC_ReturnData(None, (keywords[1].name, setValue))

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


# Operators
class ADD_Operator:
    def __init__(self):
        pass

class SUB_Operator:
    def __init__(self):
        pass

class MULT_Operator:
    def __init__(self):
        pass

class DIV_Operator:
    def __init__(self):
        pass

class EXP_Operator:
    def __init__(self):
        pass

class EQUAL_Operator:
    def __init__(self):
        pass

class NOTEQUAL_Operator:
    def __init__(self):
        pass

class LESS_Operator:
    def __init__(self):
        pass

class LESSEQUAL_Operator:
    def __init__(self):
        pass

class GREATER_Operator:
    def __init__(self):
        pass

class GREATEREQUAL_Operator:
    def __init__(self):
        pass

class GROUPING_OPEN_Operator:
    def __init__(self):
        pass

class GROUPING_CLOSE_Operator:
    def __init__(self):
        pass

# Functions
class ABS_Function:
    def __init__(self):
        pass

class ATN_Function:
    def __init__(self):
        pass

class COS_Function:
    def __init__(self):
        pass

class EXP_Function:
    def __init__(self):
        pass

class INT_Function:
    def __init__(self):
        pass

class LOG_Function:
    def __init__(self):
        pass

class RND_Function:
    def __init__(self):
        pass

class SIN_Function:
    def __init__(self):
        pass

class SQR_Function:
    def __init__(self):
        pass

class TAN_Function:
    def __init__(self):
        pass
