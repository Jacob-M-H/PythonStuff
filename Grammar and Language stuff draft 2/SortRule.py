

class ruleObj():
    def __init__(self, ruleName):
        self.name=ruleName
        self.cases=[]
        self.rank=(None,None,None)


    def addCase(self, matchCase:list|str): 
        if type(matchCase)!=type([]): #enforce case must be a list 
            if type(matchCase)!=type(''): 
                return -1 
            self.cases.append([int(item) for item in matchCase.split(" ")]) #3/13 should result in a list of symbols
            return 0
        else:
            for symbol in matchCase:
                if type(symbol)!=type(1):
                    print('Warning, matchCase iterable is not of type int')
            self.cases.append(matchCase) #assume's the array is of type int
 
        if matchCase==[]: #enforce matchCase cannot be empty list
            return -1
         
        for case in self.cases:
            if case==matchCase:
                return 0
        self.cases.append(matchCase)

        return 0

        #3/13 TODO: clever way of resorting the one case - a less generalized version of sortRules?
        #3/13 TODO: add case to a specific rule?
    def _replaceCases(self, cases):
        self.cases=cases

    def __str__(self):
        #3/13 Could memoize the join maybe... Better not unless we make a wrapper function for it
        cases="".join(["\t"+" ".join(case)+"\n" for case in self.cases])
        return self.name+":\n"+"Rank: "+self.rank+"\nCases:\n"+cases 
   
ruleCollection={}


"""Note on ENBF, I haven't figured out how the theory jives with optional and more arguments. I'm hoping the matrix stuff will lead to some revelation. Additionally it will be likely that earlier 
        []+ or {}+ are more important than later ones, as if they fail then it should be quickly be able to fail the next ones (ideally) or get a longer string.
            May enforce EBNF with [] and {} at the end of each case. I'll have to see if there exists a reason why that wouldn't work, or if other forms can be expressed as such.
                It'd be awesome if my college gave a class on this before I graduated, but I'm pretty sure its master level. 
"""

"""We want to ensure that the grammar rules are sorted from most abstract to least abstract. [or reversed if the object creation and datastructures prefer]"""
""" 
Problem definition:
1.Sort rule Objs by 'depth', from most abstract to least
    1.a Depth in this case means the maximum number of rules required to reach a completely atomic/literal definition of that rule.
2.'Most Abstract' means # atoms, termianls & worst/longest case for rules used. Longest case includes the max length of the same of each rule in a case.
3. Want to avoid cyclic lookups. Exp: Rule A: Rule B, Rule B: Rule A. This requires two additional structures or values to keep track of evaluation and seen flags.
    3.a In the event of cyclic [not necessarily bad depending on implementation desires], either report the traceback of ruleName->case->rule->case->RuleName. Either bold or italics or other indicator of the closed loop.
    3.b In the event cyclic definitions are fine, 1 meta data must have a config defining max depth of such a case... 
    3.c Or 2, a case must must exist which does not result in cylic behavior. [as it is implied that an infinite input is not allowed or can be worked around]
    3.d In either case, if additional cases do not resolve and end up in cyclic behavior, report all offending cases. Note that each case for a rule must be evaluated [either way for checking cyclic or min max depth], and if evaluated and finished, great it's a fetch, else it'll either end and resolve the rule, or discover a cylicsm.
4. Every rule must end in terminals or atoms/consist at a macro level (if extended via only terminals and atoms, is it possible?) This is a warning.
    4.a If enforced, declare offending rule, [cyclic, case may exist which terminates, simply it means the rank is not determinate, except for a 'better case', and it's depth may still be definable simply by the max between the two of each of the cases that do terminate. Implies siblings]. 
    4.b If unenforced, [cyclic, and case does not exist which ends cycle].
5. Raise errors where cyclism occurs [and note extremit] along with trace of ruleName->case with rule outlined-> rule -> case with ruleName defined-> ... until cycle is completed at least once. Does not guantee every case is caught within the specific error. Multiple runs may be required to discover each incident.
6. Algorithm is not garunteed sorted cases [This may change, as sorting cases when not in EBNF and without REGEX expressions to muddle the waters should be posible. Additionally sorted cases by length may not result in longest match as current sort algorithm only takes by number of tokens, not number of termianls/atoms]
7. Algorithm may assume Atoms and terminals can be determined [rule names with cases that are only termianls, and the ruleName 'Atom' or some variant there of.]
8. Thought last night about if two cases matched literals/atoms, it doesn't necessarily mean ambiguity if they appear in seperate parent cases. In this case, we need to store which cases *could* be ambiguious, and detect whether either 1. Parents of each case are themselves ambiguious and 2. They are sibling cases with no other demarkation [like an additional literal].


This will be an ugly, ugly algorithm. Finding a root may be quick, if we simply make every 'seen' rule within a case not available for the position, but then if there is a multi root tree it'll be problematic.

"""


"""There is a high possiblity of needing to use a directed graph to compare quickly, especially when it comes to finding roots. 
[which may not be true 'roots' of a tree, but the most appropriate place to enter the grammar graph]
    A first pass algorithm will be attempted, and it will have both recursive and linear operations, and will attempt to resolve each case in turn, but each recursion should knock out a few 
        rule obj to test o rthrow a cyclic error/warning. 

    Due to performance considerations, there will not be multiple initalization options. While C++ and Java allow method overloading, Pythons method overloading would be allowable with register/singledispatchmethod but it seems it'd take a large performance hit.
        It should be fine...
"""


class directedGraphMatrix:
    """X is the number of columns, Y is number of rows"""
    """X axis -> Y Axis Node."""
    strictMode=True #A debug tool to try. We'll see where it ends up later. Wrote a whole ton of code for safety and tooling. Try to break it later with unit tests.
    
    def __init__(self,x:int, y:int, encoding=None)->None:
        print("\n\n\n")
        print("init")
        x=self._setX(x)
        y=self._setY(y) 
        self.legendX=None
        self.legendY=None
        self.Matrix=self.createMatrix(encoding)
        if x<0 or y<0:
            if directedGraphMatrix.strictMode:
                raise ValueError("x or y are negative. Expect x>=0 and y>=0") 
        return None
        

    def _setX(self, x)->int:
        print("_setX")
        if x<0:
            self.x=0
            return -1
        else:
            self.x=x
            return 1
    def _setY(self, y)->int:
        print("_setY")
        if y<0:
            self.y=0
            return -1
        else:
            self.y=y
            return 1
    def getX(self)->int:
        print("getX")
        return self.x
    def getY(self)->int:
        print("getY")
        return self.y

    def createMatrix(self, encoding=None): 
        print("createMatrix") 
        temp=[] 
        columnNumber=self.getX()
        rowNumber=self.getY()
        for column in range(columnNumber):#How many columns 
            temp.append([encoding for row in range(rowNumber)] )#How many rows
        return temp

    def getMatrix(self)->list|None:
        print("getMatrix") 
        return self.Matrix

    def isPosition(self, row, column):
        print("isPosition") 
        if self.Matrix!=None and row<self.getY() and column<self.getX():
            return True
        else:
            return False
    def setPosition(self, row, column, encoding)->int:
        """-1 is bad inputs."""
        print("setPosition") 
        if self.isPosition(row, column):
            self.getMatrix()[column][row]=encoding
            return 1
        else:
            return -1
    def getPosition(self, row, column)->tuple: #NOTE: Part of an experiment to make sure tuples act as I expect them to in python
        #TEST: a copy of good return[1] is mutable, but return[1] is not.
        """-1 is bad inputs."""
        print("getPosition") 
        if self.isPosition(row, column):
            return (1,self.getMatrix()[column][row])
        else:
            return (-1,None)
    #TODO: let the index for the Dim functions optionally be a string. If a string send it into the legend to get the index.
    #TODO: if addrow/column is empty list, input a 0 along that row, or optional N/A arugment. At this point we should have a legend that keeps track of a N/A for a given column
        #Along with optional enforcements of type, like a function isType() that a user provides. So inputs must pass that internal type legend.
    def getColumn(self, colIdx:int)->list|int:
        print("getColumn") 
        if colIdx>-1 and colIdx<self.getX():
            return self.getMatrix()[colIdx]
        else:
            return -1 #Could perhaps give empty list, but this is more explicit.
    def getRow(self, rowIdx:int)->list|int:
        """Slightly more expensive than getColumn"""
        print("getRow") 
        if rowIdx>-1 and rowIdx<self.getY():
            return [self.getMatrix()[column][rowIdx] for column in range(self.getX())]
        else:
            return -1

    def _validateColumn(self, column:list, index:int=0)->int:
        print("_validateColumn") 
        if index<0 or index>self.getX():
            if directedGraphMatrix.strictMode:
                raise IndexError("Column replacement is outside of range!")
            return -1  
        if self.getMatrix()==None:
            if directedGraphMatrix.strictMode:
                raise ValueError("No Matrix found")
            return -1
        if len(column)!=self.getY():
            if directedGraphMatrix.strictMode:
                raise ValueError("Column has a different number of rows than the matrix!")
            return -1  
        return 1
    def _validateRow(self, row:list, index:int=0):
        print("_validateRow")   
        if index<0 or index>self.getY():
            if directedGraphMatrix.strictMode:
                raise IndexError("Row replacement is outside of range!")
            return -1
        if self.getMatrix()==None:
            if directedGraphMatrix.strictMode:
                raise ValueError("No Matrix found")
            return -1
        if len(row)!=self.getX():
            if directedGraphMatrix.strictMode:
                raise ValueError("Row has a different number of columns than the matrix!")
            return -1
        return 1
    def setColumn(self, column:list, index:int)->int: 
        print("setColumn") 
        try:
            result=self._validateColumn(column, index)
            if result<0:
                return result
        except IndexError or ValueError as e:
            if directedGraphMatrix.strictMode: #Likely redundant.
                raise e
            else:
                return -2
        self.getMatrix()[index]=column
        return 1
    def setRow(self, row:list, index:int): 
        print("setRow") 
        try:
            result=self._validateColumn(row, index)
            if result<0:
                return result
        except IndexError or ValueError as e:
            if directedGraphMatrix.strictMode:
                raise e
            else:
                return -1 
        rowNum=0
        for col in self.getMatrix():
            col[index]=row[rowNum]
            rowNum+=1
        return 1
    def addColumn(self, column, index=None)->int:
        print("addColumn") 
        if index==None:
            index=self.getX()
        try:
            result=self._validateColumn(column, index) #Validate column must not rely on getPositoin/isPosition to check column. Must cehck getY, and then if the index is within the getX, insert it, otherwise append it.
            if result<0:
                return result
        except IndexError or ValueError as e:
            raise e
        self.getMatrix().insert(index, column) #might need append if it doesn't like the exact end.
        self._setX(self.getX()+1)
        return 1
    def addRow(self, row, index=None)->int:
        print("addRow") 
        if index==None:
            index=self.getY()
        try:
            result=self._validateColumn(row, index)
            if result<0:
                return result
        except IndexError or ValueError as e:
            raise e
        rowNum=0
        for col in self.getMatrix():
            col.insert(index, row[rowNum])
            rowNum+=1
        self._setY(self.getY()+1)
        return 1
    def removeColumn(self, index:int)->int:
        print("removeColumn") 
        if index<self.getX() and index>0:
            self.getMatrix().pop(index)
            return 1
        else:
            return -1
    def removeRow(self, index:int)->int:
        print("removeRow") 
        if index<self.getY() and index>0:
            for col in self.getMatrix(): 
                col.pop(index)
            return 1 
        else:
            return -1

    
    def _validateLegend(self, keyValues:dict, getRC="X" or "Y")->bool: #This one will need unit tests for sure
        print("_validateLegend") 
        offendingValues=[]
        expectedValueAmount=0
        errorString=""
        if getRC=="X": 
            expectedValueAmount=self.getX()
        elif getRC=="Y":
            expectedValueAmount=self.getY()
        else:
            if directedGraphMatrix.strictMode:
                errorString="getRC expected to be either \"X\" or \"Y\", not " + str(getRC)
                raise ValueError(errorString)
            return False

        easyCheck=[0]*expectedValueAmount
 
        for value in keyValues.values():
            if type(value)!="int":
                raise ValueError("Values for legend are not integers! Offending value: ", value)
            if value>0 and value<len(easyCheck):
                easyCheck[value]=1
            else:
                offendingValues.append(value)
        #Ensure all values are within range of hte matrix [even if there are duplicates]
        #If value is not within range, raise error printing offending values.
        if len(offendingValues)>0:
            if directedGraphMatrix.strictMode:
                errorString="keyValues have values that exist outside of the column values. Offending values: "+str(offendingValues)+"</>"+str(self.getX())
                raise IndexError(errorString)
            else:
                #Enforced, as bad values would cause errors elsewhere.
                return False
        else:
            if sum(easyCheck)!=len(easyCheck):
                if directedGraphMatrix.strictMode:
                    badIdx=[]
                    for i in range(len(easyCheck)):
                        if (not easyCheck[i]): 
                            badIdx.append(i)
                    errorString="There exists unreachable columns via legend! Offending indices: "+str(badIdx)
                    raise IndexError(errorString)
                else:
                    badIdx=[]
                    for i in range(len(easyCheck)):
                        if (not easyCheck[i]): 
                            badIdx.append(i)
                    print("Some Indicies may not be reachable using legend. Indicies unreachable using legendX: "+str(badIdx))
                    #Return false not enfored here, as additional space may have been allocated for later dictionary use.
        return True

    def _setLegendX(self, keyValues)->None:
        print("_setLegendX") 
        self.legendX=keyValues
    def _setLegendY(self, keyValues)->None:
        print("_setLegendY") 
        self.legendY=keyValues
    def getLegendX(self)->None|dict:
        print("getLegendX") 
        return self.legendX
    def getLegendY(self)->None|dict:
        print("getLegendY") 
        return self.legendY

    def LegendX(self, key):
        print("LegendX") 
        if self.getLegendX()!=None:
            try:
                return self.legendX[key]
            except KeyError as e:
                raise e        
    def LegendY(self, key):
        print("LegendY") 
        if self.getLegendY()!=None:
            try:
                return self.legendY[key]
            except KeyError as e:
                raise e

    def setLegend(self, keyValues:dict, setLegend="X" or "Y")->bool:
        """Key allows for fast mapping of a row or column to a particular pair of strings or objects"""
        print("setLegend") 
        dimLen=0
        errorString=""
        if setLegend=="X":
            dimLen=self.getX()
        elif setLegend=="Y":
            dimLen=self.getY()
        else:
            if directedGraphMatrix.strictMode:
                errorString="Expected setLegend \"X\" or \"Y\", received "+str(setLegend)
                raise ValueError(errorString)
            return False
        
        
        if len(keyValues)-1>dimLen: #There might be some edge cases in which this is fine. For example EBNF maybe we want synonyms?
            if directedGraphMatrix.strictMode:
                raise IndexError("Too many Keys for the values in the Legend")
            else:
                warnHead="Warning, there may exist too many key values for accessing unique "
                warnBack=" in the matrix."
                if setLegend=="X":
                    print(warnHead+"columns"+warnBack)
                if setLegend=="Y":
                    print(warnHead+"rows"+warnBack)
                
        try:
            self._validateLegend(keyValues, setLegend)
            if setLegend=="X":
                self._setLegendX(keyValues)
            if setLegend=="Y":
                self._setLegendY(keyValues)
        except IndexError as e:
            if directedGraphMatrix.strictMode:
                raise e
            print(e)
            return False
        except ValueError as e:
            if directedGraphMatrix.strictMode:
                raise e
            print(e) 
            return False
        
        return True

    def getLegends(self)->tuple:
        print("getLegends")
        return (self.getLegendX(), self.getLegendY())

    #TODO: insert |, +, and - to create ASCII table borders, optionally.
    def __str__(self, minPad:int=0, optionalJustify:int=1, optionalCellNA:str="", optionalCellDefault=None, optionalDefaultXLabels:bool=False, optionalDefaultYLabels:bool=False)->str:
        """Justify 0: no justificaiton\nJustify 1: Left just\nJustify 2: Right Just\nJustify 3: center. Other integers treated as 0."""
        """X/Y label defaults "", on True labels with integers."""

        print("__str__")
        rowNum=self.getY()
        colNum=self.getX()
        #TODO, preallocate the sizes required via row num and col num
        resultStrings=[] #cells 
        formatLegendX=[0]*colNum #keys
        formatLegendY=[0]*rowNum #keys
        finalResultString=""
        padding=max(minPad,len(optionalCellNA)) #TODO: allow str to have optional integer argumetn for different types of padding or no padding.
        legendX=self.getLegendX()
        legendY=self.getLegendY() 

        def figurePadding(strValue:str, padding:int):
            strLen=len(strValue)
            if padding<strLen: 
                return strLen
            return padding 
        def padString(pad:int, string:str, opt:int=0):
            if opt==0:
                return string
            if opt==1:
                return string.ljust(pad, " ")
            if opt==2:
                return string.rjust(pad, " ")
            if opt==3:
                return string.center(pad, " ")
            return string
            
        if legendX!=None:
            for key in legendX.keys(): 
                if formatLegendX[legendX[key]]==0:
                    keyString=str(key)
                    formatLegendX[legendX[key]]=keyString
                    padding=figurePadding(keyString, padding)
                else:
                    formatLegendX[legendX[key]]+="/"+str(key)    
                    keyString=formatLegendX[legendX[key]]
                    padding=figurePadding(keyString,padding)
        else:
            if optionalDefaultXLabels:
                #Integer implementaiton
                for i in range(colNum):
                    formatLegendX[i]=str(i)
                padding=figurePadding(str(colNum), padding)
        if legendY!=None:
            for key in legendY.keys(): 
                if formatLegendY[legendY[key]]==0:
                    keyString=str(key)
                    formatLegendY[legendY[key]]=keyString
                    padding=figurePadding(keyString, padding)
                else:
                    formatLegendY[legendY[key]]+="/"+str(key)  
                    keyString=formatLegendY[legendY[key]]
                    padding=figurePadding(keyString,padding)      
        else: 
            if optionalDefaultYLabels:
                #Integer implementaiton
                for i in range(rowNum):
                    formatLegendY[i]=str(i)
                padding=figurePadding(str(rowNum), padding)
 

        print("Matrix=\n", self.getMatrix())
        for row in range(rowNum):     
            for col in range(colNum):
                print("Find row/col: ", row,"/",col, " in range rowNum/colNum: ", rowNum,"/",colNum)
                strValue=str(self.getPosition(row, col)[1])
                padding=figurePadding(strValue, padding)
                resultStrings.append(strValue)

        #Prefix with whitespace with padding to account for Y legend
        finalResultString+=padString(padding, "", 1)
        for key in formatLegendX:
            if key==0:  
                finalResultString+=padString(padding, "", 1) 
            else:
                finalResultString+=padString(padding, key, optionalJustify)  
        
        if len(finalResultString)>0:
            finalResultString+="\n"

        head=0 
        rowHead=1
        #print("result string len: ", len(resultStrings)) #empty if no values. 
        #print("X/Y len: ", colNum, "/",rowNum)
        #print("formatLegend X/Y: \n",formatLegendX,"\n",formatLegendY)
        #print("padding: ", padding)
        for key in formatLegendY:
            #append key, or whitespace
            if key==0:
                finalResultString+=padString(padding, "", 1) 
            else:
                finalResultString+=padString(padding, key, optionalJustify) 
            rowLimit=colNum*rowHead 
            print("head: ", head,", rowLimit: ",rowLimit)
            for head in range(head, rowLimit): 
                if resultStrings[head]==str(optionalCellDefault):
                    finalResultString+=padString(padding, optionalCellNA, optionalJustify)
                else:
                    finalResultString+=padString(padding, resultStrings[head], optionalJustify)  
            head=rowLimit
            rowHead+=1 
            finalResultString+="\n" 
 
        return finalResultString
  
    def prettyPrint(self, minPad:int=0, optionalJustify:int=1, optionalCellNA:str="N/A", optionalCellDefault=None, optionalDefaultXLabels:bool=True, optionalDefaultYLabels:bool=True ,replaceGenericX:bool=True, replaceGenericY:bool=True)->str:
        #During formatX, prepend with "|"
        #after loop suffix "|"
            #as usual suffix "\n"
        #create a str line '-', we'll replace the [1] with a +.
            #suffix with "\n"
        #for formatY 
            #key +="|"
            #result String suffix with "|"
        #pad then suffix!
        
        #When combining each
        #formatX + flatLine w/ [1]="+", + formatY Row with Cell Row + flatLine until completed.

        #Note that a boolean was created so that if there exists a [0] still, it should be replaced with it's integer position.
        pass
    def isMatrixEmpty(self, identity=None)->bool:
        #return True if empty, false if any populated
        pass
    def isMatrixComplete(self, askColumn:bool=True, index:list=[], identity:list=None)->bool:
        #return true if all entries are not of an identity
        #boolean checks by row or column 
        #list must be as long as identity, and idex list must be unique, and have no index out of matrix range.
        #implement same logic for is empty.
        pass


def nonZeroDimensions(matrix:directedGraphMatrix, testIteration=0): 
    print("Matrice test, nonZeroDimensions: "+str(testIteration)) 
    if matrix.getX()<0:
        raise ValueError("Negative X dimensions!")
    if matrix.getY()<0:
        raise ValueError("Negative Y dimensions!")
    
def notNoneMatrix(matrix:directedGraphMatrix, testIteration=0):
    print("Matrice test, nonZeroDimensions: "+str(testIteration))
    if matrix.getMatrix()==None:
        raise ValueError("Expected Matrix not None")
    print(matrix.getMatrix())

def printMatrix(matrix:directedGraphMatrix, testIteration=0):
    print("Matrice test, printMatrix: "+str(testIteration))
    try:
        resultString=matrix.__str__(0, 1, "N/A", None, True, True)
        print(resultString, "\n Len(resultString): ",len(resultString))
    except:
        raise ValueError("Something went wrong with the __Str__ function")

def testPositionFunc(matrix:directedGraphMatrix,x:int=0,y:int=0,value=None,testIteration:int=0):
    print("Checking for position : (",x,", ",y,")")
    print("Matrix X/Y: ", matrix.getX(), "/", matrix.getY())
    print("Matrix: \n",matrix.__str__(0, 1, "N/A", None, True, True))
    print("Matrix has position? :", matrix.isPosition(x,y))
    print("Matrix get position? :", matrix.getPosition(x,y))
    print("Matrix set position? :", matrix.setPosition(x,y, value))
    print("Matrix after attempted changes: \n", matrix.__str__(0, 1, "N/A", None, True, True))

def testDimensionFunc(matrix:directedGraphMatrix, dim:bool=True, add:list=[], addIdx:int=None, replacement:list=[], setIdx:int=None, remove:int=None, testIteration=0):
    #print matrix.
    #dim =True is column, False is row
    
    #add inserts 'add' to the matrix [either end of row or end of columsn] seperate test to try specific indexes
    #replacement 'replaces' a dim in the matrix [let's have the index match that of inserts].
    print("Test ", testIteration)
    input("continue?")
    beforeChanges=matrix.__str__(0, 1, "N/A", None, True, True)

    if dim: #add/remove column
        
        #0,0 #Replace row should just use addColumn/remove column. 
        print("add Column, ", matrix.addColumn(add,addIdx)) #expect failure  
        print("set Column, ", matrix.setColumn(replacement,setIdx)) #expect failure 
        #print("rem Column, ", matrix.removeColumn(remove)) #expect failure 
    

    else: #add/remove row
        print("add Row ", matrix.addRow(add,addIdx)) #expect failure
        print("set Row ", matrix.setRow(replacement,setIdx)) #expect failure
        #print("rem Row ", matrix.removeRow(remove))  #expect failure 

    afterChanges=matrix.__str__(0, 1, "N/A", None, True, True)
    input("See matrix "+str(testIteration)+"?")
    print("Before:\n", beforeChanges)
    print("After:\n",  afterChanges)
    input("continue?")

    pass

def testSweep(matrixList, func):
    testIteration=0
    for matrix in matrixList:
        try: 
            func(matrix=matrix,testIteration=testIteration)
        except ValueError or IndexError as e:
            print(e)  
        testIteration+=1 
    


def main(): 
    directedGraphMatrix.strictMode=False
    #TEST: Initializations 
    emptyMatrix=directedGraphMatrix(0,0) 
    squareMatrixA=directedGraphMatrix(5,5)
    squareMatrixB=directedGraphMatrix(10,10) #TEST negatives, 0, non integers, and non square matrices. Be sure to try alterations of these like -1,5
    longRectangleMatrixC=directedGraphMatrix(10,5)
    tallRectangleMatrixD=directedGraphMatrix(5,10)

    negativeMatrixE=directedGraphMatrix(-1,-9) 
    negativeRowMatrixF=directedGraphMatrix(10,-5)
    negativeColMatrixF=directedGraphMatrix(-5,10)
    testMatrices=[emptyMatrix, squareMatrixA, squareMatrixB, longRectangleMatrixC, tallRectangleMatrixD, negativeMatrixE, negativeRowMatrixF, negativeColMatrixF]
    #legendA={"Set":0, "Group":1, "Ring":2, "Monoid":3, "Magma":4, "Semi-Group":5}
    #legendB={"Numeric Algebra":0, "Variable Algebra":1, "Trig":2, "Calc":3, "Real Algebra":4, "Abstract Algebra":5, "Elliptical Curve Crypt":6, "Probability Theory":7, "Statistics":8,"Linear Algebra":9}
    #legendC={"A":1,"B":2,"C":3,"D":4, "E":5} #TEST, negatives, positives beyond index of the x/y, 0s, and multiple equal values, such as "E":5, "F":5.
    #testSweep(testMatrices, nonZeroDimensions)
    
    #testSweep(testMatrices, notNoneMatrix)
    
    #testSweep(testMatrices, printMatrix) #TODO: Need to make doc string explaining optional parameters. Need to test more complete functionality. Use functools partial to test otional parameters.
    import functools #for partial 
    testSweep(testMatrices, functools.partial(testPositionFunc,x=0,y=0,value=000))
    #to distinquish columsn and rows. 
    testSweep(testMatrices, functools.partial(testPositionFunc, x=4, y=4, value=404))
    testSweep(testMatrices, functools.partial(testPositionFunc, x=3, y=3, value=303))
    testSweep(testMatrices, functools.partial(testPositionFunc, x=2, y=2, value=202))
    testSweep(testMatrices, functools.partial(testPositionFunc, x=1, y=1, value=101)) 

    #TODO: Legend tests, row/column operations.
        #If insert row/column extends well beyond a matrix. In strictmode, index error, if not strict mode, append upto and including that index with a default N/A value (optional, otherwise default to None)
        #Row column tests first
            #to distinquish columsn and rows. 

    dimA=["a","b","c","d","e"]
    dimB=["1","2","3","4","5"]
    dimC= ["a","b","c","d","e","f","g","h","i","j"]
    dimD = ["1","2","3","4","5","6","7","8","9","10"]
    testSweep(testMatrices, functools.partial(testDimensionFunc, dim=True, add=dimA, addIdx=0, replacement=dimB, setIdx=1, remove=2 ))  
    #expecting cols: dimaA, dimB, 303, 404, if no erorrs

#def testDimensionFunc(matrix:directedGraphMatrix, dim:bool=True, add:list=[], addIdx:int=None, replacement:list=[], setIdx:int=None, remove:int=None)


    #TODO: When adding a row or column have an optional column or row legend name. [and on strict mode default when creation with numbers for row and columns]
    #TODO: When replacing a column or row, allow for the row or column to be replaced
    #TODO: Function to replace existing column or row name in legend


    pass



if __name__=="__main__":
    main()
