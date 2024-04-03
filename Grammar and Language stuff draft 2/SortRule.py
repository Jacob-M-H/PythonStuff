

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
"""
class directedGraphMatrix:
    """X is the number of columns, Y is number of rows"""
    """X axis -> Y Axis Node."""
    strictMode=True #A debug tool to try. We'll see where it ends up later. Wrote a whole ton of code for safety and tooling. Try to break it later with unit tests.
    def __init__(self):
        self.x=0
        self.y=0
        self.Matrix=None
        self.legend=None
    def __init__(self,x:int, y:int, encoding=[]):
        self.x=self.setX(x)
        self.y=self.setX(y)
        if self.getX()<0 or self.getY()<0:
            self.Matrix=None
        else:
            self.Matrix=self.createMatrix(encoding)

    def __init__(self,x:int, y:int, encoding=[]):
        self.x=self.setX(x)
        self.y=self.setX(y)
        if self.getX()<0 or self.getY()<0:
            self.Matrix=None
        else:
            self.Matrix=self.createMatrix(encoding)

    #Additional Init's that include combinations between legends and x/y's. Also a square matrix init.
    


    def getMatrix(self)->list|None:
        return self.Matrix
    
    def setX(self, x)->int:
        if x<0:
            self.x=0
            return -1
        else:
            self.x=x
    def setY(self, y)->int:
        if y<0:
            self.y=0
            return -1
        else:
            self.y=y
    def getX(self)->int:
        return self.x
    def getY(self)->int:
        return self.y

    def isPosition(self, row, column):
        if self.Matrix!=None and row<self.getY() and column<self.getX():
            return True
        else:
            return False

    def createMatrix(self, encoding): 
        temp=[] 
        for i in range(self.getX()):# How many columns
            col=[encoding for i in range(self.getY())] #How many rows

    def getPosition(self, row, column)->tuple: #NOTE: Part of an experiment to make sure tuples act as I expect them to in python
        #TEST: a copy of good return[1] is mutable, but return[1] is not.
        """-1 is bad inputs."""
        if self.isPosition(self, row, column):
            return (0,self.getMatrix()[column][row])
        else:
            return (-1,[])
    
    def setPosition(self, row, column, encoding)->int:
        """-1 is bad inputs."""
        if self.isPosition(self, row, column):
            self.getMatrix()[column][row]=encoding
            return 0
        else:
            return -1
    def getColumn(self, column)->list|int:
        if self.isPosition(0, column):
            return self.getMatrix()[column]
        else:
            return -1 #Could perhaps give empty list, but this is more explicit.
    def getRow(self, row)->list|int:
        """Slightly more expensive than getColumn"""
        if self.isPosition(row, 0):
            return [self.getMatrix()[column][row] for column in range(self.getX())]
        else:
            return -1



    def _validateLegend(self, keyValues:dict, getRC:getX|getY)->bool:
        offendingValues=[]
        easyCheck=[0]*self.getRC()
 
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
        self.legendX=keyValues
    def _setLegendY(self, keyValues)->None:
        self.legendY=keyValues
    def getLegendX(self)->None|dict:
        return self.legendX
    def getLegendY(self)->None|dict:
        return self.legendY
    
    def LegendX(self, key):
        if self.getLegendX()!=None:
            try:
                return self.legendX[key]
            except KeyError as e:
                raise e        
    def LegendY(self, key):
        if self.getLegendY()!=None:
            try:
                return self.legendY[key]
            except KeyError as e:
                raise e
   
    def setLegend(self, keyValues:dict, getRC:getX|getY, setLegend="X"|"Y")->bool:
        """Key allows for fast mapping of a row or column to a particular pair of strings or objects"""

        if len(keyValues)-1>self.getRC(): #There might be some edge cases in which this is fine. For example EBNF maybe we want synonyms?
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
            self._validateLegend(keyValues, self.getRC)
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
    

def main(): 
    pass



if __name__=="__main__":
    main()
