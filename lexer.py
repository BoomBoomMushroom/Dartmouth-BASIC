import BASIC_Keywords
import BASIC_Errors

class BASIC_Line:
    def __init__(self, lineNumber: int, keywords: list):
        self.lineNumber = lineNumber
        self.keywords = keywords
    
    def getLoopContinueVarName(self) -> str:
        statement = self.keywords[0]
        if type(statement) != BASIC_Keywords.NEXT_Statement: return None
        statement: BASIC_Keywords.NEXT_Statement = statement
        ret = statement.execute(self.keywords)
        return ret.continueLoopVarName # Either None or the variable name

    def execute(self) -> BASIC_Keywords.BASIC_ReturnData:
        #print(self.keywords)
        execOut = self.keywords[0].execute(self.keywords)
        if execOut == None: execOut = BASIC_Keywords.BASIC_ReturnData()
        return execOut


class Lexer:
    def __init__(self):
        self.lines: dict[int, BASIC_Line] = {}
        self.linesText: dict[int, str] = {}

    def loadFile(self, programFileName: str=None):
        if programFileName == None: return
        print(f"Lexing {programFileName}")
        with open(programFileName, "r") as f: self.loadText(f.read())
    
    def loadText(self, programText: str=None):
        if programText == None: return
        self.parseProgramText(programText)


    def getLine(self, lineNum: int) -> BASIC_Line:
        return self.lines.get(lineNum, None)
    def getLineText(self, lineNum: int) -> str:
        return self.linesText.get(lineNum, "")

    def spaceOutOperations(self, part: str):
        part = part.replace("+", " + ")
        part = part.replace("-", " -") # dont have a space at the end to have negative variables and stuff
        part = part.replace("*", " * ")
        part = part.replace("/", " / ")
        part = part.replace("^", " ^ ")

        part = part.replace("=", " = ")
        part = part.replace("<", " < ")
        part = part.replace(">", " > ")

        # We must consider previous replacements
        part = part.replace(" <  = ", " <= ") # " <  = " -> " <= "
        part = part.replace(" >  = ", " >= ") # " >  = " -> " >= "
        part = part.replace(" <  > ", " <> ") # " <  > " -> " <> "
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

        if part == "RESTORE": return BASIC_Keywords.RESTORE_Statement()
        return None

    def determineOperatorFromPart(self, part: str):
        if part == "+": return BASIC_Keywords.ADD_Operator()
        if part == "-": return BASIC_Keywords.SUB_Operator()
        if part == "*": return BASIC_Keywords.MULT_Operator()
        if part == "/": return BASIC_Keywords.DIV_Operator()
        if part == "^": return BASIC_Keywords.EXP_Operator() # subsitute an "up arrow" for a carrat
        if part == "=": return BASIC_Keywords.EQUAL_Operator()
        if part == "<>": return BASIC_Keywords.NOTEQUAL_Operator()
        if part == "<": return BASIC_Keywords.LESS_Operator()
        if part == "<=": return BASIC_Keywords.LESSEQUAL_Operator()
        if part == ">": return BASIC_Keywords.GREATER_Operator()
        if part == ">=": return BASIC_Keywords.GREATEREQUAL_Operator()
        if part == "(": return BASIC_Keywords.GROUPING_OPEN_Operator()
        if part == ")": return BASIC_Keywords.GROUPING_CLOSE_Operator()
        return None
    
    def determineFunctionFromPart(self, part: str):
        if part == "ABS": return BASIC_Keywords.ABS_Function()
        if part == "ATN": return BASIC_Keywords.ATN_Function()
        if part == "COS": return BASIC_Keywords.COS_Function()
        if part == "EXP": return BASIC_Keywords.EXP_Function()
        if part == "INT": return BASIC_Keywords.INT_Function()
        if part == "LOG": return BASIC_Keywords.LOG_Function()
        if part == "RND": return BASIC_Keywords.RND_Function()
        if part == "SIN": return BASIC_Keywords.SIN_Function()
        if part == "SQR": return BASIC_Keywords.SQR_Function()
        if part == "TAN": return BASIC_Keywords.TAN_Function()
        return None
    
    def determineLiteral(self, part: str) -> float:
        try:
            partNoDotOrDash = part.replace(".","").replace("-","")
            if len(partNoDotOrDash) > 9: return None # Numbers in BASIC cannot more than 9 digits!
            value = float(part)
            return value
        except ValueError as e: return None

    def determinePunctuation(self, part):
        if part == "\"": return BASIC_Keywords.QUOTE()
        if part == ";": return BASIC_Keywords.SEMICOLON()
        if part == ",": return BASIC_Keywords.COMMA()
        return None

    def breakDownParts(self, parts: list[str]) -> list:
        breakdown = []
        
        inQuote = False

        for i, part in enumerate(parts):
            if len(part) == 0: continue

            punctuation = self.determinePunctuation(part)
            if punctuation != None:
                if inQuote == False: breakdown.append(punctuation)

                if type(punctuation) == BASIC_Keywords.QUOTE:
                    if inQuote: inQuote = False
                    else: inQuote = True
                continue

            if inQuote == True:
                breakdown[-1].text += f" {part}"
                continue
            
            function = self.determineFunctionFromPart(part)
            if function != None:
                breakdown.append(function)
                continue
            statement = self.determineStatementFromPart(part)
            if statement != None:
                if type(statement) == BASIC_Keywords.REM_Statement:
                    return [statement] # dont continue this b/c it is a comment, but return something for the line number
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

            basicErrorMessage = "ILLEGAL INSTRUCTION"
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if part.startswith(letter) == False: continue
                basicErrorMessage = "ILLEGAL VARIABLE"
                break
            raise BASIC_Errors.UnknownKeyworkException(part, basicErrorMessage)
        
        if inQuote == True:
            raise BASIC_Errors.QuoteNotEndedException("Quote not ended!", "INCORRECT FORMAT")

        return breakdown

    # TODO: Check for each FOR loop that there is a NEXT statement for it, else throw "FOR WITHOUT NEXT"


    def parseProgramText(self, contents: str):
        # clear the program before we add stuff
        self.lines = {}
        self.linesText = {}

        hasEndInstruction = False
        previousLineNumber = -1
        contentLines = contents.split("\n")

        for i,line in enumerate(contentLines):
            if len(line) == 0: continue
            line = line.replace("(", " ( ")
            line = line.replace(")", " ) ")
            line = line.replace(",", " , ")
            line = line.replace(";", " ; ")
            line = line.replace("\"", " \" ")
            line = self.spaceOutOperations(line)

            parts = line.split(" ")
            lineNum = int(parts[0])
            BASIC_Errors.CurrentExecutionInformation.lineNumber = lineNum
            BASIC_Errors.CurrentExecutionInformation.lineText = line

            # todo: give them actual line numbers from the .bas file
            if previousLineNumber > lineNum: raise BASIC_Errors.LineOutOfOrderException(f"`{line}` | {previousLineNumber=} {lineNum=}", "THIS ISN'T REALLY AN ERROR JUST ME BEING EVIL AND NEEDING TO CHANGE THIS TO INSERT IN AN EDITOR")
            if self.lines.get(lineNum, None) != None: raise BASIC_Errors.LineRefedinitionException(f"Line {lineNum} is redefiend by: `{line}`", "THIS ISN'T REALLY AN ERROR JUST ME BEING EVIL AND NEEDING TO CHANGE THIS TO OVERWRITE IN AN EDITOR")
            
            keywords = None
            try: keywords = self.breakDownParts(parts[1:])
            except BASIC_Errors.UnknownKeyworkException as e:
                raise BASIC_Errors.UnknownKeyworkException(f"Unknown keyword `{e.message}`! `{line}`", e.basicErrorMessage)
            
            if keywords == None: raise Exception("Keywords is None??")
            if len(keywords) == 0: continue # REM comment probably caused this
            isEndInstruction = (type(keywords[0]) == BASIC_Keywords.STOP_Statement) or (type(keywords[0]) == BASIC_Keywords.END_Statement)
            if isEndInstruction:
                if i != len(contentLines)-1:
                    raise BASIC_Errors.PrematureENDException("END or STOP must be the last line of the program", "END IS NOT LAST")
                else: hasEndInstruction = True
            if type(keywords[0]) == BASIC_Keywords.DATA_Statement: keywords[0].execute(keywords) # have this line parse and set the data!

            programLine = BASIC_Line(lineNum, keywords)
            self.lines[lineNum] = programLine
            self.linesText[lineNum] = line
            previousLineNumber = lineNum

        if hasEndInstruction == False:
            raise BASIC_Errors.ExpectedKeywordTypeException("END or STOP Keyword not found in program! A program must contain either one at the end of their program!", "NO END INSTRUCTION")
        
        pass

