import lexer
import BASIC_Keywords


programCounter: int = -1 # start at -1 because we increment PC first meaning our first pc fetch will be 0
program = lexer.Lexer("./program.bas")
variables = {}
BASIC_Keywords.VARIABLE.variables = variables # Link up the two dicts

while True:
    programCounter += 1
    executeLine = program.getLine(programCounter)
    if executeLine == None: continue # Line doesn't exist

    modifyData: BASIC_Keywords.BASIC_ReturnData = executeLine.execute()
    if modifyData.pcSet != None: programCounter = modifyData.pcSet - 1 # minus 1 b/c our loop adds 1 immediately
    if modifyData.variableSet != None: variables[modifyData.variableSet[0]] = modifyData.variableSet[1]
    if modifyData.stopExecution == True: break

