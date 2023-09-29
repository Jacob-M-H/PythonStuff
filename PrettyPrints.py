 

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
        print("stack: ", stack, "\nLine[idx]=",line[idx])
        print("idx=",idx)
        if line[idx] in ["(", "{", "["]:
            stack.append(line[idx]) 
            if newStartIdx:
                newStartIdx=False
                startIdx=idx 
                print("found new start Idx = ",idx)
        else:
            if stack:
                if line[idx] in [")","]","}"]:
                    if (stack[-1]=="(" and line[idx]==")") or (stack[-1]=="[" and line[idx]=="]") or (stack[-1]=="{" and line[idx]=="}"):  
                        stack.pop() 
                        if not stack:
                            print("please split: ",line[startIdx+1:idx].strip())
                            info=splitStringArray(line[startIdx+1:idx].strip()) 
                            print("insider info = ", info) #should always be an array
                            typeBracket=line[startIdx]+line[idx]
                            info.append(typeBracket)
                            result.append(info) 
                            newStartIdx=True 
                            print("find a new start IDX") 
                            print("result = ", result[-1])
                    else: 
                        raise SyntaxError("1 Mismatched Brackets")
            else:
                if line[idx] in [")","]","}"]:
                    raise SyntaxError("Unbalanced Brackets")
    return result
                       

#[[(1,2,3), (4,5), (6,7,8), (9)],[(-1,-2), -3], []]


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



if __name__=="__main__":
    main()