import BASIC_Keywords
import BASIC_Errors

class BASIC_Line:
    def __init__(self, lineNumber: int, keywords: list):
        self.lineNumber = lineNumber
        self.keywords = keywords
    
    def execute(self) -> BASIC_Keywords.BASIC_ReturnData:
        #print(self.keywords)
        execOut = self.keywords[0].execute(self.keywords)
        if execOut == None: execOut = BASIC_Keywords.BASIC_ReturnData()
        return execOut


class Lexer:
    def __init__(self, programFileName: str=None):
        self.lines: dict[int, BASIC_Line] = {}
        
        if programFileName == None: return
        print(f"Lexing {programFileName}")
        with open(programFileName, "r") as f: self.parseProgramFile(f.read())

    def getLine(self, lineNum: int) -> BASIC_Line:
        return self.lines.get(lineNum, None)

    def spaceOutOperations(self, part: str):
        part = part.replace("+", " + ")
        part = part.replace("-", " - ")
        part = part.replace("*", " * ")
        part = part.replace("/", " / ")
        part = part.replace("^", " ^ ")
        part = part.replace("=", " = ")
        part = part.replace("<>", " <> ")
        part = part.replace("<", " < ")
        part = part.replace("<=", " <= ")
        part = part.replace(">", " > ")
        part = part.replace("=?", " => ")
        return part

    def determineVariableName(self, part: str) -> BASIC_Keywords.VARIABLE:
        # variables can be A-Z and A0-A9, B0-B9... Z0-Z9
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if part == letter: return BASIC_Keywords.VARIABLE(letter)
            if part == f"-{letter}": return BASIC_Keywords.VARIABLE(letter, isNegative=True)
            for n in range(0, 9+1):
                letterWithNum = (letter + str(n))
                if part == letterWithNum: return BASIC_Keywords.VARIABLE(letterWithNum)
                if part == f"-{letterWithNum}": return BASIC_Keywords.VARIABLE(letterWithNum, isNegative=True)
        
        return None

    def determineStatementFromPart(self, part: str):
        if part == "DEF": return BASIC_Keywords.DEF_Statement()
        if part == "DIM": return BASIC_Keywords.DIM_Statement()
        if part == "END": return BASIC_Keywords.END_Statement()
        if part == "STOP": return BASIC_Keywords.STOP_Statement()
        if part == "FOR": return BASIC_Keywords.FOR_Statement()
        if part == "TO": return BASIC_Keywords.TO_Statement()
        if part == "STEP": return BASIC_Keywords.STEP_Statement()
        if part == "NEXT": return BASIC_Keywords.NEXT_Statement()
        if part == "GOSUB": return BASIC_Keywords.GOSUB_Statement()
        if part == "RETURN": return BASIC_Keywords.RETURN_Statement()
        if part == "GOTO": return BASIC_Keywords.GOTO_Statement()
        if part == "IF": return BASIC_Keywords.IF_Statement()
        if part == "THEN": return BASIC_Keywords.THEN_Statement()
        if part == "LET": return BASIC_Keywords.LET_Statement()
        if part == "PRINT": return BASIC_Keywords.PRINT_Statement()
        if part == "DATA": return BASIC_Keywords.DATA_Statement()
        if part == "READ": return BASIC_Keywords.READ_Statement()
        if part == "REM": return BASIC_Keywords.REM_Statement()
        return None

    def determineOperatorFromPart(self, part: str):
        if part == "+": return BASIC_Keywords.ADD_Operator()
        if part == "-": return BASIC_Keywords.SUB_Operator()
        if part == "*": return BASIC_Keywords.MULT_Operator()
        if part == "/": return BASIC_Keywords.DIV_Operator()
        if part == "^": return BASIC_Keywords.EXP_Operator() # I want to use "^" instead of "?" for exponents
        if part == "=": return BASIC_Keywords.EQUAL_Operator()
        if part == "<>": return BASIC_Keywords.NOTEQUAL_Operator()
        if part == "<": return BASIC_Keywords.LESS_Operator()
        if part == "<=": return BASIC_Keywords.LESSEQUAL_Operator()
        if part == ">": return BASIC_Keywords.GREATER_Operator()
        if part == "=>": return BASIC_Keywords.GREATEREQUAL_Operator()
        if part == "(": return BASIC_Keywords.GROUPING_OPEN_Operator()
        if part == ")": return BASIC_Keywords.GROUPING_CLOSE_Operator()
        return None
    
    def determineFunctionFromPart(self, part: str):
        if (part.startswith("ABS") == False and
            part.startswith("ATN") == False and
            part.startswith("COS") == False and
            part.startswith("EXP") == False and
            part.startswith("INT") == False and
            part.startswith("LOG") == False and
            part.startswith("RND") == False and
            part.startswith("SIN") == False and
            part.startswith("SQR") == False and
            part.startswith("TAN") == False): return None

        if len(part) < 6: return None # 6 for the "XXX(V)", 3 for the function name, 2 for parenthesis, 1 for var name
        inners = part[4:-1] # strip out "XXX(" and ")" to leave just the inners
        inners = self.spaceOutOperations(inners)
        #print(inners)
        innerChain = self.breakDownParts(inners.split(" "))
        #print(innerChain)

        if part.startswith("ABS"): return BASIC_Keywords.ABS_Function(innerChain)
        if part.startswith("ATN"): return BASIC_Keywords.ATN_Function(innerChain)
        if part.startswith("COS"): return BASIC_Keywords.COS_Function(innerChain)
        if part.startswith("EXP"): return BASIC_Keywords.EXP_Function(innerChain)
        if part.startswith("INT"): return BASIC_Keywords.INT_Function(innerChain)
        if part.startswith("LOG"): return BASIC_Keywords.LOG_Function(innerChain)
        if part.startswith("RND"): return BASIC_Keywords.RND_Function(innerChain)
        if part.startswith("SIN"): return BASIC_Keywords.SIN_Function(innerChain)
        if part.startswith("SQR"): return BASIC_Keywords.SQR_Function(innerChain)
        if part.startswith("TAN"): return BASIC_Keywords.TAN_Function(innerChain)
        return None
    
    def determineLiteral(self, part: str) -> float:
        try:
            value = float(part)
            return value
        except ValueError as e: return None

    def determineQuote(self, part: str) -> str:
        if part.startswith("\"") and part.endswith("\""): return part
        else: return None

    def breakDownParts(self, parts: list[str]) -> list:
        breakdown = []
        for part in parts:
            if len(part) == 0: continue
            function = self.determineFunctionFromPart(part)
            if function != None:
                breakdown.append(function)
                continue
            statement = self.determineStatementFromPart(part)
            if statement != None:
                if type(statement) == BASIC_Keywords.REM_Statement: return [] # dont continue this
                breakdown.append(statement)
                continue
            operator = self.determineOperatorFromPart(part)
            if operator != None:
                breakdown.append(operator)
                continue
            variable = self.determineVariableName(part)
            if variable != None:
                breakdown.append(variable)
                continue
            literal = self.determineLiteral(part)
            if literal != None:
                breakdown.append(literal)
                continue
            quote = self.determineQuote(part)
            if quote != None:
                breakdown.append(quote)
                continue

            raise BASIC_Errors.UnknownKeyworkException(part)
        return breakdown

    def parseProgramFile(self, contents: str):
        self.lines = {} # clear the program before we add stuff
        hasStopInstruction = False
        previousLineNumber = -1
        contentLines = contents.split("\n")

        for line in contentLines:
            if len(line) == 0: continue
            parts = line.split(" ")
            lineNum = int(parts[0])
            # todo: give them actual line numbers from the .bas file
            if previousLineNumber > lineNum: raise BASIC_Errors.LineOutOfOrderException(f"`{line}` | {previousLineNumber=} {lineNum=}")
            if self.lines.get(lineNum, None) != None: raise BASIC_Errors.LineRefedinitionException(f"Line {lineNum} is redefiend by: `{line}`")
            
            keywords = None
            try: keywords = self.breakDownParts(parts[1:])
            except BASIC_Errors.UnknownKeyworkException as e:
                groupingToolTip = ""
                if ("(" in line) or (")" in line): groupingToolTip = "If you're grouping using parenthesis for math then make sure to put spaces between each one"
                # handle it here so i can give the context, e.message is the part/keyword that was not found
                raise BASIC_Errors.UnknownKeyworkException(f"Unknown keyword `{e.message}`! `{line}`\n{groupingToolTip}")
            
            if keywords == None: raise Exception("Keywords is None??")
            if len(keywords) == 0: continue # REM comment probably caused this
            if type(keywords[0]) == BASIC_Keywords.STOP_Statement: hasStopInstruction = True

            programLine = BASIC_Line(lineNum, keywords)
            self.lines[lineNum] = programLine
            previousLineNumber = lineNum

        if hasStopInstruction == False:
            raise BASIC_Errors.ExpectedKeywordTypeException("STOP Keyword not found in program! Make sure there is one to prevent infinite loops!")
        
        pass
