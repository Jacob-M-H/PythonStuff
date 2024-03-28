import os
import functools
import filecmp
import token
import math

def getContents(FilePath):
    print("open "+FilePath)
    f=open(FilePath, "r")
    contents=f.read()
    f.close()
    return contents


#Roster notation
    #A = {4,2,3,1}
#Infinite sets in roster notation
    #{1,2,3, ..., 1000}
    #{...-2,-1,0,1,2,...}
#Semantic definition
    #Let A be the set whose members are the ____ 
#Set builder notation
    #F={n | n is an integer, and 0<= n <=19}
    #| is 'such that'

#intensional definition uses a rule to define membership. Semantic and set builders are examples
#extensional describes et by listing all elements. Enumerative.
#an ostensive defintion is one that describes sets by giving examples of elements; a roster involving an ellipsis would be an example.


SymbolsToParse=[]

class Parser(): 
    #get file,
    #seperate comments,
    #Break by line, and figure out how the lines should be *actually* organized,
    #Balance set symbols, 
    #check validity of entries, 
        #suggest what line the issue occurs, or what is going wrong.
    #unrecognized characters,   
    #wrap up nicely, send to CleanUp
    def __init__(self):
        print('parser initialized')
        pass
    def parse(self, strContents): #Logic for parsing the file
        print(strContents)
        print('skip')
        pass
    pass


class CleanUp():
    #Rewrite the definitions to use specific symbols for union, intersect, setdif, caresian , and symmetric difference  (Carteisan product is going to be troublesome!)
    #reorder items, according to set order as much as possible, this is to decrease set generation when possible. (such as a not in {} being applied to a union of two finite sized sets. Simply apply the not in to either set if it's sensible.)
    #Rewrite symbols to go left to right in pairs of two between any given set operator 
    #Currying required. Though Postfix notation or prefix notation might be interesting.
    #Record a tree of possible rewrites in the event Derive Meaning is wrong, or requires evaluation or training.

    pass


class DeriveMeaning():
    #Evaluate whether the resulting set will be infinte, or finite. If finite, how large would it take to store the set as a string array? 
    #Ask for a max size or file to write, and write up to that amount if it will contain the whole set, Otherwise note if its finite or ifnite.
    #Create a function to give the set object that will allow it to determine if the item is in the set or not. If finite simple sort the set by some rule (SQL uses collations, so we should make a default unicode collation)
        #If infinite, attempt to figure out prefixes, suffixes, inclusions, max length, min lengths, or the step between possible lengths. 
            #This will likely result in a tree of possible 'good' decisions for checking depending on the elements in the set, or the subsets in the set.
                #Or a graph? Tree would be clearer but may have many duplicate nodes.
    pass


class ResultantInstructions():
    #Store the tree of good decisions from DeriveMeaning
    #Evaluate examples, return constructed Set() object, and an option to measure performance, along with a pretty print of the good decisions and some marker determining the path of the tree travelled.
     
    pass



#FUTURE: Debug and edits use arrays for cases, OTHERWISE use tuples, as it will make certain algorithms faster to run.
class ruleObj():
    def __init__(self, ruleName):
        self.name=ruleName
        self.cases=[]
        self._isSorted=self.setSorted(False)
    def getRuleName(self):
        return self.name
    def addCase(self, matchCase:list|str): 
        if type(matchCase)!=type([]): #enforce case must be a list 
            if type(matchCase)!=type(''): 
                return -1 
            self.cases.append([item for item in matchCase.split(" ")]) #3/13 should result in a list of symbols
            return 0
 
        if matchCase==[]: #enforce matchCase cannot be empty list
            return -1
         
        for case in self.cases:
            if case==matchCase:
                return 0
        self.cases.append(matchCase)

        return 0

        #3/13 TODO: clever way of resorting the one case - a less generalized version of sortRules?
        #3/13 TODO: add case to a specific rule?
    
    def setSorted(self, value:bool):
        self._isSorted=value
    def getSorted(self):
        return self._isSorted
    def insertCase(self, case):
        pass
    def replaceCase(self, case):
        pass
    def _replaceCases(self, cases):
        self.cases=cases
    
    def getCases(self):
        return self.cases
    def getCase(self, idx:int):
        if idx>len(self.getCases())-1:
            raise IndexError("Index Exceeds Number of Cases")
        if idx<0:
            raise IndexError("Index must be above -1")
        return self.getCases()[idx]
    def __str__(self):
        #3/13 Could memoize the join maybe... Better not unless we make a wrapper function for it
        cases="".join(["\t"+" ".join(case)+"\n" for case in self.cases])
        return self.name+":\n"+cases 


class cleanRules():
     
    def __init__(self):
        self._debug=False
        self._warnings=False 
        self.rules=self.getRules() #obj : {name, cases=[someString]} <-should turn it to a map, though each obj remains the same. Faster lookup for rulename:cases 
        self.alphabet=self.getAlphabet()
        self._debug=True
        pass


    #NOTE: Alphabet construction may have to give higher priority to regular expressions such as ()+ or (t|T) to sort accurately [for example, a rule may result in a different construciton with (a)+ Othersymbol, than just (a) Othersymbol]
    """Go through each ruleObj, add each word to an alphabet of symbols."""
    def getAlphabet(self):
        """
        Assumption: ditionary has unique key and unique values. This helps with sorting the rules.
            Eventually this needs to be a subobject to enforce design requirements/constraints.
                This also helps quickly prefix items [eventually]. It'd be nice if the rule objects to this langauge could use integers that map back to this unique list of symbols. Ideally this would lead to more condensed large langauges.
                    However a benefit of having the keys be strings is that comparing two languages by symbol sets is faster. However the symbols matter less than the atomics, similar rule strucutres [with the symbols not mapping per say], and a faster way of navigating those algorithms.
        """

        if not self.rules:
            return {}
        
        alphabet={}
        length=0
        def tryAlphaInsert(symbol,value):
            try:
                alphabet[symbol]
                if self._debug:
                    print("alphabet has key ", symbol, ' value: ', alphabet[symbol])
                return value
            except:
                if self._debug:
                    print('alphabet did not have key ', symbol, ' value: ', value)
                if type(symbol)==type('') and symbol!='':
                    alphabet[symbol]=value
                    return value+1

        for rule in self.rules: 
            length=tryAlphaInsert(rule.getRuleName(), length)
            for case in rule.cases:
                for symbol in case:
                    length=tryAlphaInsert(symbol, length)
        

        if self._debug:
            print("ALPHABET ")
            for item in alphabet:
                print(item, ": ", alphabet[item]) #prints key value pairs


        return alphabet
        
    #3/13 TODO: Add rule function?
    """Parse a file to collect rule Names, Rule case(s) return a list of ruleObj."""
    def getRules(self)->list|int:
        curDirectory= "\\".join(os.path.realpath(__file__).split("\\")[0:-1])+"\\"

        print('cur directory: ',curDirectory)
        #Set symbols always will be sibling file
        PathToTests=curDirectory
        PathToSymbols=curDirectory
        GrammarFile="Set Grammar.txt"
        GrammarPath=PathToSymbols+GrammarFile
        rules=[]


         
        if (os.path.exists(PathToSymbols)): 
            if (os.path.exists(GrammarPath)):
                Grammar=getContents(GrammarPath)
                GrammarLines=[line.strip("\t").strip(" ") for line in Grammar.split("\n")]
                
                if self._debug:
                    print('grammar lines:')
                    print(GrammarLines)

                for lineIdx in range(len(GrammarLines)):
                    line=GrammarLines[lineIdx]  
                    if line!="":  
                        if line[-1]==":":
                            rules.append(ruleObj(line[0:-1]))
                        elif line[0]=="|": 
                            rules[-1].addCase(line[2:]) #Assumes that there is a '| ' to start the line.
                        else: #Assumed to be a single rule 
                            rules[-1].addCase(line) #this is in the case like string:\n\tchar + (char)+

            else: 
                raise FileNotFoundError("Missing file " + GrammarPath)
        else:
            raise FileNotFoundError("Missing Directory "+PathToSymbols)
        
        if self._debug:
            for rule in rules:
                print(rule)

        #Symbol should now just have the symbols with no excessive white space, per symbol.
        #Note that white space IN a symbol means it's expecting some argument's between the known characters.
        #Note that {} simply implies it is a set, and should it be omitted the SymbolSet should be used.
        #SymbolSet describes the encoding. For now assumed to be ASCII, but UTF8MB4 is a contender. 
        #we may find value in breaking up the file case detection from meta data detection. The metadata may be wrapped into a seperate file, such as where atomics are defined. This allows us to detect if two atomics are the same [in file applicaiton]
        return rules

    
    """Sort each ruleObj cases by the mapping in the language alphabet, and by the case length. Thus earlier words in alphabet and longest cases are placed forwards in the list, shorter and later symbols in the alphabet are placed later. """
    def sortRule(self, rule:ruleObj): 
        #it will compare with self.Alphabet and the length of each string. 
        #Algorithm is recursive, and not in place. This may change in the future to in place, though for error handling, multi threading, and other considerations it may stay with this algorithm.
        if (not rule.cases):
            return -1; #insert a error warning or debug, [rule may be atomic!]
        if (not rule.name):
            return -2; #rule has no name!
        if (rule.name not in self.alphabet.keys()):
            return -3; #rule not found in language alphabet. Improper insertion or nonexistant rule in language. Consider merging ruleObj or debug.
 
        if self._debug:
            print('sort rule')
            print(rule.name)
            print(rule.cases)
            print(self.alphabet[rule.name])

        def getAlphabetValue(word):
            try:
                return self.alphabet[word]
            except:
                issueString:str
                try:
                    issueString="Symbol '"+str(word)+"' is not found in this languages' alphabet. This is either a parsing error, or some rule insertion was not properly accounted for."
                except:
                    issueString="A Symbol is not found within this languages' alphabet. This is either a parsing error, or some rule insertion was not properly accounted for."
                raise KeyError(issueString)
       
       #NOTE idx may come out as a parent function variable here, however at some point at least 1 of the sub functions would require a copy for multi thread saftey I believe.
        def intermitenStage(cases, idx):
            if self._debug:
                print(idx, ": ", str([str(findStatement(case, None))+"^"+str(getAlphabetValue(case[idx])) for case in cases]))
            #remove from mapped cases any item that is less than the idx, and append to the end of the modMergeSort return.
            
            """Recipie - able to assume for Merge(s) functions that hte idx will never exceed each case.""" 
            if len(cases)<2:
                return cases
            
            result=modMergeSort(cases,idx) #+to short for idx
            
            if self._debug:
                print(idx, ": ", str([str(findStatement(case, None))+"^"+str(case[idx]) for case in result]))
            
            
            """Take out in order the -1 lengths for next idx in this function, so that by findSubsets, as findSubsets will recombine in order the desired combinations baseed on return of intermiten stage."""
            #NOTE: note in the journal that what held me up besides will power was the idea of 3 steps instead of 4, but knowing there needed to be an intermitten step to do a few actions.
                #This was a good experiment in algorithm construction.
            return findSubsets(result,idx)
        
        def modMergeSort(cases,idx):
            """Merge sort, Favors left, i.e. it will prefer putting more items on the left half when given the choice"""
            
            maxLen=len(cases)
            if maxLen>1: 
                preferLeft=math.ceil(maxLen/2)
                left = cases[0:preferLeft] #non inclusive
                right = cases[preferLeft:] 
                return modMerge(modMergeSort(left, idx), modMergeSort(right, idx), idx) 
            else: 
                return cases

        def modMerge(left, right, idx): 
            """Logic for the merge"""
            lidx=0
            ridx=0
            midx=0
            leftLen=len(left)
            rightLen=len(right)
            merge=[None]*(leftLen+rightLen)

            while ridx<rightLen and lidx<leftLen:
                if getAlphabetValue(left[lidx][idx])<=getAlphabetValue(right[ridx][idx]): #Integer map compare. Doesn't matter if it's <, >, or <=/>=, it's an arbitrary map. Simply needs consistency.
                    merge[midx]=left[lidx]
                    lidx+=1
                else:
                    merge[midx]=right[ridx]
                    ridx+=1
                midx+=1
            
            while lidx<leftLen:
                merge[midx]=left[lidx]
                midx+=1
                lidx+=1 
            while ridx<rightLen:
                merge[midx]=right[ridx]
                midx+=1
                ridx+=1
            return merge

        """Used for debug strings"""
        def findStatement(case=None, idx=None):
            if case==None and idx==None or case!=None and idx!=None:
                raise TypeError("expect case==None xor idx==None")
            
            if idx==None:
                for kv in statementMap:
                    #print('comapre ',case,' to ', kv[1])
                    if kv[1]==case:
                        return kv[0]
                raise ValueError("no key value in which value is ", case)
            elif case==None:
                for kv in statementMap:
                    if kv[0]==idx:
                        return case
                raise ValueError("no key value in which key is ", idx)

        def findSubsets(semiSortedCases,idx):
            """Find each subset [in order by now], send that subset into intermitten stage with idx moved. Then re merge each subset"""
            #assume sorted at idx-1, find subset 'chunks', then inplace insert those at -1 length.
            
            if len(semiSortedCases)==0:
                return []
            currentValue=None
            subSections=[]
            expectedMinLen=idx+1
            for item in semiSortedCases:
                if currentValue!=item[idx]:  
                    subSections.append([[],[]])
                    currentValue=item[idx]
                if len(item)>expectedMinLen:
                    subSections[len(subSections)-1][0].append(item)
                else:
                    subSections[len(subSections)-1][1].append(item)

            sortedResult=[]


            if self._debug: 
                print("SubSecs:\n ",
                        [
                        str([str(findStatement(case, None))+"^"+str(getAlphabetValue(case[idx]))+", " for case in subSection[0]])+" Short: "+
                            str([str(findStatement(case, None))+"^x, " for case in subSection[1]])
                        for subSection in subSections]
                    )
            print('intermitten')
            #FUTURE: improvment. In a C++ version, free that subSection after passing the value, though in C++ we would likely be using references and pointers rather than Pythons pass by value.
            continueToSort=[]
            toShort=[]
            for subSection in subSections: 
                if subSection[0]!=[]:
                    continueToSort.extend(intermitenStage(subSection[0], idx+1)) #intermitten expects list of lists. On empty list return empty list. On list with one list, return that list
                if subSection[1]!=[]:
                    toShort.extend(subSection[1])
            sortedResult.extend(continueToSort)
            sortedResult.extend(toShort)

            if self._debug:
                print('result string construction')
                print("sorted result:", 
                    [str(findStatement(case, None))+"^"+str(getAlphabetValue(case[idx]))+", " for case in continueToSort]+
                    [str(findStatement(case, None))+"^x, " for case in toShort], "\n english: ", sortedResult
                )
                print('lengths: ', [len(case) for case in sortedResult])
 

            return sortedResult

        #FUTURE: to reduce size of memory used, we could make a simple numbering that references the index of the case in the RuleObj. Thus sorting a temporary list, and only referncing the actual rule object.
        if self._debug: 
            statementMap=[]
            for idx in range(0, len(rule.getCases())):
                #statementMap[exampleRule.cases[idx]]=idx
                statementMap.append([idx, rule.getCase(idx)])
            print('statement map: ', statementMap)
            
        #FUTURE: inplace sortation would be disgusting. Some considerations on depth and memory. Multi threading, etc. need to be made.
        rule._replaceCases(intermitenStage(rule.cases, 0))
        rule.setSorted(True)
        return 1 #success

    """Sort each rule in tandum."""
    def sortRules(self): 
        if self._debug:
            for key in self.alphabet:
                print(key," : ", self.alphabet[key])

        for rule in self.rules:
            rule:ruleObj
            if not rule.getSorted():
                isOk=self.sortRule(rule)
                if not isOk:
                    return isOk 
        return 0



def makeAbstract(ruleIdx, language):
    rule=language.rules[ruleIdx]
    resultString='exampleRule=ruleObj(\'Example\')'+'\n'
    for case in rule.getCases():
        newArr=[language.alphabet[symbol] for symbol in case] 
        resultString+="exampleRule.addCase("+str(newArr)+")\n"
    resultString+='print(exampleRule.cases)\ntestRuleObj(exampleRule)'
    return resultString

def main():
    tester=cleanRules()
    #tester.sortRules()
    
    for ruleNum in range(0, len(tester.rules)):
        tester.sortRule(tester.rules[ruleNum])
        x=input('okay? [no to get information]')
        if x=='no':
            print('ruleNum:',ruleNum,", ruleName: ",tester.rules[ruleNum].getRuleName(),", try to figure out what went wrong with this rule.")
            x=input('continue? [no to stop]')
            if x=='no':
                break


    #Unit tests? 
        
    #Issue in rule num 6, set.
    #issue in 10


    #abstract test construction 
    print(makeAbstract(6, tester))
    print(makeAbstract(10, tester))
 

if __name__=="__main__":
    main()