


def ParseStatement(statement:str, statementType:int):
    match statementType:
        case 0: #Default statement, unknown rigor
            pass
        case 1: #Theorem, proven entirely. Find similar wording
            pass
        case 2: #Hypothesis, assumed to be true.
            pass
        case 3: #Try, a user statement, unclear if it's helpful, fast removal required. Less prioritized.
            pass
        case 4: #Lemma, trivial from previous Theorem. [Theorem code/linking?]
            pass
        case 5: #???
            pass

    words=statement.split(" ") #we want to make a graph/tree now. 
    keyWords=["if",
              "iff","if and only if",  
              "or",
              "and",
              "then",
              "cases",   
              "equivalent", 
              "is",
              "only",
              "exists",
              "there",
              "For", "all", "every",
              "does",
              "not",
              "impossible", 
              ]
    labels=[] #Based on the objects we find. Example Integers would have a label 'positive' or 'negative', or unknown. This just helps pair labels with items in the tree/graph
    structures=[] #integers, matrices, etc.
    operators=[] #<,>,==, equiv, unicode symbols. ||, This also incldues functions.

        
def GuessStatement(statement:str):
    #lookup 'known' statements, and fidn similar graphs.
    pass