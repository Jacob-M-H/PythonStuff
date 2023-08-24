import collections





#import LinkedList as LL
#I think a python list might actually be fine. 
    #Just again have explicit deletions, otherwise have it set to None if it's just remove.
    #This allows us to keep track of children orders succienctly. Linked list unnecessary. 

import LinkedList as LL

#Anonymous container for data for specific applications.
class GraphData:
    pass
class NodeData:
    pass
class EdgeData:
    pass


#Default naming convention, for fast lookup. Though hashing it's ID might be acceptable while running, what about when it's stored in a file? Note that when we remove nodes we should keep a 
    #running list of available smaller values, and keep it sorted, so we use the smallest values available. If MAX_INT is reached, throw error.


defaultNodeName=0#Global 


#Push left default for new facts


class Node:  
    data:NodeData
    nodeName=None
    nodeNum:int; edgeNum:int #Int
    maxEdge =None #Int, or None. Ensures a user can prevent abuse
    edgeList = LL.LinkedList() #No limit on edges. Enforced during tree maybe?

    def __init__(self):
        self.setName(None)
    def __init__(self, nodeName):
        self.setName(self, nodeName)
        self.setMaxEdge(None)
    def __init__(self, nodeName, maxEdge):
        self.setName(self, nodeName)
        self.setMaxEdge(maxEdge)

    def setMaxEdge(self, maxEdge): #QUESTION, extend deque, change maxlength?
        if (maxEdge==None):
            #copy edgelist to new temp list, remake the que with None, then readd
            pass
        elif (maxEdge<self.maxEdge):
            #decrease edgeList size
            pass
        else:
            #Increase edgelist size
            pass
        self.maxEdge=maxEdge 
    def setName(self, nodeName)->int:
        if (nodeName is int or nodeName is float or nodeName is str): #QUESTION: chr is a function?
            self.nodeName=nodeName
            return 0
        else:
            self.nodeName==defaultNodeName
            defaultNodeName += 1
            return -1
    def getName(self)->nodeName.__class__: #QUESTION: does this do anything?
        return self.nodeName
    def getMaxEdges(self) ->maxEdge.__class__:
        return self.maxEdge
    def changeMaxEdges(self, newEdgeMax) -> int:
        if (newEdgeMax==None):
            self.setMaxEdge(newEdgeMax)
        elif (newEdgeMax>len(self.edgeList)):
            self.setMaxEdge(newEdgeMax)
            return 0
        else: #Too many edges, need to choose to remove some.
            return -1

class Edge:
    data:EdgeData
    origin:Node
    destination:Node
    def __init__(self, origin:Node, destination:Node):
        self.setOrigin(origin)
        self.setDestination(destination)
    def setOrigin(self, origin:Node)->None:
        self.origin=origin
    def setDestination(self, destination:Node)->None:
        self.destination=destination
    def getOrigin(self):
        return self.origin
    def getDestination(self):
        return self.destination
    
    pass
 


#Nodes might want to have a hidden 'name' which describes it's place in the graph for faster lookup...

#Parse string required. 

class Graph: 
    #Graph class, two ways to store a graph, a adj matrix or a linked list.
        #QUESTION, does the forward declare type help? Or is it pointless.
    data :GraphData
    graphName:str #string
    nodeNum:int; edgeNum:int #Int
    maxNode = None; maxEdge =None #Int, or None. Ensures a user can prevent abuse
    nodeList : LL.LinkedList()
    edgeList : LL.LinkedList()
    nodeNameList : {} 

    #boolean to auto delete unconnected noes
    #boolean to enforce tree behavior
    #boolean for undirected edge vs directed edge

    #First add a node to the graph <-do not create a node, then try to add it to the graph with addEdge, ALWAYS use addNode.
        #Then able to add edges to that node, or find that node in the graph
    #However, it is fine to create an edge and add it, SO LONG as the node's are actually in the graph already.
    #NOTE, deque is used for the constant time operation to insert and remove elements from anywhere in the list. 

    #User
    def __init__(self, graphName:str = "",   maxNode: int = None,   maxEdge: int = None):
        self.setName(graphName)
        
        #assumption: we cannot have more Edges than maxNodes.
        if (maxNode is int): 
            #To many edges possible [not enough nodes, nonsensible]
            #not enough edges is considered fine
            maxN=maxNode; maxE=0
            while(maxN>1):
                maxE+=maxN-1
                maxN-=1
            if (maxE>maxEdge):
                print("Warning, too many edges possible to assign. Assigning a maxEdge of "+maxE)
                maxEdge=maxE 
        print("maxEdge "+maxEdge) 
        self.setMaxNode(maxNode)
        self.setMaxEdge(maxEdge)
        pass
    #DANGER
    def __init__(self, graphName:str = ""): #include a boolean to have default maximums
        self.setName(graphName)
        self.setMaxNode(None)
        self.setMaxEdge(None) 
        pass
    

    #constructor only
    def setName(self, name: str = "") -> None:
        self.graphName=name
    def setMaxNode(self, max: int) -> None: #max:int enforces integer typing, '-> None' means it returns nothing
        self.maxNode=max
        self.nodeList = LL.LinkedList(None, self.maxNode) 
    def setMaxEdge(self, max: int):
        self.maxEdge=max 
        self.edgeList = LL.LinkedList(None, self.maxEdge)
    #Helpers only
    def incrementNodeNum(self) -> None:
        self.nodeNum+=1
    def incrementEdgeNum(self) -> None:
        self.edgeNum+=1
    def decrementNodeNum(self) -> None:
        self.nodeNum-=1
    def decrementEdgeNum(self) -> None:
        self.edgeNum-=1

    #User
    def changeMaxNode(): #test if lower than current number, if no number was previously assigned, and create new deque container
        pass
    def changeMaxEdge(): #...
        pass


    def getNode(self, nodeName:not Node)->[int, Node]:
        #Assuming no clever storing of graph name. Go through the list
        for node in self.nodeList: 
            if (nodeName == node.getName()): #Node found
                return 0, node 
        return  -1, None
     
    def getNode(self, node:Node)->[int, Node]: #redundant
        for aNode in self.nodeList:
            if (node==aNode):
                return 0, aNode
        return -1, None
    


    def getEdge(self, nodeOrigName, nodeDestName)->[int, Edge]:
        for edge in self.edgeList:
            if (nodeOrigName==edge.getOrigin().getName() and nodeDestName==edge.getDestination().getName()):
                return 0, edge
            else:
                return -1, None 
        return -1, None #No edges


    def addNode(self, nodeName=None)->int:  
        #-1: exceeded max nodes
        #-2: nodeName in use
        if (max(self.nodeList)==len(self.nodeList)) :
            return -1
        elif (nodeName!= None and nodeName in self.nodeNameList):
            return -2
        else:
            self.nodeList.append(Node(nodeName))
            self.nodeNameList.append(self.nodeList.end().getName())
            self.incrementNodeNum()
            return 0
        pass
    def addNode(self, node:Node)->int:  
        #-1: exceeded max nodes
        #-2: nodeName in use
        if (max(self.nodeList)==len(self.nodeList)) :
            return -1
        else:
            #Check if Node already appears in nodeList names'
            if (node.getName() in self.nodeList.getName()):
                return -2
            else: 
                self.nodeList.append(node)
                self.nodeNameList.append(self.nodeList.end().getName())
                self.incrementNodeNum()

            return 0
         
    def addEdge(self, node1:Node, node2:Node)->int: #...
        #-1: eceeded maximum edge num
        #-2: missing origin
        #-3: missing destination
        #-4: missing origin and destination
        if (max(self.edgeList) ==len(self.edgeList)):
            return -1
        else:
            if node1 in self.nodeList and node2 in self.nodeList:
                self.edgeList.append(Edge(node1, node2))
                self.incrementEdgeNum()
                return 0
            else:
                if (node1 not in self.nodeList):
                    if (node2 not in self.nodeList):
                        return -4 #missing both dest and origin
                    return -2 #missing origin 
                return -3 #missing destination           
    #assumes nodeName's used QUESTION is this correct? 'not Node'
    def addEdge(self, node1:not Node, node2:not Node)->int: #...
        #-1: eceeded maximum edge num
        #-2: missing/incorrect origin
        #-3: missing/incorrect destination Name
        #-4: missing/incorrect origin Name and destination Name
        if (max(self.edgeList) ==len(self.edgeList)):
            return -1
        else:
            if node1 in self.nodeNameList and node2 in self.nodeNameList:
                node1 = self.getNode(node1)
                node2 = self.getNode(node2)
                self.edgeList.append(Edge(node1, node2))
                self.incrementEdgeNum()
                return 0
            else:
                if (node1 not in self.nodeNameList):
                    if (node2 not in self.nodeNameList):
                        return -4 #missing both dest and origin
                    return -2 #missing origin 
                return -3 #missing destination
                    
         


    def getGraph(self):
        pass
    def setGraph(self):
        pass
 


#Store graphs
class AdjGraph(Graph):
    #subclass of Graph, represent the Graph data as a AdjGraph Object
    pass
class LinkedGraph(Graph):
    #subclass of Graph, represent the graph data as a Linked List object.
    pass





#Graph hold array of all nodes, and edgse
#Node is created first. 
#If edge is made, new Edge(Node Origin, Node Dest), it's constructor should use setters
    #Node Origin.addEdge(this), [one way], Edge.addNodeOrigin[Origin], Edge.addNodeDest[Dest]
#If a node is made, Graph.addNode(Data),  if a Node is passed use addNode(Node) 

#I thought about another algorithm for finding a tree binary search, which is keeping a 'smaller' tree, for example, explore half it's length down, if greater go half up, half down, and so forth (fast termination) in a recursive like fashion,
    #I also thought maybe it'd be fast for finding duplicates by doing such a search, but I doubt it'd find it fast enough. When it is left at 1, then it only explores by 1, so a massive tree becomes a 'smaller' tree quickly.

#bool graph omni direcitonal or one way
#Bool graph max  branches/number of children per node
#Bool check for cycling [tree] no node can form a cycle [HARD NP Hard problem? If so, keep track of 'layer' the node is on.]
#[fast find tree idea test with large tree]

def main():
    #Python passes by 'assignment', so understanding scoping is clear.  
    TestGraph = Graph()


if __name__=="__main__":
    main()
