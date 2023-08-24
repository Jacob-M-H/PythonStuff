#pytest TestFiles/LinkedList_test.py
    #flags : -v: Test names and output output.
    #-s input and output shown [prints]
    #Entry or autotree. Test directory in pyupgrade, so pyupgrade/_tests/ ?
    #Match module name_ test/helpers
    #__init__.py not needed, but best practice. Namespace packages are newer tahn thought. Two test files would colide if not made.


import sys
 
 
    #ONE OF THESE TWO MUST ALWAYS BE USED, to grab from a parent directory.
#import os
#current=os.path.dirname(os.path.realpath(__file__))
#parent=os.path.dirname(current)
#sys.path.append(parent)

sys.path.append("../Python Stuff") 

for path in sys.path:
    print(path)

import LinkedList as LL


#Run LinkedList_test.py
#Tests are meant to be simple and easy to follow. Thus a good example should be sufficient.
#-v hides a few inputs. 
#Also -s shows inputs and such.
#Tests can be function based or class based. 
#Question, if the py file leads with a underscore, does it hide it from the ls by default? Or what? 
    #ls folder/_plugins/^C? Not sure what ^ would do. 

#IDEA: linkedlist has container node List which is a linked list [itself] of length N, when length exceeded, add a new node.
    #Or geometric expansion.
    #Then we CAN have shrink list, or expand list based on a number or user call. 
    #Swaps would be fast, and the linked list could still fetch from a node next node, but also able to edit. 


def helper(tester:LL.LinkedList):
    list =[]
    for node in tester:
        list.append(node.data) 
    return list 

#__iter__, __next__
def test_iterable(): 
    tester=LL.LinkedList("A")  
    tester.getHead().setNextNode(LL.LinkedNode("b")) 
    tester.getHead().getNextNode().setNextNode(LL.LinkedNode("c"))  
    assert helper(tester)==["A", "b", "c"]

#__getItem__
def test_subscriptable(): 
    tester=LL.LinkedList("A")  
    tester.getHead().setNextNode(LL.LinkedNode("b")) 
    tester.getHead().getNextNode().setNextNode(LL.LinkedNode("c"))  

    assert tester[0].getData()=="A" 
    assert tester[1].getData()=="b" 
    assert tester[2].getData()=="c" 
    try:
        assert tester[3]==IndexError 
    except IndexError:
        print("\nExpected IndexError handled")
        pass
    try:
        assert tester[-1]==IndexError 
    except IndexError:
        print("\nExpected IndexError handled")
        pass
