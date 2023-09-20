

#Ignore - These two functions was trying to check if an instance of a variable was of a certain range of types, or a function
    #A specialized error is required,
    #Ways to check if a variable is a function: callable(), isfunction from the inspect module, type(func)==<class 'function'>, hasattr(var, '__call__'), and from module types types.FunctionType.
def checkIfFuncParameter(arg, types:list): 
    typeFail=False
    shallowFail=False #shallow copy, deep copy would require some work, or user ensurance or a wrapper.
    if (1==len(types)): 
        try:
            if not isinstance(arg, types[0]):
                raise TypeError
        except TypeError:
            typeFail=True
        try:
            if arg!=types[0]:
                raise ValueError
        except ValueError:
            shallowFail=True

        if typeFail and shallowFail:
            raise TypeError("Value or Type failed")
        else: 
            print("Found at end")
            pass 

    else:
        if not isinstance(arg, types[0]):
            try:
                checkIfFuncParameter(arg, types[1:])
            except TypeError or ValueError as e:
                raise e
        else:
            print("Found type")
            pass        
def test_checkIfFuncParameter():
    a =1
    b=.2
    c=.3
    listTest=[1,2,3,4]
    noneTest=None
    def testFunction():
        pass  
    print(locals().items())
    testCases=[[int, float, list, None], [int, float, list, None]] 
    try:
        for caseIdx in range(len(testCases)):
            print("Case : "+caseIdx)
            for item in locals().items(): #Could make internal function to run each test case easier...
                if item[0] != "testCases":
                    print("try item ", item)
                    try:
                        print(len(testCases[0]))
                        checkIfFuncParameter(item[1], testCases[caseIdx])
                    except TypeError:
                        print("error found for local: ", item)
    except NameError:
        print("Expected failure, can't figure out how to articulate variable must be a function")
    

#if not isinstance(additionalTokenSeperation, function): #NOTE/KEEP potential race condition, EAFP vs LBYL and parameter validation nonsense. will worry about it later.
#        if not isinstance(additionalTokenSeperation, None):
#            raise TypeError
    
    