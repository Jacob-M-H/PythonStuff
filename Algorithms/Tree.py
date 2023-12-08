
import sys
MAX_INT=sys.maxint
DEBUG=True


class rules():
    #Switch statements, a Tree has 1 rule object, which contains the logic for placing and comparing nodes/navigating the tree.
    pass


class Node():
    #data <-a subclass/object, that can be passed in.
    #Rule <-function, controls how children are arranged. 
    #   Requires a flag to prevent 'juggling' 
    #children array/vector
    def __init__(self, childMin, childMax, data=None ):
        self.setData(data) 
        self.children=[None]*childMin #Make into linked list, fast append and remove. 
        self.currentChildren=0
        self.childrenMax=childMax
        pass 
    def setData(self, data):
        self.data=data 
        pass
    def addChild(self, child):
        if (self.currentChildren==self.childrenMax):
            raise ValueError("Attempt to append child failed. Max integer reached!")
        else:
            self.children.append(child)
            self.currentChildren+=1
        pass
    def findChild(self, idx):
        #should raise the child most appropriate based on all the children, if a child is removed, or if a child is being sought raise that specific child.
        pass 





class Tree:
    rootNode:None
    childMin:int
    childMax:int
    numberNodes:int
    rule:rules()

    def __init__(self, rootNode, childMin, childMax) -> None:
        self.rootNode=rootNode
        self.childMin=childMin
        self.childMax=childMax
        numberNodes=1
        pass

    def __new__(cls,rootNode=Node(), childMin=0, childMax=MAX_INT): 
        print("Creating instance") 
        if (DEBUG):
            if (type(rootNode)!="Node"):
                raise TypeError("Expected Node container as rootNode.")
            if (childMin<0):
                raise ValueError("Node cannot have negative children.")
            if (childMax>MAX_INT):
                raise ValueError("Max children exceeds system max integer.")
            if (childMax<childMin):
                raise ValueError("Max children cannot be less than min children.")
        else:
            if (type(rootNode)!="Node" or childMin<0 or childMax>MAX_INT or childMax<childMin):
                print('silent fail')
                return None
        return super(Tree, cls).__new__(cls) 
    #__repr__
    #__add__ [insert one tree into another. requiring the descendant node roots to be gathered and placed appropriately.]
    
    def insertRule(rule, node):
        #Not sure how to do this. Append functions to a class? To a switch statement? Perhap make a matrix and subtree?
        #https://stackoverflow.com/questions/26881396/how-to-add-a-function-call-to-a-list#:~:text=At%20the%20simplest%20level%2C%20you,those%20tuples%20in%20a%20list.&text=That%20is%20%3A%20call%20the%20function,in%20the%20remaining%20of%20typle.
        #Append the rule in a tuple? Then the rule just has to go through the entire tuple?
        #https://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object-instance-in-python <-read this later.

        pass

    def insertNode(): #Insert node, search for viable spot [importantly no movement inplace]
        pass
    def sortTree(): #Sort the tree, this may require more thought [movement in place if node supplied?]
        pass
    def frizzTree(): #Different frizing algorithms should be tried with different rule sets. Attempts to create different levels of the tree, such as an avg depth, or a set of 'strands'
        pass

def main():
    plant=Tree()

    pass

if __name__=="__main__":
    main()


