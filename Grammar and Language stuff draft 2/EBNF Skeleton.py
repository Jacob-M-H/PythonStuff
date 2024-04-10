




class EBNFParser:
    #[]
    #{}
    #()
    #s.e
    #[]+
    #|
    #Regex 
    SQBF="["
    SQBB="]"
    CBF="{"
    CBB="}"
    PF="("
    PB=")"
    Literal="\'"
    Escape="\\"
    orSymbol="|"
    WSP=" "
    LWSP=" " #controversial, 0+ whitespace, newliens permitted, at least 1 WS needed for delimination. Def left aligned, multiple lines are required for radability, continuation lines indented by white space.
    comment=";"
    plusSym="+"
    dotSym="."
    regexDeclaration="Regex("
    QM="?"
    minusSym="-"
    star="*"
    colon=":"
    
    terminal="%"#%[b|d|x|s].[deciaml|string|hex|""] #for now I'm going to assume that if it's not a rule name, its a terminal or regex.
 


    def __init__():
        pass
    
    def matchCase(symbol): 
        pass

    def start(inputString:str, case:list, head:int=0):
        tempHead=head
        for idx in range(len(inputString)):  
            pass
        pass
    





#input string, head position
    #test against an array

#Return length of pattern match, old head position, new head position, and if complete match obtained.


class doctorOfficeWork():
    """
    inputLine <- (literals &/or atoms) (used for Syntax version)
    inputCase <- (literals &/or atoms &/or rule_names, used for both)
    Place=0
    Lookahead=0
    root(s)<-entry. highest/lowest depth first [most specific case, so either root can be started, so long as the case matches. In this case it may be useful to just start a parent root that assumes both responsbilities, sorting it's cases, to have 1 conssitent entry way [leaving the other(s) in a non parsed state in the file, so that the original data isn't discarded in the event of critical error.]]
    Expect=[] <-detect if a pairing needs to close or not [For EBNF parsing of rule cases]
    AcceptedStack=[] <- amount matched
    longestSuccess<-holds (longest successful parse, length)
    longestParse <-holds (longest parse, length), and resets the place. Gives opportuity to prompt for errors in grammar formatting by case, or if inputLine is used the syntax
    """

    #First mission is to evaluate each case for proper EBNF form. This is 'simple' and 'naive'.
        #| is not accounted for, though we should really enforce a grouping around it.
        #% is not accounted for, neither is + or * or ., These things complicate the basics.
    def validateEBNFform(inputCase:str): 
        expect=[]
        def checkExpect(idx): #Simplify things, not the exact implemntation to be used later.
            try:
                return expect[idx]
            except IndexError:
                return None
            
        NegateNextSymbol=False
        NegateEBNFSymbol=False
        NegateSingleQuote=False
        NegateDoubleQuote=False
        ErrorFound=False
        ResetNegateNextSymbol=False
        for idx in range(len(inputCase)):
            #Assumed EBNF parities.
            #\", \' \\ all should negate (,[,{, but in different ways.
            #\",\' negate all symbols until popped.
            #\\ negates next symbol, symbol should be considered to have specail meaning
            
            #Unique Parity & bad if closure happens without opening
            if inputCase[idx]=="(" and not NegateEBNFSymbol and not NegateNextSymbol:
                expect.append(")")
            elif inputCase[idx]=="{" and not NegateEBNFSymbol and not NegateNextSymbol:
                expect.append("}")
            elif inputCase[idx]=="[" and not NegateEBNFSymbol and not NegateNextSymbol:
                expect.append("]")
 
            if inputCase[idx]==")" and not NegateEBNFSymbol and not NegateNextSymbol:
                if checkExpect(-1)=="(":
                    expect.pop()
                else:
                    ErrorFound=True
            elif inputCase[idx]=="}" and not NegateEBNFSymbol and not NegateNextSymbol:
                if checkExpect(-1)=="}":
                    expect.pop()
                else:
                    ErrorFound=True
            elif inputCase[idx]=="]" and not NegateEBNFSymbol and not NegateNextSymbol:
                if checkExpect(-1)=="]":
                    expect.pop()
                else:
                    ErrorFound=True
            
            #Bad closure for EBNF form
            if ErrorFound==True:
                return False
            


            #Non Unique Parity
            if inputCase[idx]=="\'" and not NegateSingleQuote and not NegateNextSymbol:
                if checkExpect(-1)=="\'":
                    expect.pop()
                    NegateDoubleQuote=False
                    NegateEBNFSymbol=False
                else:
                    expect.append("\'")
                    NegateDoubleQuote=True
                    NegateEBNFSymbol=True
            elif inputCase[idx]=="\"" and not NegateDoubleQuote and not NegateNextSymbol:
                if checkExpect(-1)=="\"":
                    expect.pop()
                    NegateSingleQuote=False
                    NegateEBNFSymbol=False
                else:
                    expect.append("\"")
                    NegateSingleQuote=True
                    NegateEBNFSymbol=True


            #Escapenent stuff
            if NegateNextSymbol==True:
                ResetNegateNextSymbol=True
            #Escape Character
            if inputCase[idx] and not NegateNextSymbol=="\\":
                NegateNextSymbol=True
            
            if ResetNegateNextSymbol:
                NegateNextSymbol=False  
                ResetNegateNextSymbol=False          
            

            
            #End of check particlar idx - not quie right. needs to last more than just this idx, needs t olast until next too.
            NegateNextSymbol=False

        
        if expect==[]:
            return True
        #Figure out what failed.
        return False


def testSweep(tests:list, func, expectedResults:list|bool): 
    if isinstance(expectedResults, (bool)):
        print("make new list")
        expectedResults=[expectedResults]*len(tests)
        print("expectedResults")
    elif isinstance(expectedResults, (list)) and len(expectedResults)!=len(tests):
        return "Error :/, lists are not of same length."
 
    rangeLen=len(tests)
    expectedResultConfirmed=[]*rangeLen
    isExpected=True
    print("expected Results: ", expectedResults)
    
    for idx in range(rangeLen):
        if func(tests[idx])==expectedResults[idx]:
            expectedResultConfirmed.append(True)
        else:
            expectedResultConfirmed.append(False)
            isExpected=False

        
    return (isExpected,expectedResultConfirmed)


def main():
    """
    inputline <- literals+atoms. How atoms are detected will be based on whether it expects such atom, and whether that atoms implimentation excepts and escapes properly, vs a literal could be an atom, if it's expected. This is the furthest range I can think about, but more complex languages will benefit from forward declaring the type of atom or literal.
        <-this can be implemented by simply making a rule name per atom, I suppose. The atom rule name is assumed however. Guess nothing to stop double declaration? Will have to give this more thought later when we're on the topic of it.
    """
    
    #Should all return true
    goodEBNFbasics=[ "()", "[]", "{}", "\"\"", "\'\'" ]
    badEBNFbasicsF=["(\'", "[\'", "{\'", "(\"", "[\"", "{\""]
    badEBNFbasicsB=["\')", "\']", "\'}", "\")", "\"]", "\"}"]
    badEBNFbasicsP=["(]", "(}", "[)", "[}", "{)", "{]"]
    badEBNFbasicsNP=["\'\"", "\'\""]
    goodEBNFbasicsE=["\\\' \'\'", "\\\" \"\""]
    goodEBNFbasicsS=["\'([{\'", "\"([{\"", "\'}])\'", "\"}])\""]
    goodEBNFbasicsSQ=["\' \" \\\" \'", "\" \' \\\" \"", "\' \" \'", "\" \' \""]

    A=testSweep(goodEBNFbasics, doctorOfficeWork.validateEBNFform, True)
    B=testSweep(badEBNFbasicsF, doctorOfficeWork.validateEBNFform, False)
    C=testSweep(badEBNFbasicsB, doctorOfficeWork.validateEBNFform, False)
    D=testSweep(badEBNFbasicsP, doctorOfficeWork.validateEBNFform, False)
    E=testSweep(badEBNFbasicsNP, doctorOfficeWork.validateEBNFform, False)
    F=testSweep(goodEBNFbasicsE, doctorOfficeWork.validateEBNFform, True)
    G=testSweep(goodEBNFbasicsS, doctorOfficeWork.validateEBNFform, True)
    H=testSweep(goodEBNFbasicsSQ, doctorOfficeWork.validateEBNFform, True)

    tests=[A,B,C,D,E,F,G,H]
    for testIdx in range(len(tests)):
        if tests[testIdx][0]==False:
            print("test ",testIdx, " failed:")
            print(tests[testIdx])
        else:
            print("test ", testIdx, " passed.")

    pass

if __name__=="__main__":
    main()





"""
Have been thinking about it for awhile, got a potential job avenue in Java, so I'll be wrapping up the project's state and current thoughts on the project doc.
I will also try to make the over arching program path an image for the project doc so the order of operations doesn't get twisted.
Also note the isInstance is better than type() for checking. I forgot that type() doesn't necessarily return a string with the type. :/.
"""


