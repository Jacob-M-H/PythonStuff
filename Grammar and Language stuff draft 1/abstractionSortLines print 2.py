"""
    This is an abstraction of one of the sub algorithms in the Python Parser.
    When sorting a given rules' cases, we want to order each line by first Similar words, and then by length. Or by Length then similar words.
    This is a question that's got to be answered.
    We assume that each word in a case has been mapped to an integer, and that each case has been cleaned so that each symbol has purpose.

    Current Bug: Not sorted exactly how I want it to, it's good *enough* but in the future would like it to sort so that lower mapped items are first, longest items first, and such.    

    LATER: make a copy of this file, name it abstractionSortLinesSimplePrint
            Make it print in a similar fashion to how my paper kept track of items. 
            See if it was a mistake or unintenional shortcut I made on my side,
            if it's not, then we will see exactly where the notation differs from the hand version.
"""
import math

class ruleObj():
    def __init__(self, ruleName):
        self.name=ruleName
        self.cases=[]
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
        return self.name+":\n"+cases 
    
"""Note this algorithm only garuntees that the strings are sorted by how similar they are, and then by length. Not length then similarity.
        As such, if hte first case fails, then either it will compare to the same first case next, or a different first case [idx 0], if it's the same, a memoization will skip it.
            If it is a different first case, then the case may be longer than the prvious [old] first case match string.
            Example:

            I like some Candy
            I like Candy
            I like
            How's it going my dude?
            How's it going Man?

            Note the longest string is at index 3, however each case has similarity sorted.
            Note if you want the longest string to be apparent at the start, try sorting by length, and then passing the cases into this algorithm. I haven't tested it yet, but I don't think it'd be improbably it'd work.
            
            """
def sortRulesAbstraction(exampleRule:ruleObj):  
    #NOTE idx may come out as a parent function variable here, however at some point at least 1 of the sub functions would require a copy for multi thread saftey I believe.
    def intermitenStage(cases, idx):
        print(idx, ": ", str([str(findStatement(case, None))+"^"+str(case[idx]) for case in cases]))
        #remove from mapped cases any item that is less than the idx, and append to the end of the modMergeSort return.
        
        """Recipie - able to assume for Merge(s) functions that hte idx will never exceed each case.""" 
        if len(cases)<2:
            return cases
        
        result=modMergeSort(cases,idx) #+to short for idx
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
            if left[lidx][idx]<=right[ridx][idx]: #Integer map compare. Doesn't matter if it's <, >, or <=/>=, it's an arbitrary map. Simply needs consistency.
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

    def findStatement(case=None, idx=None):
        if case==None and idx==None or case!=None and idx!=None:
            raise TypeError("expect case==None xor idx==None")
          
        if idx==None: 
            for kv in statementMap: 
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


        print("SubSecs:\n ",
                [
                str([str(findStatement(case, None))+"^"+str(case[idx])+", " for case in subSection[0]])+" Short: "+
                    str([str(findStatement(case, None))+"^x, " for case in subSection[1]])
                for subSection in subSections]
            )
        
    
        continued=[]
        toShort=[]
        for subSection in subSections:
            print('SubSection to parse out ', subSection)
            if subSection[0]!=[]:
                continued.append(intermitenStage(subSection[0], idx+1)) #intermitten expects list of lists. On empty list return empty list. On list with one list, return that list
            if subSection[1]!=[]:
                toShort.append(subSection[1])
        for item in continued:
            sortedResult+=item
        for item in toShort:
            sortedResult+=item
        print("sorted Result", sortedResult)

        resultString=""
        for case in sortedResult: 
            if len(case)<idx+1:   
                resultString+=str(findStatement(case, None) )+"^"+str(case[idx])+", "
            else:
                resultString+=str(findStatement(case, None) )+"^x, "
        print("results : "+ resultString)


        return sortedResult


    statementMap=[]
    for idx in range(0, len(exampleRule.cases)):
        #statementMap[exampleRule.cases[idx]]=idx
        statementMap.append([idx, exampleRule.cases[idx]])
    print(statementMap)
    
    #FUTURE: inplace sortation would be disgusting. Some considerations on depth and memory. Multi threading, etc. need to be made.
    exampleRule._replaceCases(intermitenStage(exampleRule.cases, 0))

    pass
    

def testRuleObj(rule:ruleObj):
    print('old values')
    for case in rule.cases:
        print(case)
    sortRulesAbstraction(rule)
    print('new sorted cases')
    for case in rule.cases:
        print(case)    

def main(): 
    exampleRule=ruleObj('Example')
    exampleRule.addCase("1 2 3 4 5")
    exampleRule.addCase("2 2 3")
    exampleRule.addCase("1 3 2 4")
    exampleRule.addCase("3 2 3 4")
    exampleRule.addCase("1 2 3")
    exampleRule.addCase("1 2 3 3")
    exampleRule.addCase("1 3 4 2")
    exampleRule.addCase("1 3 2 2")
    exampleRule.addCase("1 3 2 2 5") 
    #print(exampleRule.cases)
    #testRuleObj(exampleRule)


    print("NEW attempt to replicate")
    exampleRule2=ruleObj('Example 2')
    exampleRule2.addCase('3')
    exampleRule2.addCase('1')
    exampleRule2.addCase('2') 
    #testRuleObj(exampleRule2)


    exampleRule=ruleObj('Example Set')
    exampleRule.addCase([22, 12, 25, 12, 22])
    exampleRule.addCase([24, 12, 22, 12, 25, 12, 22, 12, 26])
    exampleRule.addCase([27])
    print(exampleRule.cases)
    testRuleObj(exampleRule)
    
    exampleRule=ruleObj('Example Wildcards')
    exampleRule.addCase([48, 12, 49, 12, 50, 49, 12, 46, 12, 47])
    exampleRule.addCase([48, 12, 49, 12, 50, 49, 12, 50, 49, 12, 46, 12, 47])
    exampleRule.addCase([48, 12, 49, 51, 12, 47])
    exampleRule.addCase([48, 12, 47])
    #print(exampleRule.cases)
    #testRuleObj(exampleRule)
"""
SCRATCH
    I believe that it may be required to sort by length first, just so that it fits the form that the longest subform will be first. 
    It shouldn't matter as the first argument of each will be different, and thus it would still find the proper case.
    Perhaps it's also a consideration for optimization scripts [just to have an assumption to work off of].

"""


if __name__=="__main__":
    main()