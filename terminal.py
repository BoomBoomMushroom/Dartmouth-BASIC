import time
import os

from interpreter import Interpreter
import BASIC_Errors

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Teletype:
    def __init__(self):
        self.isInited = False
        self.lines: list[str] = []

        self.userNumber: int = 000000
        self.problemNumber: str = ""
        self.isType: bool = False

        self.commandLoop()

    def getProgram(self) -> str:
        noNone = [l for l in self.lines if l != None]
        out = "\n".join(noNone)
        return out

    def getFilePath(self) -> str: return f"./users/{self.userNumber}/{self.problemNumber}.bas"

    def getInput(self, message: str=""):
        out = input(message)
        return out

    def onCommand(self, message: str=""):
        msgUpper = message.upper()
        if msgUpper == "HELLO":
            if self.isInited == False: self.initialize()
            return
        elif self.isInited == False: return
    
        prgm = self.getProgram()
        if msgUpper == "RUN":
            try:
                print("\n", end="") # space it out
                t1 = time.time()
                interpreter = Interpreter(programText=prgm)
                t2 = time.time()
                seconds = int( t2-t1 )
                print(f"TIME: {seconds} SEC.")

                interpreter.RUN()
                print("\n", end="") # space it out
            
            except BASIC_Errors.BASIC_Exception as e:
                #print("basic error")
                print(bcolors.FAIL + e.basicErrorMessage + bcolors.ENDC)
            except Exception as e: raise e
        elif msgUpper == "LIST":
            # print out the current program
            print("\n"*1, end="")
            print(prgm)
            print("\n"*1, end="")
        elif msgUpper == "SAVE":
            path = self.getFilePath()
            os.makedirs(os.path.dirname(path), exist_ok=True) # force folders to exist
            with open(path, "w") as f:
                f.write(prgm)
                print("SUCCESSFULLY SAVED")
        elif msgUpper == "STOP":
            exit()
        else:
            # add this line to the program
            lineNum: int = 0
            try:
                lineNum = int(message.split(" ")[0])
            except:
                print("Error parsing line number!!", message)
                return
            if lineNum >= len(self.lines):
                # fill up the lines array w/ `None`s until we hit the size we need 
                self.lines.extend( [None] * ((lineNum+1) - len(self.lines)) )
            
            self.lines[lineNum] = message


    def commandLoop(self):
        while True:
            cmd = self.getInput()
            self.onCommand(cmd)

    def initialize(self):
        userNo: str = None
        while True:
            userNo = self.getInput("USER NO.--")
            if len(userNo) != 6:
                print("Enter your 6-digit user number!")
                userNo = None
                continue
            for char in userNo:
                if char in "0123456789": continue
                print("Make sure you only type digits 0-9!")
                userNo = None
                continue
            if userNo == None: continue
            self.userNumber = int(userNo)
            break
        
        problemNo: str = None
        while True:
            problemNo = self.getInput("PROBLEM NO.--")
            if len(problemNo) > 6:
                print("Problem numbers cannot be longer than 6 characters!")
                problemNo = None
                continue
            for char in problemNo:
                if char in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ": continue
                print("Make sure you only type letters and numbers! (A-Z, 0-9)")
                problemNo = None
                continue
            if problemNo == None: continue
            self.problemNumber = problemNo
            break

        print("SYSTEM--BASIC")

        typeOrOld = None
        while True:
            typeOrOld = self.getInput("TYPE OR OLD--").upper()
            if typeOrOld == "TYPE": self.isType = True
            elif typeOrOld == "OLD": self.isType = False
            else:
                print("Enter either \"TYPE\" or \"OLD\"")
                continue
            break

        self.isInited = True

        # If we type OLD, then we must fetch the program and load it into `self.lines`, then print "READY"
        if self.isType == False:
            path = self.getFilePath()
            if os.path.exists(path) == False:
                raise FileExistsError(f"File does not exist under {self.userNumber=}, {self.problemNumber=}")
            with open(path, "r") as f:
                self.lines = []
                lines = f.read().split("\n")
                for l in lines:
                    # run onCommand AFTER self.isInited=True so we can actually get past the init part
                    self.onCommand(l) # adds the line to the program

        print("READY.")


if __name__ == "__main__":
    t = Teletype()

