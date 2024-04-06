import copy
import functools #for partial 

#TODO: Condense functionalities, like _Validates, as there is only a subfunctions worth difference. 
#TODO: Ensure that any higher order functionality makes use of the basic functionality to achieve additional features.
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
        #print("_setX")
        if x<0:
            self.x=0
            return -1
        else:
            self.x=x
            return 1
    def _setY(self, y)->int:
        #print("_setY")
        if y<0:
            self.y=0
            return -1
        else:
            self.y=y
            return 1
    def getX(self)->int:
        #print("getX")
        return self.x
    def getY(self)->int:
        #print("getY")
        return self.y

    def createMatrix(self, encoding=None): 
        #print("createMatrix") 
        temp=[] 
        columnNumber=self.getX()
        rowNumber=self.getY()
        for column in range(columnNumber):#How many columns 
            temp.append([encoding for row in range(rowNumber)] )#How many rows
        return temp

    def getMatrix(self)->list|None:
        #print("getMatrix") 
        return self.Matrix

    def isPosition(self, row, column):
        #print("isPosition") 
        if self.Matrix!=None and row<self.getY() and column<self.getX():
            return True
        else:
            return False
    def setPosition(self, row, column, encoding)->int:
        """-1 is bad inputs."""
        #print("setPosition") 
        if self.isPosition(row, column):
            self.getMatrix()[column][row]=encoding
            return 1
        else:
            return -1
    def getPosition(self, row, column)->tuple: #NOTE: Part of an experiment to make sure tuples act as I expect them to in python
        #TEST: a copy of good return[1] is mutable, but return[1] is not.
        """-1 is bad inputs."""
        #print("getPosition") 
        if self.isPosition(row, column):
            return (1,self.getMatrix()[column][row])
        else:
            return (-1,None)
    #TODO: let the index for the Dim functions optionally be a string. If a string send it into the legend to get the index.
    #TODO: if addrow/column is empty list, input a 0 along that row, or optional N/A arugment. At this point we should have a legend that keeps track of a N/A for a given column
        #Along with optional enforcements of type, like a function isType() that a user provides. So inputs must pass that internal type legend.

    #TODO: Stack changes. If at any point in the list of changes to do, a -1 or fail state is returned, revert the changes [or duplicate the object and only return the object when desired]. 
        #If revert is to be done, the set column/remove columns would have to record what certain values in a matrix are. In this case, we'd likely have a list of changes up to X amount of changes.
        #Eahc X change has a max change size of Dim+1^2 of matrix and a min size of dim-1^2 of a matrix. But if we allow the stack to hold onto as many a sthere are instrucitons, then we could implement an undo operation.
        #FUTURE: ^Maybe. Or the parent object we were talking about in the git which supports strong typing and validation functions to be provided.
    def getColumn(self, colIdx:int)->list|int:
        #print("getColumn") 
        if colIdx>-1 and colIdx<self.getX():
            return self.getMatrix()[colIdx]
        else:
            return -1 #Could perhaps give empty list, but this is more explicit.
    def getRow(self, rowIdx:int)->list|int:
        """Slightly more expensive than getColumn"""
        #print("getRow") 
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
            return -2
        if len(column)!=self.getY():
            print("colLen: ",len(column),", getY: ",self.getY())
            if directedGraphMatrix.strictMode:
                raise ValueError("Column has a different number of rows than the matrix!")
            return -3  
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
        #print("setColumn") 
        try:
            result=self._validateColumn(column, index)
            if result<0:
                return result
        except IndexError or ValueError as e:
            if directedGraphMatrix.strictMode: #Likely redundant.
                raise e
            else:
                return -2
        self.getMatrix().insert(index,column)

        return 1
    def setRow(self, row:list, index:int): 
        #print("setRow") 
        try:
            result=self._validateRow(row, index)
            if result<0:
                return result
        except IndexError or ValueError as e:
            if directedGraphMatrix.strictMode:
                raise e
            else:
                return -1 
        rowNum=0
        if index<self.getY():
            for col in self.getMatrix():
                col[index]=row[rowNum]
                rowNum+=1
            return 1
        else:
            return -1
    

    def addColumn(self, column:list, index=None)->int:
        """NOTE it seems that hte list sent in as it is an object will be 'consumed' when the underlying objects are mutated. This is a bigger issue than I want to handle, so for now I'll cheat it with a copy.deepcopy"""
         
        #print("addColumn") 
        if index==None:
            index=self.getX()
        try:
            result=self._validateColumn(column, index) #Validate column must not rely on getPositoin/isPosition to check column. Must cehck getY, and then if the index is within the getX, insert it, otherwise append it.
            print("Result of validate column: ", result)
            if result<0:
                return result
        except IndexError or ValueError as e:
            raise e
        copyCol=copy.deepcopy(column)
        self.getMatrix().insert(index, copyCol) #might need append if it doesn't like the exact end.
        self._setX(self.getX()+1)
        return 1
    def addRow(self, row:list, index=None)->int:
        #print("addRow") 
        if index==None:
            index=self.getY()
        try:
            result=self._validateRow(row, index)
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
        if index<self.getX() and index>-1:
            self.getMatrix().pop(index)
           
            self._setX(self.getX()-1)
            return 1
        else:
            return -1
    def removeRow(self, index:int)->int:
        print("removeRow")  
        if index<self.getY() and index>-1: 
            for col in self.getMatrix(): 
                col.pop(index) 
            self._setY(self.getY()-1)
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

        #print("__str__")
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
 

        #print("Matrix=\n", self.getMatrix())
        for row in range(rowNum):     
            for col in range(colNum):
                #print("Find row/col: ", row,"/",col, " in range rowNum/colNum: ", rowNum,"/",colNum)
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
            #print("head: ", head,", rowLimit: ",rowLimit)
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
 


class LegendParent:
    def _defaultValidation():
        return True
    

class LegendObj(LegendParent):
    def __init__(self, len, typeValidationFunc:function=LegendParent._defaultValidation):
        """Uniqueness is forced as all three require unique keys, which informs that we cannot have two strings to to the same idx, nor idx go to two strings. 1:1 and onto"""
        self.strToIdx={}
        self.idxToStr={} 
        self.idxToValidation={}
        for i in range(len):
            temp=str(i)
            self.idxToStr[i]=temp 
            self.idxToValidation[i]=typeValidationFunc
            self.strToIdx[temp]=i 
        

        pass
    
    def _validateKey(self, key:int|str)->bool:
            if type(key)=='int':
                if key in self.idxToStr.keys():
                    return True

            if type(key)=='string':
                if key in self.strToIdx.keys():
                    return True
                
            return False


    def getIntIdx(self, entry:str):
        return self.strToIdx[entry] 
    def getStr(self, idx:int):
        return self.idxToStr[idx]
    def getValid(self, idx:int|None, strKey:str|None=None):
        if idx!=None:
            return self.idxToValidation[idx]
        else:
            return self.getValid(self.strToIdx[strKey])

    def getInfo(self, key:int|str|None, idxKey:int|None=None, strKey:str|None=None)->tuple[int, str, function]:
        if idxKey!=None:
            return (idxKey, self.getStr(idxKey), self.getValid(idxKey, None))
        elif strKey!=None:
            return (self.getIntIdx(strKey), strKey, self.getValid(None, strKey))
        elif key!=None:
            if type(key)=='string':
                return self.getInfo(None, None, key)
            elif type(key)=='int':
                return self.getInfo(None, key, None)
        pass

    def setIntIdx(self, entry:str):
        pass
    def setStr(self, idx:int):
        pass
    def setValid(self, int, strKey):
        pass
 

    def setInfo(self, key:int|str|None, idxKey:int, strKey:str): 
        pass

        

    def swapLegendIdx(self, Key1:str|int, Key2:str|int):
        #Get their int versions
        K1idx, K1str, K1Val=self.getInfo(Key1)
        K2idx, K2str, K2Val=self.getInfo(Key2)
        #if no error thus far, good
        #check to ensure they are not referencing the same item
        if K1idx==K2idx:
            return True 
        self.idxToStr[K1idx]=K2str
        self.idxToValidation[K1idx]=K2Val
        self.idxToStr[K2idx]=K1str
        self.idxToValidation[K2idx]=K1Val       
        return True

    #If entry is str and exists, return false
    #If entry is int and exists, return false
    #if entry is not int or str, return false
    def extendLegend(self, entry:str|int, typeValidationFunc:function=LegendParent._defaultValidation):
        if type(entry)=="int" or type(entry)=="string": 
                pass
        else:
            return False

    
    


def main(): 
    
    
    import copy 
    def resetMatrices()->list:
        global testMatricesOldValues 
        return copy.deepcopy(testMatricesOldValues)
    
    def saveMatrices(testMatrices:list)->int:
        global testMatricesOldValues
        testMatricesOldValues=[]
        for matrix in testMatrices:
            testMatricesOldValues.append(copy.deepcopy(matrix)) 
        return 1
    
    def copyMatrix(matrix:directedGraphMatrix)->directedGraphMatrix: 
        #Need to add legend stuff and others. Not this simple. 
        newMatrix=directedGraphMatrix(0,0)
        for column in matrix.getMatrix():
            newMatrix.addColumn(column)
        return newMatrix



    directedGraphMatrix.strictMode=False
    #TEST: Initializations 
    emptyMatrix=directedGraphMatrix(0,0) 
    squareMatrixA=directedGraphMatrix(5,5)
    squareMatrixB=directedGraphMatrix(10,10) #TEST negatives, 0, non integers, and non square matrices. Be sure to try alterations of these like -1,5
    longRectangleMatrixC=directedGraphMatrix(10,5)
    tallRectangleMatrixD=directedGraphMatrix(5,10)

    negativeMatrixE=directedGraphMatrix(-1,-9) 
    negativeRowMatrixF=directedGraphMatrix(10,-5)
    negativeColMatrixF=directedGraphMatrix(-5,10) #7
    testMatrices=[emptyMatrix, squareMatrixA, squareMatrixB, longRectangleMatrixC, tallRectangleMatrixD, negativeMatrixE, negativeRowMatrixF, negativeColMatrixF] 
    

if __name__=="__main__":
    main()
