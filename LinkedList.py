
#Deque is not what we want. It seems input limited at one ends (not middle)
 #And output limited at both ends.
#We want an ordered list, that can have 'empty' space, a declared maximum [or no max],
    #removable in center, swappable. etc.
#A linked list is what seems to be desired.

class LinkedNode:
    def __init__(self, data=None):
        self.data=data
        self.next=None
    def setNextNode(self, node):
        self.next=node
    def getNextNode(self):
        return self.next
    def getData(self):
        return self.data
    def setData(self, data):
        self.data=data


#Forward linked, Left easy access, right hard access. Lookup looks at each item<-slow. Might be fine for purposes.

#Purposes: Fast insert 1 end is fine. [new facts]
#Slow removal is fine [graph shouldn't have to delete often]
#Slow lookup [fine, since children should have a list of facts, and thus would have to look at all anyways]
#-10 reserved for unimplemented functions. 

class LinkedList: 
    #Linked List is the parent container for LinkedNodes. It tracks the Max number of Nodes available. Does not shrink unless explictly desired.
    # Items in the list when 'removed' will still take up that space. a 'Shrink' is required to shrink the list in it's entirely.
    # A 'Grow' is required for expansion if the size was declared.
    # -should implement a 'end' ptr for the container
    # -should implement a representation of 'has data' for faster lookup.
    #     
    head:LinkedNode
    ptr:LinkedNode
    MaxItems:None or int
 
    def __init__(self,data=None, max=None): 
        self.MaxItems=max
        if (max is int):
            nextSpot=None 
            if (max>0):
                self.head=LinkedNode(data)
                max-=1
                nextSpot=self.head
            else:
                raise ValueError
            
            while (max>0):
                nextSpot.setNextNode(LinkedNode())
                nextSpot=nextSpot.getNextNode()
                max-=1
            #If max!=Int, then infinite items possible.
            #If max is int, then 'None' represents an empty Node. 

        else:
            self.head=LinkedNode(data) 

        self.ptr=self.head
    
    def __iter__(self):#Special, dunder, or magic methods. dir(list) shows methods... okay 
        return self
    def __next__(self):
        if self.ptr==None: #check if there are more values
            self.ptr=self.head
            raise StopIteration
        else:
            current = self.ptr
            self.ptr=self.ptr.getNextNode()
            return current
           
        
    def __sizeof__(self) -> int:
        pass
    def getHead(self):
        return self.head
    
    def my_range(self, start, end):
        #genreator function? 
        
        if (end<start):
            pass
        
        
        else:
            current=self.head
            end=end-start #how far after the proper 'start' place
            if start<0 or end<0: #Either start is bad, or the places after end is bad
                #NOTE: If end<start, maybe just flip the two, and return a reversed array? idk. A recursive yield?
                return ValueError
            

            while(start>0): #Get to the proper 'start' place 
                current=next(current)
                start-=1


            while current!=None and end!=0: #while there are values ot grab, and end is not reached.
                yield current
                current=current.getNextNode()
                end-=1

    def __getitem__(self, place:int)->LinkedNode:
        #Data not predictable, So space taken is unclear. [can't grow by byte count]
        #End not tracked, as  getPreviousNode is not tracked. Thus negative values are not valid.
        if place<0:
            raise IndexError #Does non reversable list
        else:
            current=self.getHead()
            while (place!=0):
                current=current.getNextNode()
                place-=1
                if current==None:
                    raise IndexError #Exceeded max 

            return current

    def deleteSlot(self, idx:int) -> int:
        
        #-3 exceeded max number of items allowed in the list. fail fast.
        if (self.MaxItems!=None and idx>self.MaxItems-1):
            return -3
        
        prev=None
        current=self.head
        while (idx>0 and current!=None):
            idx-=1
            prev=current
            current=current.getNextNode()
        if (idx!=0):
            return -2
        if (current==None):
            return -1
        prev.setNextNode(current.getNextNode())
        return 0

    def removeItem(self, idx:int) -> int: #NOTE: PopLeft, PopRight!
        #-1 for already no data
        # 0 deleted data
        #-2 exceeded current number of elements in linked list.
        #-3 exceeded max number of items allowed in the list. fail fast.
        current=self.head
        if (self.MaxItems!=None and idx>self.MaxItems-1):
            return -3
        while (idx>0 and current!=None):
            idx-=1
            current=current.getNextNode()
        if (current==None):
            return -2
        elif (idx!=0):
            return -1
        else:
            current.setData(None)
            return 0


    def insertItem(self, node:not LinkedNode, idx)->int:
        self.insertItem(LinkedNode(), idx)
    def insertItem(self, node:LinkedNode, idx)->int:
        #-1 for already no data
        # 0 inserted data
        #-2 exceeded current number of elements in linked list.
        #-3 exceeded max number of items allowed in the list. fail fast.
        if (self.MaxItems!=None and idx>self.MaxItems-1):
            return -3
        current=self.head
        prev=None
        while(idx!=0 and current!=None):
            idx-=1
            prev=current
            current=current.getNextNode()
        if (current==None):
            return -2
        elif (idx!=0):
            return -1
        else:
            if prev==None:
                #Seperate function call, 'pushLeft'       
                self.pushLeft(node) 
                pass
            else: 
                prev.setNextNode(node)
                node.setNextNode(current)
                
        return 0
    
    def push()->int:#append R end
        return -10
    def pop(): #remove R end
        return -10
        pass 
    def swapItems()->int:
        return -10
        pass
    def shrinkList()->int:
        return -10
        pass
    
    def pushLeft(self, node:LinkedNode)->int:
        #append to start
        if (len(self) < self.MaxItems):
            node.setNextNode(self.head)
            self.head=node
            return 0 
        else:
            return -1 #exceeded max number of elements, did not append
        
    def pushLeft(self, data:not LinkedNode)->int:
        #append to start 
        return self.pushLeft(LinkedNode(data))   

    
    
    def popLeft(self): #deletes item
        #remove start
        oldHead=self.head
        self.head=self.head.getNextNode()
        return oldHead
    
     


def main():
     
    
    pass
















if __name__=="__main__":
    main()
