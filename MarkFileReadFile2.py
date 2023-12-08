#Became disillusioned with the older version. Too much 'noise' happening in the code. 
    #Things I want to do that I can't do yet,
    #Things that are too 'woven' together, instead of a list of instructions.



from PrettyPrints import prettyPrintMatrix

specialTokens=["\\expr", "..."]; #Expr is any string. Parsed later basically, or of lower priority  Perhaps a [min, max] will be created which will let the parser know how much of something to expect.
logicSymbols=["if", "then", "otherwise", "else", ",", ".", "and", "or", "cannot", "be", "exists","exist", "there",  
              "for", "all", "every", "is", "are", "an", "a","must","only","case","cases"]
reservedTokenHead="/\\"



class FoundPotentialToken(): #The idea is that the sets_ will let us change the start/end when accpeting fair tokens across pairs and the unqiue list 
    symbolIndex:int #Which word in the sentence to look at for this token.
    tokenSymbol:str
    layer:int
    start:int
    end:int
    def __init__(self, tS:str, l:int, s:int, e:int, symbolIndex:int):
        self.symbolIndex=symbolIndex
        self.tokenSymbol=tS
        self.layer=l
        self.start=s
        self.end=e
    def getSymbolIndex(self):
        return self.symbolIndex
    def setSymbolIndex(self, idx:int):
        self.symbolIndex=idx
    def checkAssumptions(self):
        if self.layer>-1 and self.start>-1: #end is not clear, but start is.
            if self.start<=self.end:
                return 1
            else:
                return -1
        else:
            return -2
    def getTokenSymbol(self):
        return self.tokenSymbol
    def getLayer(self):
        return self.layer
    def setStart(self, s:int):
        self.start=s
    def setEnd(self, e:int):
        self.end=e
    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end
    def __str__(self): #str(FoundPotentialToken) <-guess
        return "["+self.tokenSymbol+", "+ str(self.layer)+", "+str(self.start)+", "+str(self.end)+", "+str(self.symbolIndex)+"]"
    def __repr__(self): #print 
        return "["+self.tokenSymbol+", "+ str(self.layer)+", "+str(self.start)+", "+str(self.end)+", "+str(self.symbolIndex)+"]"
   



class PhraseRecord():#https://stackoverflow.com/questions/70507587/storing-list-of-strings-that-have-a-format-variable might have some use
    totalLayers:int
    ORIGINALPHRASE:str
    currentPhrase:str

    phraseHistory:list[str] #not sure if this is correct notation(s)
    problemTokenHistory:list[list[list]]
    fairTokenHistory:list[list[list]] 
    problemMatrix:list[list] #Running total of problem tokens
    fairMatrix:list[list] #Running total of fair tokens
    totalTokensMatrix:list[list] #Total tokens accepted from deminishes.
    symbolDict:dict() #The index in the matrices (row or column) for that specific Token. 

#Initial construction of object
#region
    #User inputed functions -passed as arguments to the class?  
    def __init__(self, orgPhrase:str, tokenSplitCharacter=" "):
        self.ORIGINALPHRASE=orgPhrase #Declare const/final? 
        self.totalLayers=0 #NOTE Layers will have to be handled carefully later - need a better way of tracking later after we have the ability to do itterations on longer phrases.
        self.currentPhrase=self.ORIGINALPHRASE.split(" ") 
        self.phraseHistory=[]
        self.phraseHistory.append(self.currentPhrase)
        self.problemTokenHistory=[]
        self.problemTokenHistory.append([])
        self.fairTokenHistory=[]
        self.fairTokenHistory.append([]) 
        self.symbolDict={}
        place=0
        for i in set(specialTokens+logicSymbols):
            self.symbolDict[i]=place
            place+=1


        self.createMatrices()
  
    #EDIT, make a copy of relevant info for the tokens
    def pushPhrase(self, phrase:str, fairTokens:list, problemTokenPairs:list):
        def matchCurrentPhraseWithHistoryPhrase(): #Ensures the currentPhrase is matching with the end of the history of Phrases.
            mostRecentPhrase =self.phraseHistory[len(self.phraseHistory)-1]
            if self.currentPhrase != mostRecentPhrase:
                self.currentPhrase=mostRecentPhrase

        self.totalLayers+=1
        self.phraseHistory.append(phrase)
        self.fairTokenHistory.append(fairTokens)
        self.problemTokenHistory.append(problemTokenPairs) #NOTE this and the others need to be made into deep copies or constructors' in form of a list, otherwise history get's eddited as tokens are accepted and adjusted.
        matchCurrentPhraseWithHistoryPhrase()

    #EDIT, create a new prblm/fair tkn lists based on preserved information
    def popPhrase(self) ->int:
        def matchCurrentPhraseWithHistoryPhrase(): #Ensures the currentPhrase is matching with the end of the history of Phrases.
            mostRecentPhrase =self.phraseHistory[len(self.phraseHistory)-1]
            if self.currentPhrase != mostRecentPhrase:
                self.currentPhrase=mostRecentPhrase

        if self.totalLayers>0:
            self.totalLayers-=1
            self.phraseHistory.pop()
            self.fairTokenHistory.pop()
            self.problemTokenHistory.pop()
            matchCurrentPhraseWithHistoryPhrase()
            return 0
        else:
            return -1 #fail

    def createMatrices(self): #Assumes specialtokens and logic symbols are defined. FUTURE: Should make the matrices able to 'eliminate' rows and columns if symbols change, or 'append' if symbols change. Vectors/linked lists might be best for this application!
        #CTRLF NOTE SUBROUTINE #NOTE: This might be a utility function later (unique(iterable, sorting method)), used in other places as well 
            #Likely will want upper and lower triangular matrices. See MarkFileReadFile for how I was using symbolDict
        pass
 
    def checkAssumptions(self): #Later, particularly when subclasses are created.
       pass
#endregion

#Initial values of object String Data -Runs only once for now. NEXT:=PromptUser
    def deminishStatement2(self, phrase:list[str], 
                        additionalTokenSeperation, #function|None
                        findHighOrderTokens, #function|None
                        layer=None):
        if layer==None: #mhm :/
            layer=self.totalLayers 
        #validate type
        if not hasattr(additionalTokenSeperation, '__call__') and additionalTokenSeperation != None: #possible race condition
            print("additionalTokenSeperation should try to seperate symbols from other tokens, if those symbols might be confused in regular grammar \n expected/suggested behavior seperates each 'new' token as length 1 string.")
            raise TypeError("additionalTokenSeperation must be a callable function or of type None")
        if not hasattr(findHighOrderTokens, '__call__') and findHighOrderTokens != None: #possible race condition
            print("findHighOrderTokens should try to recombine additionaltokenSeperation's tokens into higher order Tokens, which are more clearly seperated [hopefully] from the rest of the expression.")
            print("Note that findHighOrderTokens is expected/suggested to search for strings of length 1 from additionalTokenSeperation")
            raise TypeError("findHighOrderTokens must be a callable function or of type None") 
        #Clean/seperate tokens
        #Find potential recombinations of tokens for higher order tokens
        #find conflicts in the potential - fair tokens, problem tokens
        #record phrase, and tokens before accepting.
        #accept tokens
            #adjust tokens, new string
        #record remaining tokens, new phrase
        if additionalTokenSeperation!=None:
            wordList=additionalTokenSeperation(phrase) #Clean/seperate tokens
        else:
            wordList=phrase
        #Layer 0, assuming this is what is desired. 


        #EDIT/INSERT <- argument for adding symbols to this phrase object. 
        #SYMBOL DICT: REquired for verifying and finding
        self.symbolDict[0]="..."


        #----- Find special Syntax and Conflicts in that (unintentional grammer conplexity) ----- 
        if findHighOrderTokens!=None:
            highTokens=fastFindSpecialSymbol1(wordList, ["..."], self.totalLayers) #DEFAULT PLACEHOLDER
        else:
            highTokens=[]    
        
        
        #find conflicts in the potential - fair tokens, problem tokens 
        problemHighTokensPairs=[]
        if len(highTokens)>1:
            problemHighTokensPairs=self.checkConflictsHighTokens(highTokens) #Insert=True means it's save to add all,  
        
        print("ProblemTokensPairs: ", problemHighTokensPairs) #ERR, 14-16, and 5-7 should be in fair tokens :/?
        #CTRLF NOTE SUBROUTINE Substep Standard report unique problems, preserve problem pairs for data retreival. 
        problemHighTokens=set()
        for pair in problemHighTokensPairs: 
            for problem in pair: 
                problemHighTokens.add(problem) 
        problemHighTokens=list(problemHighTokens)  
        fairTokens=[i for i in highTokens if i not in problemHighTokens]  #Fair tokens are those that can be applied without conflict 
        if len(fairTokens)>1:
            fairTokens=self.sortBy(highTokens, [ [lambda x:(x.getSymbolIndex()), False],[lambda x:(x.getStart()), False], [lambda x:(x.getEnd()-x.getStart()), True] ] ) 
         
        print("fairTokens : ", fairTokens)

        self.recordTokens(fairTokens, problemHighTokensPairs) #Record token conflicts and fair tokens for later analysis.

        #Initial layer 0 push
        self.pushPhrase(wordList, fairTokens, problemHighTokensPairs) #word list pushed as it seperates additional tokens for highToken finding. 
        print("current phrase: ", self.currentPhrase)
        self.promptUser(fairTokens, problemHighTokensPairs, wordList, problemHighTokens) #Seperate function for user accepting commands 

        #KEEP:
        #region
        #Keep
            #GOAL: Turn the string into just tokens or expr, and not tokens that are seen as expr, and not expr that are seen as tokens. [whatever that means]
            #Additional seperation <-cleanWordList is mine, should seperate punctuation. User defined for unforseen required seperations.
            #findHighOrdertokens <-findSpecialSyntax, is mine, should recombine strings of length 1, from the additional seperation.  (Want a larger system test multiple special syntaxes in parallel)

            #Check conflicts
            #record problem ,fairs, and current wordList [during each of these following steps if changes are made]
                #Record conflicting tokens in a matrix
            #accept fair tokens?
                #Y/N,
            #handle conflicts?  #record seperately which ones are favored in syntax graphs
                #Y/N
            #Manual handle conflicts? #Record seperately which ones are favored in user graphs
                #Y/N
            
                #when things are handled, map [start position] with a length [len], and a total 'dist', so that in any order after the strings been completed [for each of those four steps]
                    #it is easy to go through and adjust the positions of each.


            #KEEP high level of whats going on, 
                #assumption:token seperator should be applied already, exmple " ", any whitespace left should be part of a token, or itself have meaning.
                #additionalTokenSeperation should try to seperate symbols from other tokens, if those symbols might be confused in regular grammer.
                #findHighOrderTokens should try to recombine additionalTokenSeperation's tokens into highorderTokens, which then are more clearly seperated [hopefully] from the rest of the expression
                                #findhighOrderTokens should default to trying to find all specialtokenSyntax. ASSUMPTION, each character of the highordertoken is a token after splitting. (so we can filter the default special tokens by those with a start that maches a token of length 1 in the phrase?)
                #checkConflictsHighTokens [not a default], for all hightokens make sure the interpretation is either handled or raised as a conflict for suggestions on grammar construction
                #Record all problem Tokens, and fairTokens
                    #Q: accept fair tokens? Handle problem tokens? (record which tokens conflicted, which was chosen if any)
                    #On accept of any and a confirmation of 'end', record new resulting statement, and remaining problem/fair tokens [adjusting their idxes by accepted]
        #endregion
        
        pass

    def recordTokens(self, fairTokens:list[FoundPotentialToken], problemHighTokenPairs:list[list[FoundPotentialToken]]):
       pass 
 
    def promptUser(self, fairTokens:list, problemHighTokenPairs:list[list[FoundPotentialToken]], wordList:list[str], problemHighTokens:list[FoundPotentialToken]):
        #Commands
        print("What is your command:")
        response=None 

        def createNewLine(type:int (0|1), skipList:list[str]):
                nonlocal problemHighTokenPairs #remove conflicts when accepting or handling one over the other.
                nonlocal problemHighTokens #fast adjust indexes
                nonlocal fairTokens
                #ASSERT type==0
                #Fair tokens, accept based on original line, and not mutated line. Thus it is fine to look at the current for all tokens to be accepted until completed.
                if type==0:
                    fTIdx=0
                    wordIdx=0
                    newList=[] 
                    acceptedTokens=[]

                    while (wordIdx<len(self.currentPhrase)):
                        if (fTIdx<len(fairTokens)):
                            if fairTokens[fTIdx].getStart()==wordIdx:
                                if fairTokens[fTIdx].getTokenSymbol() not in skipList:
                                    inspectToken=fairTokens.pop(fTIdx)
                                    wordIdx+=inspectToken.getEnd()-inspectToken.getStart() 
                                    acceptedTokens.append(inspectToken) 
                                    newList.append(inspectToken.getTokenSymbol())
                                else:
                                    fTIdx+=1
                                    inspectToken=None
                                    wordIdx-=1 #Potentially another token is found in the same spot? (Likely would be a problem token then, but just to be safe)
                            else:
                                #Accept the word as it is
                                newList.append(self.currentPhrase[wordIdx])    
                        else:
                            #Accept the word as it is
                            newList.append(self.currentPhrase[wordIdx]) 
                        wordIdx+=1

                    #Adjust those that remain by the ones that we accepted
                    newline, adjusts=self.acceptToken(self.currentPhrase, acceptedTokens) #inspect the token, adjust all those after it's index 
                    self.adjustTokens3(adjusts, fairTokens)
                    self.adjustTokens3(adjusts, problemHighTokens)
                    self.pushPhrase(newList, fairTokens, problemHighTokenPairs) #NOTE Perhaps make shallow/deep copies? Since editing in the past would edit all the recorded ones. 
                    
                else:
                    #Virtually the same, accept when accepting, we must remove all conflicts with that inspected token. It's already an adjacency list so not much improvement can be done to the search.
                    pTIdx=0
                    wordIdx=0
                    newList=[] 
                    acceptedTokens=[]

                    while (wordIdx<len(self.currentPhrase)):
                        if (pTIdx<len(fairTokens)):
                            if fairTokens[pTIdx].getStart()==wordIdx:
                                if problemHighTokens[pTIdx].getTokenSymbol() not in skipList:
                                    inspectToken=problemHighTokens.pop(pTIdx)
                                    wordIdx+=inspectToken.getEnd()-inspectToken.getStart() 
                                    acceptedTokens.append(inspectToken) 
                                    newList.append(inspectToken.getTokenSymbol())
                                else:
                                    pTIdx+=1
                                    inspectToken=None
                                    wordIdx-=1 #Potentially another token is found in the same spot? (Likely would be a problem token then, but just to be safe)
                            else:
                                #Accept the word as it is
                                newList.append(self.currentPhrase[wordIdx])    
                        else:
                            #Accept the word as it is
                            newList.append(self.currentPhrase[wordIdx]) 
                        wordIdx+=1

                    #Adjust those that remain by the ones that we accepted
                    newline, adjusts=self.acceptToken(self.currentPhrase, acceptedTokens) #inspect the token, adjust all those after it's index 
                     #Sanity check, make sure our problem tokens are still there, recreate their pairs
                        #Problem High Tokens are already removed from the fast list. Now to adjust the pairs.
                    problemHighTokenPairs=self.problemPairSanityCheck(problemHighTokens, problemHighTokenPairs)
                    self.adjustTokens3(adjusts, fairTokens)
                    self.adjustTokens3(adjusts, problemHighTokens)
                    self.pushPhrase(newList, fairTokens, problemHighTokenPairs) #NOTE Perhaps make shallow/deep copies? Since editing in the past would edit all the recorded ones. 
                    

        def trimList(tokens:list[str]):
            print("trimList start: ",tokens)
            if len(tokens)>1:
                if tokens[0][0]=="[" and tokens[-1][-1]=="]":
                    tokens[0]=tokens[0][1:]
                    tokens[-1]=tokens[-1][:-1]   
                    return tokens
                else:  
                    raise SyntaxError("Missing brackets. 1")
            elif len(tokens)==1:
                if len(tokens[0])<2: 
                    raise SyntaxError("Missing brackets. 2")
                elif (tokens[0][0]!="[" or tokens[0][-1]!="]"):
                    raise SyntaxError("Missing brackets. 3")
                else: 
                    return tokens[0][1:-1]
            else: 
                return tokens 
        
        def verifyTokens(tokens:str): 
            nonlocal tknType
            badTokens=[] 
            #EDIT, check for sym, then wordidx, then start end if available.
            for token in tokens:
                token=token.split(",")
                #Remove the []
                #EDIT, try trimlist?
                

                for infoIdx in range(len(token)):
                    token[infoIdx]=token[infoIdx].strip() 
                #Now check that each of the tokens is a valid token to find.

                #EDIT - when found token is valid, put in a list. Sort that list by WordIdx, Start. 

                if token[0] not in self.symbolDict.keys():
                    badTokens.append(token)
            
            
            
            if len(badTokens)>0:
                raise ValueError("unrecognized tokens: ", badTokens) 
            else:
                return tokens

        def trimAndVerify(startTokens:str): 
            nonlocal response
            tokens=[]
            print(startTokens)
            print(startTokens.split(", "))
            try: #Just a test temporary
                tokens=trimList(startTokens.split(", ")) 
            except SyntaxError as e:
                print("Error:",e)
                response=None #try again   
            
            #Now should have list of tokens '[' (sym),  (sym (start, end)), (sym, wordIdx), (sym, (start, end), wordIdx) ']' as possible sizes of individual elements and where elements are

            try:
                tokens=verifyTokens(tokens)
            except ValueError as e:
                print("Error:",e)
                response=None #try again  
            return tokens

        while (response==None):
            response=input() 
            response=[response.split(" ")[0],response[len(response.split(" ")[0])+1:].strip()] # seperate the first input from the rest of the string  
            print(response)

            if (response[0]=="help"): #need to test if trailing enter is tracked
                print("Commands:\n 'yes': accept all 'type' tokens.\n",
                        "'no': skip all 'type' tokens.\n ",
                        "'yes ['tokens']': yes followed by a list of tokens means accept all of these specific tokens.\nIf the list has additional information, it is expected in the form [tokenSymbol, start, end, wordIdx].\nNote also that it is assumed included information priorities are (tokenSymbol), (wordIdx), (start, end)",
                        "'no ['tokens']': no followed by a list of tokens means reject these specific tokens, accept the rest.\nIf the list has additional information, it is expected in the form [tokenSymbol, start, end, wordIdx].\nNote also that it is assumed included information priorities are (tokenSymbol), (wordIdx), (start, end)",
                        "'tokens?': prints a list of current fair/problem tokens.\n",
                        "'inspect':returns the information of each token, and the original phrase, and the current phrase.\n",
                        "'exit': Assumes this prompt was incurred in error, will resolve without doing anything."
                        "'type?': Fair or Problem Tokens. If fair, use 0, if problem, use 1.")
                response=None
            else:
                #assert response must be a strength of len 0 or more 
                if response[0]=='no' : #Expecting a integer 0 or 1. Then a list of tokens [sym, start, end, wordIdx] (length 1, 2, or 4)
                    if response[1]!='':
                        tknType=int(response[1][0])
                        if tknType!=0 or tknType!=1:
                            print("invalid token type, please use 0 for fair, and 1 for problem tokens")
                            response=None
                        else:
                            response.append(response[1][response[1][len(str(tknType)):].strip()])
                            response[1]=tknType
                        print("response: no ", response[1], "skipList: ", response[2])

                        tokens=trimAndVerify(response[1]) #Notice the response is set to None non-locally inside these functions
                        if response==None:
                            print("try again")
                            continue #something must've failed, try again 

                        #Tokens should be a list of tokens ready to skip. Not just the string values.
                            #Construct during trimAndVerify
                        print("current line : ", self.currentPhrase)
                        print("current fair tokens : ",fairTokens)
                        print("current problem tokens : ", problemHighTokens) 
                        createNewLine(0, tokens) 
                        print("new line : ", self.currentPhrase)
                        print("new fair tokens : ",fairTokens)
                        print("new problem tokens : ", problemHighTokens) #NOTE, should likely sort problemHighTokens by start. 


                    
                    else:
                        print("recieved no") #simple case



                elif response[0]=='yes':
                    pass
                elif response[0]=='exit':
                    print("exited")
                    pass
                elif response[0]=='tokens?':
                    pass
                elif response[0]=='inspect':
                    pass    
                else:
                    print("unrecognized input")
                    response=None





    #One time, cleanWordList, runs on the first wordList to make the next current phrase easier to stand for
    def cleanWordList(self):  #Needs improvement - can a user override this via argument? like self.cleanWordList={function without name?}
        wordList=self.currentPhrase

        newList =[]
        repeat=False
        print(wordList)
        for word in wordList:
            if len(word)>1:
                if word[len(word)-1]==".": 
                    newList.append(word[0:len(word)-1])
                    newList.append(".")
                    repeat=True #Expect some syntax like ...
                elif word[len(word)-1]==",": 
                    newList.append(word[0:len(word)-1])
                    newList.append(",")
                else:
                    newList.append(word)
            else:
                newList.append(word)
        print(newList)
        if repeat:
            return cleanWordList(newList)
        else:
            self.pushPhrase(newList, [], [])
            return 1

    def findPotentialHighToken(self, specialToken:"...", layer=0): #Needs improvement 
                                                #Limited version of what I want to do eventually, which is try to find all high tokens in the series of length 1 characters
                                                #Perhaps in the future we'll split everything with "", and then try to match using a dictionary, favoring longer strings 
        #Find ellipses, or combos of special tokens?
        #A matrix might be useful, or a list of indexes for which the current word Idx is acceptable for that token, reset when not, or reset when complete... Not clear how I may do this efficently besides this to go through just once. Would have to alter how the stagger happens, and how recursion may be handled again.
        specialToken0=specialToken #Example is the ...
        sT0idx=0
        combineIdx=[]
        for wordIdx in range(len(self.currentPhrase)):
            pass
        wordIdx=0
        while (wordIdx < len(self.currentPhrase)):
            #Special token matching, ideally make anonymous and general for each special token.
            if self.currentPhrase[wordIdx]==specialToken0[sT0idx]:
                sT0idx+=1
                #print("match found at ", wordIdx)
                if (sT0idx==len(specialToken0)): 
                    #print("finish find")
                    combineIdx.append([wordIdx-sT0idx+1, wordIdx])
                    sT0idx=0 #reset
                    #A recursion in our format wouldn't know when to stop (continues until end of string), but by staggering at most we have to do double the string length, or a factor of it. This needs improvement regardless
                    wordIdx=wordIdx-len(specialToken)+1 #<-basically a situation lilke ..., and ...., if looking for ..., we end up in trouble. Since there should be two possibel spots flagged.
            else:
                sT0idx=0 #Close, no cigar.
            wordIdx+=1

        for combo in range(len(combineIdx)):
            delist=combineIdx[combo]  
            combineIdx[combo]=FoundPotentialToken(specialToken, layer, delist[0], delist[1])
            
        return combineIdx #All idxs which seem like they might want to be a higher order token.
        pass
 
    def acceptHighToken(highToken):
        #Handles adjusting all other token indexes. Note FairTokens should be able to adjust all the other fair tokens and problem tokens
            #Note if a problem token is accepted, must remove all those which had conflict [and either check again or add to fair idk], and rerun findPotential hightoken [possibly] and check conflict [possibly] since it might've sorted out the problems.
        pass

    def runDeminishPhrase(self):
        self.deminishStatement2(self.currentPhrase, self.cleanWordList, findSpecialSyntax)
        pass

    def getUserResponse(self): 
        response=input("[Y/N]")
        if response=="Y":
            return(response)
        elif response=="N":
            return(response)
        else:
            response=input("[Y/N]") 

     
    def checkConflictsHighTokens(self, highTokens:list[FoundPotentialToken]): #Could be improved. Runs only once per layer, after potential hightoken(s) are found.
        #Check just if there exists a conflict, report all idx's where the conflict occurs.
        #print("CCHT: ",highTokens) 
         
        highTokens=self.sortBy(highTokens, [ [lambda x:(x.getSymbolIndex()), False],[lambda x:(x.getStart()), False], [lambda x:(x.getEnd()-x.getStart()), True] ] )
        #print("CCHT sorted: ",highTokens)
        if len(highTokens)<2:
            return []
        else:
            initialSymbolIdx=highTokens[0].getSymbolIndex()
        seenSpans=[]
        problemPairs=[]
        problemFlag=False
        for token in highTokens: 
            if token.getSymbolIndex()!=initialSymbolIdx:
                seenSpans=[]
                initialSymbolIdx=token.getSymbolIndex()
            for spanIdx in range(len(seenSpans)):
                span=seenSpans[spanIdx]
                #t.end=>s.start #t.start <= s.end #Both - russian doll (or neither?, the opposite, span is inside this span. Shouldn't happen since lambda sorts by span gap, )
                if token.getEnd()>=span.getStart() and token.getStart()<=span.getEnd(): #either one will be true 
                    problemFlag=True
                elif span.getEnd()>=token.getStart() and span.getStart()<=token.getEnd():
                    problemFlag=True
                else: #redundant but assured.
                    problemFlag=False
                if problemFlag:
                    problemPairs.append([span, token]) #span comes first, because it came earlier in the sequence at the very least.
                    problemFlag=False
            seenSpans.append(token)  
        #Token in highTokens = [specialToken, Layer, st, end], conflict if they overlap between two or more tokens. [how to check multiple, unordered pairs?] [Order by widest span?]
    
        return problemPairs #If not empty, the pairs are the problems.     
    
    def sortBy(self, tokens:list[FoundPotentialToken], lambdaKeys:list): #First sort by [0], then sort by [1], then sort by .... [grouping each after each sort by the criteria that came before]
        toDo=lambdaKeys[0]
        tokens.sort(key=toDo[0], reverse=toDo[1])
        #if there are more instructions, find runs and run those instructions on that subset
        if len(lambdaKeys)-1!=0:
            tempRun=[0,0]
            while tempRun[1]<len(tokens):
                if toDo[0](tokens[tempRun[0]])==toDo[0](tokens[tempRun[1]]):
                    tempRun[1]+=1
                else:
                    #print("Found run of ", tempRun[0], ", ",tempRun[1]-1)
                    tokens[tempRun[0]:tempRun[1]]=self.sortBy(tokens[tempRun[0]:tempRun[1]], lambdaKeys[1:]) #Widest range to start, mutates original list. 
                        #NOTE, I think the slicing when passing into sortBy makes it not sort in place :/. What can you do? I suppose. 
                    tempRun[0]=tempRun[1]
                    tempRun[1]=tempRun[0]
            
            #print("Found run of ", tempRun[0], ", ",tempRun[1]-1)
            tokens[tempRun[0]:tempRun[1]]=self.sortBy(tokens[tempRun[0]:tempRun[1]], lambdaKeys[1:]) #Widest range to start, mutates original list.  

        return tokens


   
    
        
    
    #Override 2, try adding back the changing of HighTokenIndexes and SymbolIndexs
    def adjustTokens3(tokenList:list[FoundPotentialToken], adjustList:list[list[int,int,int,int]]):
        #Base case
        if len(tokenList)==0:
            return tokenList, adjustList
        if len(adjustList)==0:
            return tokenList, adjustList 

        def addRunning(running, Adj): 
            if Adj!=None: 
                running[0]=Adj[0]
                running[1]=Adj[1]
                running[2]=Adj[2]
                #running[3]+=Adj[3] simply replaced by ins
            return running
        
        def addChange(running, tkn:FoundPotentialToken): #Might have issues at tkn lengths of 1
            if running[0]!=None and running[0]!=tkn.getSymbolIndex(): #No need to adjust length of string, just the index is required 
                tkn.setSymbolIndex(running[3]+tkn.getSymbolIndex()-1)
            else: 
                newStart=tkn.getStart()-running[2]-1 #old start - running end 
                newEnd=newStart+ tkn.getEnd()-tkn.getStart()
                #newSymbolIdx=running[3] + tkn.getSymbolIndex() #running[3] counts how many words have been added total as a result of the breaks. For example Jacob...,,..., with ..., and ... takne results in 5 string, but only an increase of 4 in index. 
                newSymbolIdx=ins+tkn.getSymbolIndex() #New for replacing above by ins
                tkn.setStart(newStart)
                tkn.setEnd(newEnd)
                tkn.setSymbolIndex(newSymbolIdx) 
    
        ######
        ins=0
        LastIdx=None
        adjIdx=0
        tknIdx=0
        running=[None, None, None, 0]
        print("Trying together now")
        while adjIdx<len(adjustList) and tknIdx<len(tokenList):
            tkn=tokenList[tknIdx] 
            nextAdj=adjustList[adjIdx]
            if nextAdj[0]<tkn.getSymbolIndex():
                print("5") 
                running=addRunning(running, nextAdj) 
                adjIdx+=1  

                if LastIdx==None:
                    LastIdx=nextAdj[0]
                elif LastIdx==nextAdj[0]:
                    ins+=1
                else:
                    LastIdx=nextAdj[0] 


            else: 
                if nextAdj[0]>tkn.getSymbolIndex():
                    print("4")  
                    if running[0]!=None: #Or adjIdx >0?
                        addChange(running, tkn)
                    tknIdx+=1 
                    #ins+=1? #Don't increase insert amount, no split has occured.
                    print("tkn: ",tkn, " try increase of ", ins) #Maybe LastIdx=None?
                else: #nextAdj[0]==tkn.getSymbolIdx()  
                    if nextAdj[2]<tkn.getStart(): #Maybe we should compare start with start instead of end with start... just a thought.
                        print("3")  
                        running=addRunning(running, nextAdj)
                        adjIdx+=1
                        ins+=1 #Split occured
                    else:
                        print("2")  
                        if running[0]!=None: #Should also check running's [0]<=tkn symbol? maybe?
                            addChange(running, tkn)
                        tknIdx+=1 
                        #ins+=1? #No split, so don't increase teh 'insert' amount, I think. Might have to check on a 1 lengt hhigh token...
                        print("tkn: ",tkn, " try increase of ", ins) #Maybe LastIdx=None?


        while tknIdx<len(tokenList):
            tkn=tokenList[tknIdx]
            print("tkn: ",tkn, " try increase of ", ins)
            tknIdx+=1
            tkn.setSymbolIndex(tkn.getSymbolIndex()+ins) #Either stay same or increases.
            
            #ins+=1 ? Only want to increase when a split occurs. Since no split occurs hence forth no need

    #Used before adjustTokens to get the adjust values after accepting, also returns a line with the new informaiton.
    def acceptToken(self, wordList:list[str], inspectTokens:list[FoundPotentialToken]):
        
        def breakUp(cpyWord:str, culprits:list[FoundPotentialToken]):
            adj=[]
            line=[]
            running=0
            adjIndex=0
            if culprits==[]:
                return [], []
            else:  
                crime=culprits.pop(0) 
                RunStart=0
                ADJIDX=1
                SYMIDX=crime.getSymbolIndex() 

                f1=cpyWord[:crime.getStart()]
                f2=cpyWord[crime.getStart():crime.getEnd()+1]
                f3=cpyWord[crime.getEnd()+1:]
                running=crime.getEnd()+1 
                if f1!="":
                    adj.append([SYMIDX, RunStart, crime.getStart()-1, ADJIDX]) 
                    line.append(f1) 
                adj.append([SYMIDX, crime.getStart(), crime.getEnd(), ADJIDX]) 
                line.append(f2)
                RunStart=crime.getEnd()+1 

                while (len(culprits)>0):  
                    cpyWord=f3
                    #print("deal with remaining word(s): ", f3)
                    if (cpyWord==""):
                        break
                    
                    crime=culprits.pop(0)
                    f1=cpyWord[:crime.getStart()-running]
                    f2=cpyWord[crime.getStart()-running:crime.getEnd()+1-running]
                    f3=cpyWord[crime.getEnd()+1-running:]
                    running=crime.getEnd()+1  
                    if f1!="":
                        adj.append([SYMIDX, RunStart, crime.getStart()-1, ADJIDX]) 
                        line.append(f1) 
                    adj.append([SYMIDX, crime.getStart(), crime.getEnd(), ADJIDX]) 
                    line.append(f2)
                    RunStart=crime.getEnd()+1
            
                if f3!="":# in the event len(culprits)==0) 
                    start=max(crime.getEnd()+1, RunStart) 
                    adj.append([SYMIDX, start, start+len(f3)-1, ADJIDX]) #Only one additional left
                    line.append(f3) 

                return line, adj

        inspectIdx=0
        if len(inspectTokens)==0:
            return wordList, [] 
        inspectToken=inspectTokens[inspectIdx]
        newLine=[]
        culprits=[]
        adjustSurvivors=[]#insert error if there is a Token with a wordIndex beyond our wordList (early sanity check)
        for wordIdx in range(len(wordList)):  
            cpyWord=wordList[wordIdx]
            if wordIdx<inspectToken.getSymbolIndex() or len(inspectTokens)==inspectIdx: #Might be an unncessary econd condition here [eh, fine I think in event inspectIdx over extends]
                #print("Needs testing!") #NOTE TEST ME, jacob...,,... x2, and only take both high tokens fro the first. triggers.
                newLine.append(cpyWord)
            else:  
                while wordIdx==inspectToken.getSymbolIndex(): 
                    if len(inspectTokens)==inspectIdx: 
                        break
                    else: 
                        culprits.append(inspectToken)
                        inspectIdx+=1
                        if inspectIdx<=len(inspectTokens)-1: 
                            inspectToken=inspectTokens[inspectIdx] 
                x,y=breakUp(cpyWord, culprits) #returns a list to join with the new line, and a list to join with the adjust 
                culprits=[]
                newLine.extend(x)
                adjustSurvivors.extend(y) 
    
        return newLine, adjustSurvivors
    
        """testList1=["NOBREAKORREMOVE", "...,..." , "NOBREAK", 
                   "NOBREAK", "...,...,..." , "...,...,...,..." , 
                   "NOBREAK", "NOBREAK", "NOBREAK"]
            wordList=testList1
            line, adjusts=acceptToken(wordList, inOrder) 
            print("resulting line: ",line)
            print("resulting adjusts: ", adjusts) 

            inOrderSurvivor=[]   
            adjustTokens3(inOrderSurvivor, adjusts)
            print(inOrderSurvivor) 
            print("e Test if breaks are alright")
            print("\n")"""

    def problemPairSanityCheck(survivorProblemList, problemPairs):
        propPair=0
        while probPair<len(problemPairs):
            problemPair=problemPairs[problemPair]
            if problemPair[0] not in survivorProblemList or problemPair[1] not in survivorProblemList:
                problemPairs.pop(problemPair)
            else:
                probPair+=1
        return problemPairs  




#----- Find special Syntax and Conflicts in that (unintentional grammer conplexity) ----- 
#highTokens=findSpecialSyntax(wordList,"...", self.totalLayers) #Find potential recombinations of tokens for higher order tokens  
def fastFindSpecialSymbol1(wordList:list[str], specialSymbols:list[str], layer:int): #This function looks like it works best for 'highly recursive' string stuctures like ellipses, but otherwise too messy I think
    #Idea one: 
    foundPotentialTokens=[]
    sTokenList=[]
    for symbol in specialSymbols:
        sTokenList.append([symbol, [0]*len(symbol), 0])
    for wordIdx in range(len(wordList)):
        if wordIdx!=0: #Reset sTokenInfo per word
            for sTokenInfo in sTokenList:
                for idx in range(len(sTokenInfo[0])):
                    sTokenInfo[1][idx]=0
                sTokenInfo[2]=0
        word =wordList[wordIdx]
        for chrIdx in range(len(word)):
            for sTokenInfo in sTokenList:
                symbolLength=len(sTokenInfo[0])  
                for i in range(sTokenInfo[2]+1): 
                    if word[chrIdx]==sTokenInfo[0][sTokenInfo[1][i]]:
                        sTokenInfo[1][i]+=1
                        if sTokenInfo[2]<symbolLength-1: #Note, this may be a problem, say in the case .....I.... we might end up all once again at the same, perhaps we can minus 1 when we fail? and shift right all the others? 
                            sTokenInfo[2]+=1 
                        if sTokenInfo[1][i]==symbolLength: #Found fill string
                            sTokenInfo[1][i]=0
                            foundPotentialTokens.append(FoundPotentialToken(sTokenInfo[0], 0, chrIdx-symbolLength+1, chrIdx, wordIdx)) #FoundPotentialToken basically NOTE FUTURE, layer should be corrected for now lots of layer location default to 0
                    else:
                        sTokenInfo[1][i]=0
                        sTokenInfo[2]=0
    #I essentially temporarily double the specialtoken list. it's fine for small lists but on large langauges might become irksome.         
    return foundPotentialTokens


 


def main():
    #region
    #only Read file -Math
    #replace everything that is not a logicSymbol with "\\expr" (or remove)
        #The read file can be stolen from MarkFile mostly
        #Markov Chain with the resulting strings? Maybe?

    #Graph of possible substring combos <-requires some tokens to be created
    #Deminish each line to be expr and a series of logical symbols/special tokens
    #Make a copy of this 'deminished line', for each logic symbol
    #Go through each logic symbols graph, and demarkate each instance of that tree [so if the root branches into two symbols, if either symbol occurs again and isn't specified to self loop, make a copy skip the first and continue after demarking the first]
    #Report each as a string with a substring beneath each word that demarks it's 'ownership'. 
        #Report conflicts and compatible symbol graph decisions, so that we can think of markov chain stuff.
        #Each sub expression is therefore 'carved' out of these niches.
        #Also, try to report the least amount of strings, so combos that work well together (no overlap).
        #These might be booled flags.
    #string -> deminish string (into tokens/words) -> test graph symbols (each requires a copy of the deminish, and an array equal to the symbols) (copies required per possible split) ->collect those deminished symbol graph strings -> compare them and report good combines, or confusions between symbol graphs.

    #Special tokens should check a passed expression class that will handle that kind of special expression...
        #How should this be done? Needs access to the graph, the statement, and the actual special token(s) specified by user.
    #Get Statement, deminish it, go through each SymbolGraphs, split when choices are possible, join the arrays. And give a value to each graph, and instance when marking the statement.
            #Try to combine annd report conflicts and rank how likely those statements are basedo n how much information we can extract. 

    #The statements might be able to make markov based on corrective Person assisted vs Machine assisted versiosn.

    #Special Token Graph/super class collection (Abstract class/interface class), determines how special tokens are handled
    #Create speical token handles
    #Create symbol graphs for each of the important statements
    #Clean strings [plurals for logics removed] <-this might be run multiple times based on deminish statement findings...?
    #Get statement, deminish statement, 
    #Test deminish statement copies through each symbolGraph, and split when decisions are made
        #And then keep track of each symbolGraph instance, split path, and type of symbolgraph root, 
        # collect all findings of each, try to merge nonconflictary findings, based on having different roots and non conflicts
        # Report back how many conflicts are in each word per statements, and which statements are most likely to conflict (These suggest markov or a hierarchy is to be produced)
    #endregion
    
    testStatement1= "If x is an Integer, then either x is positive, x is negative, or x is zero."
    "[varName:X, groups:Integer, Number, Labels:Positive,negative, or zero], falseLabels=[]"
    "X is positive"
    "[varName:X, groups: Integer, Number, Labels:Positive, falseLabels[Negative, Zero]"
    "X is an integer, and it is positive"
    
    testStatement2= "If x is an Integer, then either x is positive or negative, when x is not zero." 
    testStatement3= "If x is a Real Number, then x can be a Rational number, or an Irrational number."
    testStatement4="If x is a non-negative Integer, then x is either a Prime or a unique Sum of Primes."
    testStatement5="If x is Infinity, then x>0, x>1, x>2..."
    testStatement6="If x is Infinity, then x>0, x>1, x>2...." #Problem should be deteced at end.
    testStatement7="1 2  3   4    ."
 

    #Step 1, deminish the phrases.  


    TS1=PhraseRecord(testStatement1)  
    #print(prettyPrintMatrix(TS1.getProblemMatrix())) 

    print("Test the promptUser for phrase")
    hypetheticalString="Jacob... Hilst... Matthew..... King... Chaos.... Anti..."
    print(hypetheticalString.split(" "))
    TS2 = PhraseRecord(hypetheticalString)
    TS2.deminishStatement2(TS2.currentPhrase, None, fastFindSpecialSymbol1)

    #TS2.promptUser([FoundPotentialToken("...", 0, 0, 2),FoundPotentialToken("Jacob", 0, 3, 7)], [[FoundPotentialToken("Hil",0, 8, 11), FoundPotentialToken("Hilst", 0, 8, 13)]], hypetheticalString, [FoundPotentialToken("Hil",0, 8, 11), FoundPotentialToken("Hilst", 0, 8, 13)])
 

    pass

if __name__=="__main__":
    main()

#Note for future Jacob. Left off with the commands. 
    #The tokenizing of the string [I would like to retain spaces for most applications of the code I believe]
    #The UI parse response[2] (The array of possible tokens to exclude/include) and then return the new phrase after checking against these.
        #It's simply a matter about organizing the parsable token info appropriately. PrettyPrints should have a function that allows for a string array to be made into a proper array of strings. "[1,2,3, [1,2,3]]"  -> ["1", "2", "3", ["1","2","3"]]
    #Then, after the UI is complete, the project is supposed to pivot onto symbol graphs/syntax trees to inform how to handle conflicts, and suggest new graphs to try.

    #Applications to apply to: Yugioh Effect Text [to make rudamentry pseudo code per card, and detect 'old' language that could be rephrased to the modern level]
                            #Math Theorems, to organize information and statements, and apply scripts to retained values.

    #Finally, use AI techniques with Stats and the accumulated data to iterate on the suggested graphs/wording.
        #Old phrases -> new phrases via what 'should' have been created for them in the yugioh effect sense.

#Benefits of this project:
    #Allows for a front end for organizing information, and suggesting new experimetns.
        #An individual should be able to make a new symbol graph [such as 'if x is matrix, try to find deter.'] such that the program can help 'guide' someone from their own work/notes.
 