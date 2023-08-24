from typing_extensions import SupportsIndex


#Left class for now. Inserting is expensive in a list, but in a LinkedList it can be cheap, besides just exploring to the linked list. But it's only expensive when it has to resize.
    #The doubtlist would only 'remove' the place in a list when explicitly called for. Otherwise it simply places a 'None' in it's place.
    #Still, some langauges grow the list everytime an appending exceeds allocated space, but usually it's clever in a geo series or something like the double rule. 

class DoubtNode(list):
    pass

class Doubt:
    pass

class DoubtList(list):
    maxValue =None #int or None. 
    itemCollection=[]

    def __init__(self, maxValue):
        if (maxValue is int):
            self.maxValue=maxValue       
        else:
            self.maxValue=None
 
    pass

