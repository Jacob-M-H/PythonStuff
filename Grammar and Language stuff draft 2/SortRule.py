

class ruleObj():
    def __init__(self, ruleName):
        self.name=ruleName
        self.cases=[]
        self.rank=(None,None,None)


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
        return self.name+":\n"+"Rank: "+self.rank+"\nCases:\n"+cases 
   
ruleCollection={}
"""We want to ensure that the grammar rules are sorted from most abstract to least abstract. [or reversed if the object creation and datastructures prefer]"""
""" 
Problem definition:
1.Sort rule Objs by 'depth', from most abstract to least
    1.a Depth in this case means the maximum number of rules required to reach a completely atomic/literal definition of that rule.
2.'Most Abstract' means # atoms, termianls & worst/longest case for rules used. Longest case includes the max length of the same of each rule in a case.
3. Want to avoid cyclic lookups. Exp: Rule A: Rule B, Rule B: Rule A. This requires two additional structures or values to keep track of evaluation and seen flags.
    3.a In the event of cyclic [not necessarily bad depending on implementation desires], either report the traceback of ruleName->case->rule->case->RuleName. Either bold or italics or other indicator of the closed loop.
    3.b In the event cyclic definitions are fine, 1 meta data must have a config defining max depth of such a case... 
    3.c Or 2, a case must must exist which does not result in cylic behavior. [as it is implied that an infinite input is not allowed or can be worked around]
    3.d In either case, if additional cases do not resolve and end up in cyclic behavior, report all offending cases. Note that each case for a rule must be evaluated [either way for checking cyclic or min max depth], and if evaluated and finished, great it's a fetch, else it'll either end and resolve the rule, or discover a cylicsm.
4. Every rule must end in terminals or atoms/consist at a macro level (if extended via only terminals and atoms, is it possible?) This is a warning.
    4.a If enforced, declare offending rule, [cyclic, case may exist which terminates, simply it means the rank is not determinate, except for a 'better case', and it's depth may still be definable simply by the max between the two of each of the cases that do terminate. Implies siblings]. 
    4.b If unenforced, [cyclic, and case does not exist which ends cycle].
5. Raise errors where cyclism occurs [and note extremit] along with trace of ruleName->case with rule outlined-> rule -> case with ruleName defined-> ... until cycle is completed at least once. Does not guantee every case is caught within the specific error. Multiple runs may be required to discover each incident.
6. Algorithm is not garunteed sorted cases [This may change, as sorting cases when not in EBNF and without REGEX expressions to muddle the waters should be posible. Additionally sorted cases by length may not result in longest match as current sort algorithm only takes by number of tokens, not number of termianls/atoms]
7. Algorithm may assume Atoms and terminals can be determined [rule names with cases that are only termianls, and the ruleName 'Atom' or some variant there of.]
    
"""

def main(): 
    pass



if __name__=="__main__":
    main()
