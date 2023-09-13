from PrettyPrints import prettyPrintMatrix

specialTokens=["\\expr", "..."]; #Expr is any string. Parsed later basically, or of lower priority  Perhaps a [min, max] will be created which will let the parser know how much of something to expect.
logicSymbols=["if", "then", "otherwise", "else", ",", ".", "and", "or", "cannot", "be", "exists","exist", "there",  
              "for", "all", "every", "is", "are", "an", "a","must","only","case","cases"]
reservedTokenHead="/\\"

#Error when symbols aren't found when expected
class SymbolException(Exception):
    """To catch undefiend tokens/symbols, for when user defines custom semantic graphs"""
     
    def __init__(self, message):
        if message=="":
            self.message="Symbol not found in logicSymbols or specialTokens"   
        else: 
            self.message=message 
        super().__init__(self.message)
  
#Rule set for each phrase - may symbolize the CNF form, or CFG form.
class SymbolGraph:
    root:str
    nodes=[] #Each value should be unique.
    arcs=[] #Each arc should be unique.

    def __init__(self, symbolRoot):
        try:
            self.setRoot(symbolRoot)
        except SymbolException as e: #Just raise a warning
            print(e.message) #message
            symbolRoot=""

        self.root=symbolRoot
        self.arcs=[]
        
    def setRoot(self, symbolRoot):    
        try:
            self.checkSymbol(symbolRoot)
        except SymbolException as e: 
            self.root="" #default behavior make it impossible to enter
            print(e.message)
        self.root=symbolRoot
        self.nodes.append(self.root)

    def checkSymbol(self, symbol):
        if symbol not in specialTokens and symbol not in logicSymbols: 
            raise SymbolException("")
        pass

    def addArc(self, parent, child):
        #Legitimate symbols
        try:
            self.checkSymbol(parent)
        except SymbolException as e:
            print(e.message)
            return -1 #Hard fail
        try:
            self.checkSymbol
        except SymbolException as e: 
            print(e.message)
            return -2
        if [parent,child] in self.arcs:
            return 0 #Already inside
        if parent in self.nodes:
            self.addNode(child)
            self.arcs.insert([parent, child])
        return 1
    
    def addNode(self, node):
        if node not in self.nodes: #Assume each symbol can appear at most once in the graph.
            self.nodes.insert(node)
            return 1
        return 0
    
    def removeArc(self, parent, child):
        try:
            self.checkSymbol(parent)
        except SymbolException as e:
            print(e.message)
            return -1 #Hard fail
        try:
            self.checkSymbol(child)
        except SymbolException as e: 
            print(e.message)
            return -2
        try:
            self.arcs.remove([parent, child])
        except ValueError as e:
            return 0 #handled, nothing removed
        
        self.removeNode(child) 

        return 1 

    def removeNode(self, child):
        #Remove only when there are no arcs to said node.
        found=False
        for arc in self.arcs:
            if arc[1]==child:
                found==True
                break
        if found==True:
            return -1 #There still exists a arc connecting to this node
        else: #There is no arc to this node, remove it. 
            try:
                self.nodes.remove(child) #Removes by value, since each value should be unique it should be fine.
            except ValueError as e:
                return 0
        return 1

#Collection of symbol graphs,, I suppose this would be our 'language' resulting from CFG's. 
class SymbolGraphs:
    pass

 

class FoundPotentialToken(): #The idea is that the sets_ will let us change the start/end when accpeting fair tokens across pairs and the unqiue list 
    tokenSymbol:str
    layer:int
    start:int
    end:int
    def __init__(self, tS:str, l:int, s:int, e:int):
        self.tokenSymbol=tS
        self.layer=l
        self.start=s
        self.end=e
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
        return "["+self.tokenSymbol+", "+ str(self.layer)+", "+str(self.start)+", "+str(self.end)+"]"
    def __repr__(self): #print 
        return "["+self.tokenSymbol+", "+ str(self.layer)+", "+str(self.start)+", "+str(self.end)+"]"
   
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
        self.createMatrices()

    def getProblemMatrix(self):
        return self.problemMatrix
    
    def forceTestValueMatrices(self, matrix:0|1|2, col:int, row:int, value:int): #Temp to test expected matrix behavior.
        if matrix==0:
            self.problemMatrix[col][row]=value
        elif matrix==1:
            self.fairMatrix[col][row]=value
        elif matrix==2:
            self.totalTokensMatrix[col][row]=value
        else:
            raise ValueError("Matrix integer is incorrect")

    def createMatrices(self): #Assumes specialtokens and logic symbols are defined. FUTURE: Should make the matrices able to 'eliminate' rows and columns if symbols change, or 'append' if symbols change. Vectors/linked lists might be best for this application!
        #CTRLF NOTE SUBROUTINE #NOTE: This might be a utility function later (unique(iterable, sorting method)), used in other places as well 
        recognizedSymbols=set(specialTokens+logicSymbols) #dict map symbol to a value? Faster matrix lookup.
        recognizedSymbols=list(recognizedSymbols)  
        recognizedSymbols.sort()

        #Could compare these with a confusion matrix to test classification expectations quickly? Or an acceptable accuracy?
        symbolCount=len(recognizedSymbols)
        self.problemMatrix=[[0]*(symbolCount+2) for i in range(symbolCount+2)] 
        self.fairMatrix=[[0]*(symbolCount+2) for i in range(symbolCount+2)] 
        self.totalTokensMatrix=[[0]*(symbolCount+2) for i in range(symbolCount+2)] 
        self.symbolDict =dict()
        
        for i in range(2, symbolCount+1): #I NEED AN ADDITIONAL EMPTY ROW/COLUMN NEXT TO each symbol.
            self.symbolDict[recognizedSymbols[i-2]]=i
            self.problemMatrix[0][i]=recognizedSymbols[i-1]
            self.problemMatrix[i][0]=recognizedSymbols[i-1]
            self.fairMatrix[0][i]=recognizedSymbols[i-1]
            self.fairMatrix[i][0]=recognizedSymbols[i-1] 
            self.totalTokensMatrix[0][i]=recognizedSymbols[i-1] #NOTE, unclear use?
            self.totalTokensMatrix[i][0]=recognizedSymbols[i-1]
        print("matrices made")

        #Additional labels 
        self.problemMatrix[0][1]=reservedTokenHead+"Total"
        self.problemMatrix[1][0]=reservedTokenHead+"Total"
        self.fairMatrix[0][1]=reservedTokenHead+"Total"
        self.fairMatrix[1][0]=reservedTokenHead+"Total"
        self.totalTokensMatrix[0][1]=reservedTokenHead+"Total"
        self.totalTokensMatrix[1][0]=reservedTokenHead+"Total"

        #Too long, would like just the last word, the address, maybe at most
            #self.problemMatrix[0][0]=reservedTokenHead+str(self)
            #self.fairMatrix[0][0]=reservedTokenHead+str(self)
            #self.totalTokensMatrix[0][0]=reservedTokenHead+str(self)
            
        self.problemMatrix[1][1]=reservedTokenHead+"-"
        self.fairMatrix[1][1]=reservedTokenHead+"-"
        self.totalTokensMatrix[1][1]=reservedTokenHead+"-"

    def pushPhrase(self, phrase:str, fairTokens:list, problemTokenPairs:list):
        self.totalLayers+=1
        self.phraseHistory.append(phrase)
        self.fairTokenHistory.append(fairTokens)
        self.problemTokenHistory.append(problemTokenPairs) #NOTE this and the others need to be made into deep copies or constructors' in form of a list, otherwise history get's eddited as tokens are accepted and adjusted.
        self.matchCurrentPhraseWithHistoryPhrase()

    def popPhrase(self) ->int:
        if self.totalLayers>0:
            self.totalLayers-=1
            self.phraseHistory.pop()
            self.fairTokenHistory.pop()
            self.problemTokenHistory.pop()
            self.matchCurrentPhraseWithHistoryPhrase()
            return 0
        else:
            return -1 #fail

    def checkAssumptions(self):
        #Not in any order of severity. If positive okay, if negative able to trace back the problem.
        if len(self.problemTokenHistory)==len(self.fairTokenHistory)==self.totalLayers and self.totalLayers>=0: #Base cases stand
            if self.currentPhrase==self.phraseHistory[len(self.phraseHistory)-1]: #current phrase set up correctly
                if self.problemTokenHistory[0] == self.fairTokenHistory[0]==[]: #Original case history is fine
                    return 1
                else:
                    return -1
            else:
                return -2
        else:
            return -3
    
    def matchCurrentPhraseWithHistoryPhrase(self): #Ensures the currentPhrase is matching with the end of the history of Phrases.
        mostRecentPhrase =self.phraseHistory[len(self.phraseHistory)-1]
        if self.currentPhrase != mostRecentPhrase:
            self.currentPhrase=mostRecentPhrase

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

    def checkConflictsHighTokens(highTokens): #Could be improved. Runs only once per layer, after potential hightoken(s) are found.
        #Check just if there exists a conflict, report all idx's where the conflict occurs.
        #print("CCHT: ",highTokens) 
        highTokens.sort(key=lambda x:(x.getEnd()-x.getStart()), reverse=True) #Widest range to start, mutates original list. 
        #print("CCHT sorted: ",highTokens)
        seenSpans=[]
        problemIdxPairs=[]
        problemFlag=False
        for token in highTokens:
            for span in seenSpans:
                #t.end=>s.start #t.start <= s.end #Both - russian doll (or neither?, the opposite, span is inside this span. Shouldn't happen since lambda sorts by span gap, )
                if token.getEnd()>=span.getStart(): 
                    problemFlag=True
                elif token.getStart()<=span.getEnd(): #either one will be true 
                    problemFlag=True
                if problemFlag:
                    problemIdxPairs.append([token, span])
                    problemFlag=False
            seenSpans.append(token)

        #Token in highTokens = [specialToken, Layer, st, end], conflict if they overlap between two or more tokens. [how to check multiple, unordered pairs?] [Order by widest span?]
        return problemIdxPairs #If not empty, the pairs are the problems.     
        
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

    def recordTokens(self, fairTokens:list[FoundPotentialToken], problemHighTokenPairs:list[list[FoundPotentialToken]]):
        #temporary but know what they mean in my own way 
        #record tokens appeared and phrase before accepting.
        for fairToken in fairTokens:
            #A simple matrix would do, but not sure what else it might be useful for.
            self.fairMatrix[self.symbolDict[fairToken.getTokenSymbol()]][self.symbolDict[fairToken.getTokenSymbol()]]+=1 
        for problemPair in problemHighTokenPairs: 
            #ProblemMatrix[col][row], s.t. row<=col
            locationPlace=[self.symbolDict[problemPair[0].getTokenSymbol()], self.symbolDict[problemPair[1].getTokenSymbol()]].sort(key=lambda x:x, reverse=True) #upper triangular required for tracking the symbols which conflict
            if problemPair[0].getStart() == problemPair[1].getStart(): #NOTE, if the symbols are teh same, it ends up counting int hte middle without a clear winner [that's fine I think?]
                if problemPair[0].getEnd()== problemPair[1].getEnd():
                    #Impossible! They must be the same token!
                    raise ValueError("Two tokens seem to be the same based on how Problems arise and how it's checked!")
                else:
                    problemPair.sort(key=lambda x:x.getEnd(),reverse=True)
            else:
                problemPair.sort(key=lambda x:x.getStart())
            #So earlier is prefered, or the longest is prefered. the prefered always ends up as the first index, [0], and the nonprefered as teh second [1]
            #This makes the column preference more visible to me
            locationPlace=[self.symbolDict[problemPair[0].getTokenSymbol()],self.symbolDict[problemPair[1].getTokenSymbol()]]
            self.problemMatrix[locationPlace[0]][locationPlace[1]] 
 
    def checkConflictsHighTokens(self, highTokens:list[FoundPotentialToken]): #Could be improved. Runs only once per layer, after potential hightoken(s) are found.
        #Check just if there exists a conflict, report all idx's where the conflict occurs.
        #print("CCHT: ",highTokens) 
        highTokens.sort(key=lambda x:(x.getEnd()-x.getStart()), reverse=True) #Widest range to start, mutates original list. 
        #print("CCHT sorted: ",highTokens)
        seenSpans=[]
        problemIdxPairs=[]
        problemFlag=False
        for token in highTokens:
            for span in seenSpans:
                #t.end=>s.start #t.start <= s.end #Both - russian doll (or neither?, the opposite, span is inside this span. Shouldn't happen since lambda sorts by span gap, )
                if token.getEnd()>=span.getStart() and token.getStart()<=span.getEnd(): #either one will be true 
                    problemFlag=True
                elif span.getEnd()>=token.getStart() and span.getStart()<=token.getEnd():
                    problemFlag=True
                else: #redundant but assured.
                    problemFlag=False
                if problemFlag:
                    problemIdxPairs.append([token, span])
                    problemFlag=False
            seenSpans.append(token)

        #Token in highTokens = [specialToken, Layer, st, end], conflict if they overlap between two or more tokens. [how to check multiple, unordered pairs?] [Order by widest span?]
        return problemIdxPairs #If not empty, the pairs are the problems.     
         
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
        #Temporarily going to ignore user input stuff, since I'm becoming more sure that I want to fully seperate the stuff, but suggest the structure to the user somehow :/...


        #Clean/seperate tokens
        #Find potential recombinations of tokens for higher order tokens
        #find conflicts in the potential - fair tokens, problem tokens
        #record phrase, and tokens before accepting.
        #accept tokens
            #adjust tokens, new string
        #record remaining tokens, new phrase

        wordList=additionalTokenSeperation(phrase) #Clean/seperate tokens
        #Layer 0, assuming this is what is desired. 

        #----- Find special Syntax and Conflicts in that (unintentional grammer conplexity) ----- 
        highTokens=findSpecialSyntax(wordList,"...", self.totalLayers) #Find potential recombinations of tokens for higher order tokens  
        
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
            fairTokens.sort(key=lambda x:x.getStart())
         
        print("fairTokens : ", fairTokens)

        #TODAY: Accept tokens, 1 hr, track accept reject conflict and conflict winners 20 minutes
            #When accepting tokens a sub routine must be run:
                #All tokens beyond that particular token must be moved by a length of that token
                    #If it is a token with a problem, then when accepting delete every problem pair that includes that token. (perhaps sort problem tokens, also be sure problem token pairs are sorted by first appearence?)
        
        #1 hr, accept reject tokens user input
        #2 hours fast matrix special syntax (change to symbol) search, assume length 1 token, matrix of indexes? /fail fast?
        #1 hr  reserved symbols (disallow inputs to start with that reseserved symbol. this includes: Symbols, Symbol Graphs[since \ is for special syntax with functionality or meaning], )
        self.recordTokens(fairTokens, problemHighTokensPairs) #Record token conflicts and fair tokens for later analysis.
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

    def promptUser(self, fairTokens:list, problemHighTokenPairs:list[list[FoundPotentialToken]], wordList:list[str], problemHighTokens:list[FoundPotentialToken]):
        #Commands
        print("Accept fair tokens?")
        response=None 

        def acceptToken(type:int (0|1|2|3), inspectTokens:list[FoundPotentialToken]): 
              #do with tokens as desired
                #acceptTokens(type:int (0:fair|1:problem), skipList:list[FoundPotentialToken]) 
                #accept tokens (and record outcome) 
                    #if fair, fastadjust all other tokens (fair/problem)
                    #If problem, fast adjust all fairs (as appliable), and remove all conflicting tokens wit hthat token
                        #for problem, show all competing problems, and the current phrse and original phrase (current being the new statement with problems acting on it, or fairs already accepted on it)
            #accept tokens should be run until either tokens are exhausted, or a command is given to break from handling.
            nonlocal problemHighTokenPairs #remove conflicts when accepting or handling one over the other.
            nonlocal problemHighTokens #fast adjust indexes
            nonlocal fairTokens  
            
            #NOTE - can be imrpoved by using a list to keep track of which tokens to move and how much (just requires more operations intermidetly. and a moving head)
            #ASSERT There are no conflicts in inspectTokens, and that inspectTokens is ordered by earliest START index in the string.
            runningDifference=0
            insIdx=0
            while (len(inspectTokens)>insIdx):
                inspectToken=inspectTokens[insIdx]
                difference=inspectToken.getEnd()-inspectToken.getStart()+1
                print("current difference, runningdifference", difference, " ", runningDifference)
                if type==0:#0 accept fair token, adjust fair token
                    for token in fairTokens:
                        if inspectToken.getEnd()-runningDifference <token.getStart():
                            print("0 Adjust token ", token.getTokenSymbol()," by the inspect token", inspectToken.getTokenSymbol())
                            print("1 token start, end ",token.getStart(), token.getEnd())
                            token.setStart(token.getStart()-difference)
                            token.setEnd(token.getEnd()-difference)
                            print("2 token start, end ",token.getStart(), token.getEnd())
                    pass
                elif type==1: #1 accept problem adjust problem
                    pass
                elif type==2:#2 accept fair, adjust problems
                    for token in problemHighTokens:
                        if inspectToken.getEnd()-runningDifference<token.getStart():  
                            print("inspectToken ", inspectToken.getEnd())
                            print("token position before [",token.getStart(),", ",token.getEnd(), "]")
                            token.setStart(token.getStart()-difference)
                            token.setEnd(token.getEnd()-difference)
                            print("token position after [",token.getStart(),", ",token.getEnd(), "]")
                    pass
                elif type==3: #3 accept problem, adjust fairs
                    pass
                insIdx+=1
                runningDifference+=difference  
            pass

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
                acceptToken(0, acceptedTokens) #inspect the token, adjust all those after it's index
                acceptToken(2, acceptedTokens) #Adjust all the problem tokens as well    
                self.pushPhrase(newList, fairTokens, problemHighTokenPairs) #NOTE Perhaps make shallow/deep copies? Since editing in the past would edit all the recorded ones. 
            else:
                #Virtually the same, accept when accepting, we must remove all conflicts with that inspected token. It's already an adjacency list so not much improvement can be done to the search.
                print("implement later")
                pass

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
            badTokens=[] 
            for token in tokens:
                if token not in self.symbolDict.keys():
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
                print("Commands:\n 'yes': accept all fair tokens.\n",
                      "'no': skip all fair tokens.\n ",
                      "'yes ['tokens']': yes followed by a list of tokens means accept all of these specific tokens.\n",
                      "'no ['tokens']': no followed by a list of tokens means reject these specific tokens, accept the rest.\n",
                      "'tokens?': prints a list of current fair tokens.\n",
                      "'inspect':returns the information of each fair token, and the original phrase, and the current phrase.\n",
                      "'exit': Assumes this prompt was incurred in error, will resolve without doing anything.")
                response=None
            else:
                #assert response must be a strength of len 0 or more 
                if response[0]=='no' :
                    if response[1]!='':
                        print("recieved no ...")
                        print("response[1] : ",type(response[1]), response[1]) 
                        tokens=trimAndVerify(response[1]) #Notice the response is set to None non-locally inside these functions
                        if response==None:
                            print("try again")
                            continue #something must've failed, try again
                        print("accept tokens into new line - assuming fair, and skipping ", tokens)

                        print("current line : ", self.currentPhrase)
                        print("current fair tokens : ",fairTokens)
                        print("current problem tokens : ", problemHighTokens) 
                        createNewLine(0, tokens) 
                        print("new line : ", self.currentPhrase)
                        print("new fair tokens : ",fairTokens)
                        print("new problem tokens : ", problemHighTokens) #NOTE, should likely sort problemHighTokens by start.
                        #do with tokens as desired
                         #acceptTokens(type:int (0:fair|1:problem), skipList:list[FoundPotentialToken]) 
                            #accept tokens (and record outcome) 
                                #if fair, fastadjust all other tokens (fair/problem)
                                #If problem, fast adjust all fairs (as appliable), and remove all conflicting tokens wit hthat token
                                    #for problem, show all competing problems, and the current phrse and original phrase (current being the new statement with problems acting on it, or fairs already accepted on it)
                        #accept tokens should be run until either tokens are exhausted, or a command is given to break from handling.
                        
                    
                    
                    else:
                        print("recieved no")



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









#These three are for deminish1. 
#assumption: Punctuation might be tokens of worth. Math statements don't have spaces, but are allowed them.
def cleanWordList(wordList:list[str]): 
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
        return newList
 
def findSpecialSyntax(wordList:list[str], specialToken="...", Layer=0): #this allows prioirtys to be made.
    #Find ellipses, or combos of special tokens?
        #A matrix might be useful, or a list of indexes for which the current word Idx is acceptable for that token, reset when not, or reset when complete... Not clear how I may do this efficently besides this to go through just once. Would have to alter how the stagger happens, and how recursion may be handled again.
    specialToken0=specialToken #Example is the ...
    sT0idx=0
    combineIdx=[]
    for wordIdx in range(len(wordList)):
        pass
    wordIdx=0
    while (wordIdx < len(wordList)):
        #Special token matching, ideally make anonymous and general for each special token.
        if wordList[wordIdx]==specialToken0[sT0idx]:
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
        combineIdx[combo]=FoundPotentialToken(specialToken, Layer, delist[0], delist[1])
         
    return combineIdx #All idxs which seem like they might want to be a higher order token.

def checkConflictsHighTokens(highTokens): #Could be improved. Runs only once per layer, after potential hightoken(s) are found.
    #Check just if there exists a conflict, report all idx's where the conflict occurs.
    #print("CCHT: ",highTokens) 
    highTokens.sort(key=lambda x:(x.getEnd()-x.getStart()), reverse=True) #Widest range to start, mutates original list. 
    #print("CCHT sorted: ",highTokens)
    seenSpans=[]
    problemIdxPairs=[]
    problemFlag=False
    for token in highTokens:
        for span in seenSpans:
            #t.end=>s.start #t.start <= s.end #Both - russian doll (or neither?, the opposite, span is inside this span. Shouldn't happen since lambda sorts by span gap, )
            if token.getEnd()>=span.getStart(): 
                problemFlag=True
            elif token.getStart()<=span.getEnd(): #either one will be true 
                problemFlag=True
            if problemFlag:
                problemIdxPairs.append([token, span])
                problemFlag=False
        seenSpans.append(token)

    #Token in highTokens = [specialToken, Layer, st, end], conflict if they overlap between two or more tokens. [how to check multiple, unordered pairs?] [Order by widest span?]
    return problemIdxPairs #If not empty, the pairs are the problems.     
    

 




def TestPhrase(phrase:PhraseRecord):
    if phrase.totalLayers==0:
        phrase.cleanWordList() #should only have to run once... I think
    highTokens=phrase.findPotentialHighToken("...", phrase.totalLayers) #Should be replaced with ...highToken(s) when that's rigged up.
    newList=[], problemHighTokensPairs=[]
    if len(highTokens)>1:
        problemHighTokensPairs=phrase.checkConflictsHighTokens(highTokens) #Insert=True means it's save to add all, 
    def getUniqueItemsInListOfPairs(listOfPairs):
        unique=set() #NOTE, whenever list to set, make sure it is sorted, otherwise the order is non determinate.
        for pair in listOfPairs: 
            for problem in pair: 
                unique.add(problem) 
        unique=list(unique)
        return unique
    problemHighTokens=getUniqueItemsInListOfPairs(problemHighTokensPairs) 
    #recognizedSymbols.sort() #Super required when used.
    fairTokens=[i for i in highTokens if i not in problemHighTokens]  #Fair tokens are those that can be applied without conflict
    #initialize a few matrix, with row/col demarked with the syntax arrays. -FUTURE, specified for the langauge the phrase was added to
        #Logic+Special [logic are expected to contirbute to the structure of the sentence/intepretation, special would be demarking some special behavior - special are also those to be checked when recombining]
            #So Unique(Logic+Special)  


def deminishStatement(phrase:str):
    wordList=phrase.split(" ") 
    wordList=cleanWordList(wordList) #Seperate all punctaution
    print(wordList)
    #----- Find special Syntax and Conflicts in that (unintentional grammer conplexity) -----
    Layer =0
    highTokens=findSpecialSyntax(wordList,"...", Layer) #'recombine' possibilities for higher order tokens.
    #[[sT, Layer, start, end]], thus we can merge a lot of high tokens to start if desired, and prioritize different or similar special Tokens... Layer lets us know how 'processed' it is.
    print("High tokens found:", highTokens)
    
    newList=[] 
    problemHighTokensPairs=[]
    if len(highTokens)>1:
        problemHighTokensPairs=checkConflictsHighTokens(highTokens) #Insert=True means it's save to add all, 
    
    #ProblemHighTokensPairs can be handled later by user algorithm
    print("Problem High token Pairs: ", problemHighTokensPairs)

    #Substep Standard report unique problems, preserve problem pairs for data retreival. 
    problemHighTokens=set()
    for pair in problemHighTokensPairs: 
        for problem in pair: 
            problemHighTokens.add(problem) 
    problemHighTokens=list(problemHighTokens)

    print("Problem high tokens unique list: ", problemHighTokens)
    #This should adjust the problem highTokens maybe, or be moved to a new function for applying.
    fairTokens=[i for i in highTokens if i not in problemHighTokens]  #Fair tokens are those that can be applied without conflict
     
    print("fairTokens: ",fairTokens)
    if len(fairTokens)>1:
        fairTokens.sort(key=lambda x:x.getStart())   #Should be able to apply so sort by earliest featured. Perhaps apply to a copy string? Again must move the problem token ranges appropraitely.
 
    fTidx=0
    newList=[]
    wordIdx=0
    while wordIdx<len(wordList):
        if fTidx<len(fairTokens):
            if wordIdx==fairTokens[fTidx].getStart(): #If the idx is equal to the start of a fair token, handle it
                while(wordIdx<fairTokens[fTidx].getEnd()): #final symbol will be iterated by end of the loop
                    wordIdx+=1
                newList.append(fairTokens[fTidx].getTokenSymbol())
                fTidx+=1
            else:
                newList.append(wordList[wordIdx])
        else:
            newList.append(wordList[wordIdx])    
        wordIdx+=1
    wordList=newList

    #Go through problems' and adjust their positions. [assuming fair tokens accepted]
    # Problem/Fair tokens should be given own class, would help organize data easier
    

    print("New Word List with Fair HighTokens ", wordList)        #Missing the ... and kept the . . ., so that needs to be solved.

    #then this function needs to be broken up a bit. So that there is an opportunity for a user to handle the problems, or ignore and let them accumulate.
        #If allow accumulate, we need to somehow reduce the problem locations to where they would be after adding in the changes.
            #This suggests the wordList should become a class that 'listens' to it's own changes and keepts track of those token lists.

    #So the current problem path string->token find/create/substitute -> token ownership for statements -> graph ownership statements into entry and exit nodes and the 'rigor' of such statements.
    


def main():
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
    deminTS1 = deminishStatement(testStatement1)
    deminTS1 = deminishStatement(testStatement5)
    deminTS1 = deminishStatement(testStatement6)
    #deminTS1 = deminishStatement(testStatement7)


    TS1=PhraseRecord(testStatement1)
    try:
        TS1.forceTestValueMatrices(4,1,2,666)
    except ValueError as e:
        print(e)

    TS1.forceTestValueMatrices(0,1,2,666)

    print(prettyPrintMatrix(TS1.getProblemMatrix())) 

    print("Test the promptUser for phrase")
    hypetheticalString="Jacob... Hilst... Matthew..... King... Chaos.... Anti..."
    print(hypetheticalString.split(" "))
    TS2 = PhraseRecord(hypetheticalString)
    TS2.deminishStatement2(TS2.currentPhrase, cleanWordList, findSpecialSyntax)

    #TS2.promptUser([FoundPotentialToken("...", 0, 0, 2),FoundPotentialToken("Jacob", 0, 3, 7)], [[FoundPotentialToken("Hil",0, 8, 11), FoundPotentialToken("Hilst", 0, 8, 13)]], hypetheticalString, [FoundPotentialToken("Hil",0, 8, 11), FoundPotentialToken("Hilst", 0, 8, 13)])
 

    pass

if __name__=="__main__":
    main()