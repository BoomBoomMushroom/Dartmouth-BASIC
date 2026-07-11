import lexer
import BASIC_Keywords
import BASIC_Errors

class Interpreter:
    def __init__(self, programText: str=None, programFile: str=None):
        self.program = lexer.Lexer()
        self.programCounter: int = -1 # start at -1 because we increment PC first meaning our first pc fetch will be 0
        self.variables: dict[str, float] = {}
        self.programData: list[float] = []
        BASIC_Keywords.VARIABLE.VARIABLES = self.variables # Link up the two dicts
        BASIC_Keywords.BASIC_DATA.DATA = self.programData # Link up the two lists
        self.activeLoops: list[BASIC_Keywords.BASIC_Loop] = []
        self.returnStack: list[int] = []
        self.skippingLoopVarName = None

        # Lex the program AFTER we make the VARIABLES and DATA lists/dicts to not override
        if programFile: self.program.loadFile(programFile)
        elif programText: self.program.loadText(programText)

    def continueLoop(self, varName: str=None):
        stopIndex = -1

        for i in range(len(self.activeLoops)-1, -1, -1):
            loop: BASIC_Keywords.BASIC_Loop = self.activeLoops[i]
            if loop.variableName != varName: continue

            self.variables[loop.variableName] += loop.increment

            currentVal = self.variables[loop.variableName]        
            endLoop = False
            if loop.end > loop.start:
                if currentVal > loop.end: endLoop = True
            else:
                if loop.end > currentVal: endLoop = True

            stopIndex = i
            if endLoop == False:
                # we dont need to do +1 on setPc since it'll put us on the FOR line then our exec loop adds 1 itself
                self.programCounter = loop.setPc
                stopIndex += 1
            
            break

        if stopIndex == -1:
            raise BASIC_Errors.NotInForLoopException(f"No FOR loop found for variable \"{varName}\"!")
        # remove all loops spawned inside a higher loop. im assuming this is how it would work and it makes sense to me
        self.activeLoops = self.activeLoops[0:stopIndex]

    def RUN(self):
        while True:
            self.programCounter += 1
            executeLine = self.program.getLine(self.programCounter)
            if executeLine == None: continue # Line doesn't exist

            if self.skippingLoopVarName != None:
                currentRetVarName = executeLine.getLoopContinueVarName()
                # Variable names match, we have skipped the loop
                if currentRetVarName == self.skippingLoopVarName: self.skippingLoopVarName = None
                continue
            
            modifyData: BASIC_Keywords.BASIC_ReturnData = executeLine.execute()

            if modifyData.skipLoopVarName != None: self.skippingLoopVarName = modifyData.skipLoopVarName
            if modifyData.addAddressToReturnStack == True: self.returnStack.append(self.programCounter)
            if modifyData.pcSet != None:
                modifyData.pcSet = int(modifyData.pcSet)
                if self.program.getLine(modifyData.pcSet) == None:
                    raise BASIC_Errors.UndefinedLineException(f"Line number \"{modifyData.pcSet}\" not found in the program!")
                self.programCounter = modifyData.pcSet - 1 # minus 1 b/c our loop adds 1 immediately
            if modifyData.variableSet != None: self.variables[modifyData.variableSet[0]] = modifyData.variableSet[1]
            if modifyData.stopExecution == True: break
            
            if modifyData.returnToAddressFromReturnStack == True:
                if len(self.returnStack) == 0:
                    raise BASIC_Errors.NotInSubroutubeException("Not in subroutine so we cannot return from one!")
                self.programCounter = self.returnStack.pop()

            if modifyData.createdLoop != None:
                loop: BASIC_Keywords.BASIC_Loop = modifyData.createdLoop
                loop.setReturnPC(self.programCounter)
                self.activeLoops.append(loop)
            if modifyData.continueLoopVarName != None: self.continueLoop(modifyData.continueLoopVarName)


if __name__ == "__main__":
    interpreter = Interpreter(programFile="./program.bas")
    interpreter.RUN()

