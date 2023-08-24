




seenWords={}

def recordStatementString(statement:str, number:int):
    
    statement=statement.lower() #fine only as I'm recording statements to count how often certain words are used, and in what contexts.
    #train data basically
    statement=statement.split()


def ParseProblem():
    pass
def ParseStatements():
    pass


def Parser(file):
    comment:str #Holds comments for each line,   
    for line in file.readlines():
        #Array of just words.
        Parse=line
        Parse=Parse.split(" ") #Split by words
        Parse=list(filter(lambda a: a!='', Parse)) #Handle Tabs
        Parse=[item.strip("\n") for item in Parse] #Remove new lines
        

        print( Parse, len(Parse) )
        if (Parse[0]=='\n'):
            continue
        elif ("#" == Parse[0][0]): #Section break 
            Parse=[item.strip("#") for item in Parse]  
            print("Found section"+''.join(Parse))
            if (Parse==""):
                pass


            pass #Send to approrpiate parseer
        else: #Details
            #Still might have comments. Find the comment, substring it

            pass 




def main():
    train=open("statementTrain.txt","r")
    Parser(train)
    train.close()

    #File -statement [seperator '/\/\/\'] [wordPlace Num], [word], [context];  (Useful for 1 word stuff)
        #Word 'could' be larger than 1 word, so long as it's relatively together in a range [like +- 5], this range mustb e consistent for each word however, and it's pariing.
 
    pass



if __name__=="__main__":
    main()