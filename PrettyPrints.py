 
class TestStuff: #Test getsublist
    one=1
    two=2
    three=3
    sub=[[1,2,3,4,5]]
    def __init__(self):
        a="A"
        b="B"
        c="C"
    def testOut(self):
        temp=self.a+self.b+self.c
        temp2=str(self.one)+str(self.two)+str(self.three)
        return temp+" "+temp2
    def getSublistStuff(self):
        return self.sub
    
class TestStuff2: #test non sublist function handling it
    ten=10
    twenty=20
    thirty=30
    sub=[[1,2,3,4,5]]
    def __init__(self):
        aa="A"
        bb="B"
        cc="C"
    def testOut(self):
        temp=self.a+self.b+self.c
        temp2=str(self.one)+str(self.two)+str(self.three)
        return temp+" "+temp2 

class TestStuff3: #Test str()
    ten=10
    twenty=20
    thirty=30
    sub=[[1,2,3,4,5]]
    def __init__(self):
        aa="A"
        bb="B"
        cc="C"
    def testOut(self):
        temp=self.a+self.b+self.c
        temp2=str(self.one)+str(self.two)+str(self.three)
        return temp+" "+temp2 
    def __str__(self):
        return str(self.ten)+" "+str(self.twenty)+" "+str(self.thirty)+"\n"




def prettyPrintMatrix(matrix): 
    formatString="[{:{}}] "
    #stringMatrix=[[None]*len(matrix[0])]*len(matrix)   #THIS IS PROBLEMATIC Note that it clones teh data structure reference wise! So it's actually 1 column! GROSS
    print("PPMatrix start")

    #This can be made better
    stringMatrix=[]
    for col in matrix:
        stringMatrix.append([])
        for row in col:
            stringMatrix[len(stringMatrix)-1].append(None)

    #(matrixValue, leftJustifyAmt=maxincolumn)
 
    for colIdx in range(len(matrix)):
        col=matrix[colIdx]
        largestString= max(  map(len, map(str, col) )  ) 
        for rowIdx in range(len(col)):  
            temp=formatString.format(matrix[colIdx][rowIdx], largestString)   
            stringMatrix[colIdx][rowIdx]=temp 
    print("String matrix made <- can improve just by converting right then and appending to a string?")

    #Print each row   
    #print(stringMatrix[0][0], stringMatrix[1][0], stringMatrix[2][0],"\n", stringMatrix[0][1], stringMatrix[1][1], stringMatrix[2][1]) <-expectation sample 
     
    rowNum=len(stringMatrix[0])
    colNum=len(stringMatrix)
    temp=""
    for row in range(rowNum):
        for col in range(colNum):
            temp+=" "+stringMatrix[col][row]
        temp+="\n"
    
    print("String made")


    print("Finished up")
    return temp
    


def splitStringArrayBalancedRecord(line:str, splitLine=None):
    """Takes a string of the form [stuff, stuff, ..., stuff]. Splits it into 'stuff' by a given by a splitline, for example ',' """
    line=line.strip()
    

    pair=[] #[idxStart, idxEnd, brackets]
    stack=[]#[index, bracket]
    for idx in range(len(line)):
        if line[idx] in ["(", "{", "["]:
            stack.append([idx, line[idx]])
        else:
            if stack:
                if line[idx] in [")","]","}"]:
                    if (stack[-1][1]=="(" and line[idx]==")") or (stack[-1][1]=="[" and line[idx]=="]") or (stack[-1][1]=="{" and line[idx]=="}"):
                        pair.append([stack[-1][0], idx, line[stack[-1][0]:idx+1]])  
                        stack.pop()
                    else:
                        raise SyntaxError("Mismatched Brackets")
            else:
                if line[idx] in [")","]","}"]:
                    raise SyntaxError("Unbalanced Brackets")

    if stack: #Stack should've been consumed entirely
        raise SyntaxError("Mismatched Brackets or Unbalanced Brackets")

    return pair, line

def splitStringArray(line:str, splitLine=","): 
    #Note on using, it will return an array wrapping the parsed array/list.
        #Thus when wanting to get the info of the data you must delist it.
    startIdx=0
    while startIdx<len(line) and line[startIdx] not in ["(", "{", "["]:
        if line[startIdx] in [")","]","}"]:
            raise SyntaxError("Unbalanced Brackets")
        startIdx+=1
    if startIdx==len(line)-1: #[/{/( exist, but theres no posible match
        raise SyntaxError("Unbalanced Brackets") 
    
    if startIdx==len(line): #This is a line that has info, but not much else, base case 
        line.split(splitLine)
        array=[]
        for tkn in line:
            if tkn is not splitLine:
                array.append(tkn.strip()) 
        return array


        #Actually, if this is a recursive statement, split by ",", and strip each entry for whitespace, then return an array with those values? Maybe'? 
    result=[]
    pair=[] #[idxStart, idxEnd, brackets]
    stack=[] 
    stack.append(line[startIdx]) 

    newStartIdx=False 
    for idx in range(startIdx+1,len(line)):
        #print("stack: ", stack, "\nLine[idx]=",line[idx])
        #print("idx=",idx)
        if line[idx] in ["(", "{", "["]:
            stack.append(line[idx]) 
            if newStartIdx:
                newStartIdx=False
                startIdx=idx 
                #print("found new start Idx = ",idx)
        else:
            if stack:
                if line[idx] in [")","]","}"]:
                    if (stack[-1]=="(" and line[idx]==")") or (stack[-1]=="[" and line[idx]=="]") or (stack[-1]=="{" and line[idx]=="}"):  
                        stack.pop() 
                        if not stack:
                            #print("please split: ",line[startIdx+1:idx].strip())
                            try:
                                info=splitStringArray(line[startIdx+1:idx].strip())  #FUTURE: An improvement would be to iterate idx by the length of info, perhaps a plus 1? Unsure.
                            except SyntaxError as e:
                                raise e 
                            #print("insider info = ", info) #should always be an array
                            typeBracket=line[startIdx]+line[idx]
                            info.append(typeBracket)
                            result.append(info) 
                            newStartIdx=True 
                            #print("find a new start IDX") 
                            #print("result = ", result[-1])
                    else: 
                        raise SyntaxError("1 Mismatched Brackets")
            else:
                if line[idx] in [")","]","}"]:
                    raise SyntaxError("Unbalanced Brackets")
    return result
                       

#FUTURE: Insert base cases, early failures, and syntax error possiblities.
def sortBy(tokens:list, lambdaKeys:list): #First sort by [0], then sort by [1], then sort by .... [grouping each after each sort by the criteria that came before]
        toDo=lambdaKeys[0]
        tokens.sort(key=toDo[0], reverse=toDo[1])
        #if there are more instructions, find runs and run those instructions on that subset
        if len(lambdaKeys)-1!=0:
            tempRun=[0,0]
            while tempRun[1]<len(tokens):
                if toDo[0](tokens[tempRun[0]])==toDo[0](tokens[tempRun[1]]):
                    tempRun[1]+=1
                else:
                    print("Found run of ", tempRun[0], ", ",tempRun[1]-1)
                    tokens[tempRun[0]:tempRun[1]]=sortBy(tokens[tempRun[0]:tempRun[1]], lambdaKeys[1:]) #Widest range to start, mutates original list. 
                        #NOTE, I think the slicing when passing into sortBy makes it not sort in place :/. What can you do? I suppose. 
                    tempRun[0]=tempRun[1]
                    tempRun[1]=tempRun[0]
            
            print("Found run of ", tempRun[0], ", ",tempRun[1]-1)
            tokens[tempRun[0]:tempRun[1]]=sortBy(tokens[tempRun[0]:tempRun[1]], lambdaKeys[1:]) #Widest range to start, mutates original list.  

        return tokens

#[[(1,2,3), (4,5), (6,7,8), (9)],[(-1,-2), -3], []]


#input array of values/lists
    #return string -> for each list, put the appropraite bracket on space _y_, and _y+2_, with hte internal values printed on _y+1_
        #If the value is another string/value, print on _x+1_ (as the bracket prints on _x_), this pattern continues until either the type cannot be grasped on the inside again, or it is empty
    #EXPECT: if a container is used like object, [non primitive, non standard], it will try to print the iter then call next?
def printListValuesJsonLike(tokens:list, y=0, x=0, _y_=1, _x_=1, getSublist=None, objList=[]):
    """objList should include all objects possible to run into for this array,  containers in which you want the '__str__' method called. In this case, it's attributes may not be present, but allows customizable reports.
    If the object doesn't have a __str__ method, it prints the data members (name : value) pairs.
    y and x are defaulted, y handles how many newlines to include at the start of the string construction. Otherwise it gives the 'hieght' of the output. x handles how many spaces to give each object at the start
    For instance, [1,2,3] with x=0, will print '[' at (x=0,y=0), but '1' at (x=1), y=(1). To edit the Spacing of these objects, pass the desired amountto _y_ and _x_."""

    #region
        #In:[1,2,3 [a,b,c], objWithSubList, objWithoutSublist]
        #out:
        #[
        #  1,
        #  2,
        #  3,
        # [
        #   a,
        #   b,
        #   c,
        # ]
        #  objectPrintWSub [
                    #         stuff
        #                  ]
        # objectPrintW/O
        # ]
    #endregion
    
        #signature <-make sure the getSublist has 0 arguments (or self)
    #getattr(type(item), itemFromDir)[0]=='function/attribute': <-perhaps make a toggle for this?
        #include in the list
    from inspect import signature
    import inspect 
    

    tempStr=""
    if y!=0:
        tempStr+="\n"*y
    if x!=0:
        tempStr+=" "*x
    tempStr+="["; x+=_x_; y+=1

    for item in tokens:
        #INSERT: Check if its a function [for whatever reason? and raise error]
        if type(item)!=int and type(item)!=str and type(item)!=bool: #The item is not primitive  
            sTMembers=inspect.getmembers(TestStuff) 
            sTMethods=[i for i in sTMembers if inspect.isfunction(i[1])] 
            sTAttr=[i for i in sTMembers if not inspect.isfunction(i[1]) and not inspect.isclass(i[1]) and not inspect.isbuiltin(i[1]) and not inspect.ismethod(i[1])
                        and not inspect.isabstract(i[1]) and not inspect.isasyncgen(i[1]) and not inspect.isasyncgenfunction(i[1]) and not inspect.isawaitable(i[1])
                        and not inspect.iscode(i[1])and not inspect.iscoroutine(i[1]) and not inspect.iscoroutinefunction(i[1])and not inspect.isdatadescriptor(i[1])
                        and not inspect.isframe(i[1])and not inspect.isgenerator(i[1]) and not inspect.isgeneratorfunction(i[1]) and not inspect.isgetsetdescriptor(i[1])
                        and not inspect.ismemberdescriptor(i[1]) 
                        and not inspect.ismodule(i[1])and not inspect.isroutine(i[1]) and not inspect.istraceback(i[1])]
            sTAttr=sTAttr[3:] #Skip the first three members as these seem to be hard toremove with just inspect.
            print("Found Methods: ", sTMethods) 
            print("Found Attributes: ", sTAttr)

            if item in objList:  #Assume it has a __str__ method.
                tempStr+=" "*x + item.__name__+": "+str(item) + "\n"*_y_ #NOT CLEAR if str() is required, or if it would auto call without it
                y+=_y_
                y+=str(item).count("\n") 
                x+=_x_ #we will subtract this after printing the attributes and/or methods
                
                
                hasSublistFunction=False
                functionHolder=None
                for item in sTMethods:
                    if item[1].__name__==getSublist:
                        hasSublistFunction=True
                        functionHolder=item[1]
                        sig=signature(functionHolder)
                        if len(sig)!=0: 
                            raise SyntaxError("expected no arguments for 'getSublist: "+getSublist+", instead obtained: "+sig)
                    tempStr+=" "*x + item + "\n"*_y_
                    y+=_y_
                if hasSublistFunction==True:
                    #INSERT: In the future, would like to test if the attributes are objects, and/or if the objects have an iterable like a List/Tuple. 
                    lines, height=printListValuesJsonLike(functionHolder(item), 0, x, _y_, _x_, getSublist, objList)
                    tempStr+=" "*x+lines+"\n"*_y_
                    y+=(_y_+height)
                x-=_x_
                #Recursion preserves _y_, x, _x_, getSublist, and  objList.
                #if item has method getSublist:
                    #item.getSublist recursion
                #elif item has method itr and next:
                    #handle in this layer or compile all of it into a list/remove the tokens:list requirement.
                
            else:
                tempStr+=" "*x + item.__name__+": "+"\n"*_y_
                y+=_y_
                x+=_x_ #we will subtract this after printing the attributes and/or methods
                for item in sTAttr:
                    tempStr+=" "*x + item + "\n"*_y_
                    y+=_y_
                hasSublistFunction=False
                functionHolder=None
                for item in sTMethods:
                    if item[1].__name__==getSublist:
                        hasSublistFunction=True
                        functionHolder=item[1] 
                        sig=signature(functionHolder)
                        if len(sig)!=0: 
                            raise SyntaxError("expected no arguments for 'getSublist: "+getSublist+", instead obtained: "+sig)
                        
                    tempStr+=" "*x + item + "\n"*_y_
                    y+=_y_
                if hasSublistFunction==True:
                    #INSERT: In the future, would like to test if the attributes are objects, and/or if the objects have an iterable like a List/Tuple. 
                    lines, height=printListValuesJsonLike(functionHolder(item), 0, x, _y_, _x_, getSublist, objList)
                    tempStr+=" "*x+lines+"\n"*_y_
                    y+=(_y_+height)
                x-=_x_
                
        else:
            tempStr+=" "*x + str(item) + "\n"*_y_
            y+=_y_


    tempStr+="]"


    pass


def defaultClearTerminal():
    """Just an easier way to clear the terminal"""
    print("\n"*30) 


def testMe(y=0):
    x=1+y
    print("just to test inspect package")
    return x

def main(): #Seperate this into a test file
    testMatrixSquare=[ #col vectors are easier to grab
        [1,  
        2], [3, 
            4]
    ]
    testMatrixRectangle=[
        [10,
        2], [300,
            4], [5000,
                6]
    ]
    print(prettyPrintMatrix(testMatrixSquare))
    print("\n")
    print(prettyPrintMatrix(testMatrixRectangle))
    
    testLine="[[( 1,2,3), (  4,5  ) , (6,7,8), ( 9)  ],[(-1,-2), -3], []]"
    testbadLine="[()]{}}" #unbalanced
    pairs, line=splitStringArrayBalancedRecord(testLine)
    print("pairs: ", pairs)
    try: 
        splitStringArrayBalancedRecord(testbadLine)
    except SyntaxError as e:
        print("expected, ", e)

    #splitStringArray, idea is to iterate over a given string in the form of an array to reconstruct that string as an actual array.
        #[arguments, "bracket type"], example [(1,2,3), 4] becomes [ [1,2,3 "[]"], 4, "[]"]
        #We should recieve [startIdx, endIdx, insideInfo, TypeBrackets], so we can then go
            #[splitStringArray(InsideInfo), TypeBrackets]
    #Need to think more on how to make this recursive... :/

    #{[1,2,3,4]}
    testLine="{[1,2,3,4]},[1,2],{1},()"
    result=splitStringArray(testLine)
    print(result)
    testLine="[{[1,2,3,4]},[1,2],{1},()]"
    result=splitStringArray(testLine)
    print(result)
    testLine=""
    result=splitStringArray(testLine)
    print(result)

    print(dir(TestStuff))
    try:    
        print(getattr(TestStuff, "a"))
    except:
        print("expected failure")
    print(getattr(TestStuff, "one"))

    print(getattr(TestStuff, "testOut"))
    import inspect
    print(inspect.isfunction(testMe))
    print(inspect.isfunction(testMe())) #exectues the code, but doesn't return a callable!
    defaultClearTerminal()

    a=TestStuff()
    b=TestStuff2()
    c=TestStuff3()
    testArray=[-1,-2,-3, a, b, c]
    #printListValuesJsonLike(testArray, 0, 0, 1, 1, "getSublistStuff",)
    sTMembers=inspect.getmembers(TestStuff) 
    sTMethods=[i for i in sTMembers if inspect.isfunction(i[1])] 
    print(sTMethods)
    print(type(sTMethods[1]))
    print("(", type(sTMethods[1][0]),",",type(sTMethods[1][1]),")")
    print(sTMethods[1][1](a)) 
    defaultClearTerminal()
 
    tempStr="HEY1:"
    TestStuff #NonInstance
    if isinstance(a, a.__class__):
        tempStr+=a.__class__.__name__
    else:
        tempStr+=a.__name__
    print(tempStr)

    tempStr="HEY2:"
    a=TestStuff() #Instance
    if isinstance(a, a.__class__):
        tempStr+=a.__class__.__name__
    else:
        tempStr+=a.__name__
    print(tempStr)

    #Note for future jacob. The inspect package function we were writting to explore an array and related subObjects
        #Needs to store the ID of those objects to check against. We can organize/sort it and then we won't end up with a parent->child ->parent->... situation in the event two objects are children of each other.
    


    printListValuesJsonLike(testArray, 0, 0, 1, 1, "getSublistStuff",[TestStuff, TestStuff2, TestStuff3])


if __name__=="__main__":
    main() 