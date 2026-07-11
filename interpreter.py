import lexer
import BASIC_Keywords


programCounter: int = -1 # start at -1 because we increment PC first meaning our first pc fetch will be 0
program = lexer.Lexer("./program.bas")
variables = {}
BASIC_Keywords.VARIABLE.variables = variables # Link up the two dicts
activeLoops: list[BASIC_Keywords.BASIC_Loop] = []
returnStack: list[int] = []

def continueLoop(varName: str=None):
    global programCounter, activeLoops

    stopIndex = -1

    for i in range(len(activeLoops)-1, -1, -1):
        loop: BASIC_Keywords.BASIC_Loop = activeLoops[i]
        if loop.variableName != varName: continue

        variables[loop.variableName] += loop.increment

        currentVal = variables[loop.variableName]        
        endLoop = False
        if loop.end > loop.start:
            if currentVal > loop.end: endLoop = True
        else:
            if loop.end > currentVal: endLoop = True

        stopIndex = i
        if endLoop == False:
            # we dont need to do +1 on setPc since it'll put us on the FOR line then our exec loop adds 1 itself
            programCounter = loop.setPc
            stopIndex += 1
        
        break

    # remove all loops spawned inside a higher loop. im assuming this is how it would work and it makes sense to me
    activeLoops = activeLoops[0:stopIndex]


while True:
    programCounter += 1
    executeLine = program.getLine(programCounter)
    if executeLine == None: continue # Line doesn't exist

    modifyData: BASIC_Keywords.BASIC_ReturnData = executeLine.execute()

    if modifyData.addAddressToReturnStack == True: returnStack.append(programCounter)
    if modifyData.pcSet != None: programCounter = modifyData.pcSet - 1 # minus 1 b/c our loop adds 1 immediately
    if modifyData.variableSet != None: variables[modifyData.variableSet[0]] = modifyData.variableSet[1]
    if modifyData.stopExecution == True: break
    
    if modifyData.returnToAddressFromReturnStack == True: programCounter = returnStack.pop()

    if modifyData.createdLoop != None:
        loop: BASIC_Keywords.BASIC_Loop = modifyData.createdLoop
        loop.setReturnPC(programCounter)
        activeLoops.append(loop)
    if modifyData.continueLoopVarName != None: continueLoop(modifyData.continueLoopVarName)

