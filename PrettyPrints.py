 

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
    


if __name__=="__main__":
    main()