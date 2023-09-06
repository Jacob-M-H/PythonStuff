  

specialTokens=["\\expr"]; #Expr is any string. Parsed later basically, or of lower priority  Perhaps a [min, max] will be created which will let the parser know how much of something to expect.
logicSymbols=["if", "then", "otherwise", "else", ",", ".", "and", "or", "cannot", "be", "exists","exist", "there",  
              "for", "all", "every", "is", "are", "an", "a","must","only","case","cases"]

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

def checkConflictsHighTokens(highTokens): 
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
    


class PhraseRecord():#https://stackoverflow.com/questions/70507587/storing-list-of-strings-that-have-a-format-variable might have some use
    totalLayers:int
    ORIGINALPHRASE:str
    currentPhrase:str
    phraseHistory:list[str] #not sure if this is correct notation(s)
    problemTokenHistory:list[list[list]]
    fairTokenHistory:list[list[list]] 

    #User inputed functions -passed as arguments to the class?  
    def __init__(self, orgPhrase):
        self.ORIGINALPHRASE=orgPhrase #Declare const/final?
        self.totalLayers=0
        self.currentPhrase=self.ORIGINALPHRASE 
        self.phraseHistory.append(self.currentPhrase)
        self.problemTokenHistory.append([])  
        self.fairTokenHistory.append([])

    def pushPhrase(self, phrase:str, fairTokens:list, problemTokenPairs:list):
        self.totalLayers+=1
        self.phraseHistory.append(phrase)
        self.fairTokenHistory.append(fairTokens)
        self.problemTokenHistory.append(problemTokenPairs)
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
    temp="" 
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
    #unique =set()
    #for problem in problemHighTokens:
    #    unique.add(tuple(problem)) 
    #problemHighTokens=[]
    #for problem in unique:
    #    problemHighTokens.append(list(problem))
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
    testStatement2= "If x is an Integer, then either x is positive or negative, when x is not zero." 
    testStatement3= "If x is a Real Number, then x can be a Rational number, or an Irrational number."
    testStatement4="If x is a non-negative Integer, then x is either a Prime or a unique Sum of Primes."
    testStatement5="If x is Infinity, then x>0, x>1, x>2..."
    testStatement6="If x is Infinity, then x>0, x>1, x>2...." #Problem should be deteced at end.

 

    #Step 1, deminish the phrases.
    deminTS1 = deminishStatement(testStatement1)
    deminTS1 = deminishStatement(testStatement5)
    deminTS1 = deminishStatement(testStatement6)

    
    
    pass

if __name__=="__main__":
    main()