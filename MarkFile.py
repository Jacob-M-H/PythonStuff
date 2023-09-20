





WordCount =dict() #Keep track of all words.


#try:
#    notesPath=""
#    categoryPath=""
#    markupPath=""
#    notesFile =open(notesPath, "r") #https://docs.python.org/3/library/functions.html#open
#    cateogryFile=open(categoryPath, "+") 
#    markupFile=open(markupPath, "+")
#except:
#    pass



categoryDict = dict()
class hashableList(): 
    def __init__(self, length):    
        self.labels = [None]*length #Create dummy array
    def replace(self, position, value):
        self.labels[position]=value
    def __str__(self) -> str:
        if len(self.labels)>1:
            words = " ".join(self.labels)
        elif len(self.labels==1):
            words=self.labels[0]
        else:
            words=""
        return words
    def getLabels(self):
        return self.labels

#Takes a line of previously categorized information, places Obj as key, properties/subObj/subCategories as array in hashableList
def parseCategory(line:str):
    words = line.split(" ") #CategoryName : [Property1, Property2] 
    place=0
    piece=""  
    while (words[place]!=":"):
        piece+=words[place]+" "
        place+=1
    piece=piece[0:len(piece)-1]
    print("words: ", words)
    print("piece: "+piece) 
    print("leftover:", words[place:]) 
    place+=1   
    words=" ".join(words[place:]) 
    print("Next Break " + words)  
    place=0
    words=words.split(", ")
    labels = hashableList(len(words))
    print("Pieces of Break = ", words)
    #Categories under this category (I.e. 'Number : Integer, Real, Prime, Imaginary, Rational)
        #Assuming for now all categories are labels, and all labels are possible categories.
        #If there is no 'lead' later, then it is considered a label/property, otherwise it is considered a category property. 
    
    if len(words)==0:
        pass
    elif len(words)==1:
        labels.replace(place, words[place][1:len(words[place])-2]) #[
        #labels[place]=  words[place][1:len(words[place])-2]
    else:
        labels.replace(place, words[place][1:])
        #labels[place]=words[place][1:] #[
        place+=1
        while (place < len(words) and not words[place].endswith("]")):
            labels.replace(place, words[place])
            #labels[place]=words[place] 
            place+=1
        labels.replace(place, words[place][:len(words[place])-1]) #] 
        #labels[place]=words[place][:len(words[place])-2] #] 

    categoryDict.update({piece : labels}) 
    print(piece+" :", categoryDict[piece])

 
def markUpNote( ):
    tempFile=["If x is an Integer and x > 0, then x is positive", "If x is an Integer and x<0, then x is negative"]

    cmds=["ADD CATEGORY","ADD PROPERTY", #CMD(idx)<-insert a new category in dict, CMD(prop idx, cat CATEGORY.idx)<-finds cateogry in dictionary, adds prop in its labels.
                                        #Insert CATEGORY() or PROPERTY() around surroudning terms. 
          "REMOVE CATEGORY","REMOVE PROPERTY", 
                                    #Remove Cat/Prop : 1 - from dictionary key/category propertys
                                    #                   2 - from line idx's
                                    #                   3 - from line char matching.
          "UNDO", "REDO",           #Undo last comand, redo last command <-logic required
          "NEXTLINE", "PREVLINE",   #fetching: Read next line (save previous markups), read prev line (save previous markups)
          "SHOWCATEGORIES", "SHOWLINE", #list categories and their properties, 
                                        #Show the line, 0-no edits, 1-with specified categories/labels, 2- with all categories/labels. 
          "AUTO" #Try to fit found strings to categores/labels based on a grammer of sorts.
          ]



    pass

def cleanLine(line:str) ->str:
    line.replace(". "," . ")
    line.replace(", "," , ") 
    line=line.lower()
    return line

def wordCount(arr):
    #Array of strings
    for line in arr:
        assert(type(line)==str)  
        line=cleanLine(line)
        words=line.split(" ")
        for word in words:
            if word in WordCount.keys():
                WordCount[word]+=1
            else:
                WordCount.update({word : 1})

def printWordCount(i:int):
    if i==0: 
        print(wordCount.items())
    elif i==1:
        print(sorted(WordCount.items(), key=lambda x:x[1])) #Sort wordCount by it's count, items will print both the key and value.
    else:
        pass



#Note a definite symbol is a symbol that must exist, regardless of it's value
anyNumWordSymbol="///" #This is not a definite symbol, 0 or more
anyWordSymbol="_" #This is a definite symbol, 1 value must be there
class Phrase:
    def __init__(self, phraseLine:str):
        self.skipSymbol=anyNumWordSymbol
        self.anyWordSymbol=anyWordSymbol
        self.phraseLine=phraseLine
        self.phraseArr=phraseLine.split(" ") #Verify that the phrase is 'valid', so no ... next to ..., 
        self.length=self.findLength()
        self.trueLength=len(self.phraseArr)

    #Helper for init
    def findLength(self):
        L=0
        for word in self.phraseArr:
            if word!=self.skipSymbol:
                L+=1
        return L
    
    #Main functionality 
    def comparePhrase(self, compLine:list, L:int): #compare this phrase to a line. Note that this line is considered to NOT be a phrase. Thus placeholders are interpreted differently.
            #that is, ..., or whatever the 'ANY NUM WORD' symbol ends up being, is only in the PhraseLine, whereas ... in the compLine would be an ellipse, a regualr word.
        if (L>=self.trueLength): #At least as many as there are definites
            skip=False
            place=0; compPlace=0
            #look until we find the phrase, or not. If the phrase is found, we should report it is/contains the phrase.
            while(place<self.length):
                if self.phraseArr[place]==self.anyWordSymbol:
                    place+=1; compPlace+=1; skip=False
                elif self.phraseArr[place]==self.skipSymbol:
                    place+=1; skip=True
                elif self.phraseArr[place]==compPlace[place]:
                    place+=1; compPlace+=1; skip=False
                elif skip==True: #skip Symbol in place, 
                    compPlace+=1
                else:
                    return False
            return True #Phrase is in the compLine. 
        else: #Not enough definite symbols
            return False





Phrases=[] #_ means any string can be found in that position
def comparePhraseToKnownPhrase(wordPhrase:str):
    #Note if ..._Word, then ... means 'any length before' and ... after is 'any length after',
        #This would be a 'case' system of checking, find first possible word that fits the phrase (not ounting ...), and find anything that matches,
        #Then, not that the 'phrase' itself is only of the length allowed, like _Word... and ..._Word are length 2, so would NEVER be in anything under or greater
        #However _..._ would ALWAYS let the phrase appear in phrase length 2 or greater. 
        #Whereas _..._..._ would ALWAYS let the phrase appear in phrase length 3 or greater.
        #So if ... appears in the phrase, we must allow it to go pass the len === based on how many 'solid' length we have.
            #And it's equivalence must be relaxed to allow the any number inbetween. Thus these phrases are intrinsically more expensive.
    wordPhrase=wordPhrase.split(" ")
    PossiblePhrases=[]
    for phrase in Phrases: #Check against every phrase
        phrase.split(" ")
        if len(phrase)==len(wordPhrase):
            for temp in range(len(phrase)):
                if phrase[temp]=="_": #ANY
                    continue
                elif phrase[temp]!=wordPhrase[temp]: #FAIL
                    break 

            PossiblePhrases.append(" ".join(phrase)) #Report possible phrases
    if len(PossiblePhrases)>1:
        print("WARNING, more than one possible phrases:", PossiblePhrases) #show the confusion <- example '_ all' and 'for _' for the phrase 'for all'. Thus the more 'solid' a prhase is the more it should be favored, otherwise a user should be asked, or context clues looked at. 
    elif len(PossiblePhrases)==1:
        return PossiblePhrases[0] #Definite phrase found
    else: #No phrase found
        return " ".join(wordPhrase)

def wordCountExpanded(arr, phraseLength=1):
    for line in arr:
        line=cleanLine(line)
        words=line.split(" ")
        for idx in range(len(words)):
            try:
                wordPhrase=" ".join(words[idx:idx+phraseLength])
            except:
                break #Get next line basically,  
            wordPhrase=comparePhraseToKnownPhrase(wordPhrase)
            
            if type(wordPhrase) == list:
                for phrase in wordPhrase: #Count up to length to increase the relevancy, as those phrases are still valid, however do NOT record the original wordphrase, as seeing each valid phrase should start to fill each other in.
                    if phrase in WordCount.keys():
                        WordCount[phrase]+=1
                    else:
                        WordCount.update({phrase : 1})

            elif type(wordPhrase)==str:
                if wordPhrase in WordCount.keys():
                    WordCount[wordPhrase]+=1
                else:
                    WordCount.update({wordPhrase : 1})
            else:
                print("wordCountExpanded is confused")
                break



#A different way to compare must be done with the skip symbol in play... :/ 
    #Take line, go through all possible length of statements for a pharse (default 1, assert >=1)
        #Then with that line, compare it to all phrases known <-fail fast and compare fast if possible
    #If multiple phrases are found, report each in an array <-may inflate phrases found in center of a phrase... Hm :/. NOTE THIS REQUIRES THOUGHT
def compareStatementToKnownPhrases(words:list, idx:int, phraseLength:int, numWords:int): #Hard default in func? 
    Phrases:list(Phrase)
    temp=[]
    for phraseObj in Phrases:
        if phraseObj.comparePhrase(words, numWords):
            temp.append(phraseObj)
    return temp #any and all phrases that matched

#Now integrate knownPhrases
def wordCountExpandedAnySymbol(arr, phraseLength=1):
    for line in arr:
        line=cleanLine(line)
        words=line.split(" ")
        numWords=len(words)
        for idx in range(numWords):
                #CHANGE HERE TMW, also introduce a 'or' set/'chr_' any symbol leading with chr, and ending with 1 symbol, or 'chr..._' start with chr, ends iwth at least 1 symbol
                #These symbols are now encapsulated in the Phrase class, which should take a super that has those special symbols defined for ease of replacement.
                #Note a problem emerged mathematically, phrases trend to over count towards the middle of a phrase. It is unclear how we should account for this.
                    #AFter phrases figured out, we want to record the idx's where prhases happen, so that we get a 'pyramid' of likelyhood locations.
            try:
                wordPhrase=" ".join(words[idx:idx+phraseLength])
            except:
                break #Get next line basically,  
            wordPhrase=comparePhraseToKnownPhrase(wordPhrase)
            
            if type(wordPhrase) == list:
                for phrase in wordPhrase: #Count up to length to increase the relevancy, as those phrases are still valid, however do NOT record the original wordphrase, as seeing each valid phrase should start to fill each other in.
                    if phrase in WordCount.keys():
                        WordCount[phrase]+=1
                    else:
                        WordCount.update({phrase : 1})

            elif type(wordPhrase)==str:
                if wordPhrase in WordCount.keys():
                    WordCount[wordPhrase]+=1
                else:
                    WordCount.update({wordPhrase : 1})
            else:
                print("wordCountExpanded is confused")
                break
 




def main():
    #Parses saved category relationships.
    parseCategory("Matrix : [n x m, determinate, traingular]") 
    markUpNote()

    
    notesPath="Math Records/Linear Algebra TESTFILE.txt"
    
    WordCount.clear()
    notesFile =open(notesPath, "r") #https://docs.python.org/3/library/functions.html#open
    wordCount(notesFile.readlines())
    notesFile.close()
    printWordCount(1)
    print("\nTotal Phrases: ", sum(WordCount.values()))
    

    print("\n\n\n\n\n\n next function 2 \n\n\n\n\n\n")    
    #No phrases
    WordCount.clear()
    notesFile =open(notesPath, "r") #https://docs.python.org/3/library/functions.html#open  
    wordCountExpanded(notesFile.readlines())
    notesFile.close()
    printWordCount(1)
    print("\nTotal Phrases: ", sum(WordCount.values()))
    

    
    print("\n\n\n\n\n\n next function 3 \n\n\n\n\n\n")    
    #Phrase (every word is now a phrase)
    Phrases.append("_")
    WordCount.clear()
    notesFile =open(notesPath, "r") #https://docs.python.org/3/library/functions.html#open  
    wordCountExpanded(notesFile.readlines())
    notesFile.close()
    printWordCount(1)
    print("\nTotal Phrases: ", sum(WordCount.values()))
    


if __name__=="__main__":
    main()