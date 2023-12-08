from decimal import Decimal #avoids float errors, keeps trailing zeros. Way better than floats for my purposes


#NOTE FUTURE: 1,42,54, etc should be placed as 1., 42., 54., but 100 should not round to 100., I should assume in the future that if the digit is entered with a nonzero placeholder at the end of the string that it implies exact measurements, and thus a decimal should be included.
 
class SigFigCHECKER():
    def __init__(self, val:str):
        self.originalValue=str(val)
        self.sigString=""
        self.sigValue=None
        self.exp=None
        self.setSig(val)

    def setSig(self, val:str):
        #brute force
        head=0
        decimalPlace=None
        while(head<len(val) and val[head]!="."):
            head+=1

        if head==len(val): #NO DECIMAL PLACE ORIGINALLY
            front=val
            head=0
            #no decimal place
            while head<len(front) and front[head]=="0":
                head+=1
            if head==len(front):
                self.sigValue=0
                self.exp=0
                self.sigString=f"{self.sigValue} * 10^{self.exp}"
                return
            else: #Exists a non zero value in front
                front=front[head:]
                #Count backwards until first non sig shows
                headf=-1
                while front[headf]=="0":
                    headf-=1
                front=front[:len(front)+headf+1]
                if len(front)>1: #multiple sigs left in front
                    self.sigValue=float(front[0]+"."+front[1:])
                    self.exp=len(front)-1
                    self.sigString=f"{self.sigValue} * 10^{self.exp}"
                    return
                else: #single value left in front
                    self.sigValue=int(front)
                    self.exp=0
                    self.sigString=f"{self.sigValue} * 10^{self.exp}"
                    return
                



        else: #DECIMAL PLACE FOUND
            decimalPlace=head
            front=val[:decimalPlace]
            back=val[decimalPlace+1:] 
            headf=0
            headb=0

            #remove leading 0's
            while (headf<len(front) and front[headf]=="0"):
                headf+=1
             

            if len(front)==headf:
                #figure out back
                while headb<len(back) and back[headb]=="0":
                    headb+=1
                if len(back)==headb:
                    self.sigValue=0.0
                    self.exp=0
                    self.sigString=f"{self.sigValue} * 10^{self.exp}"
                    return
                else:
                    self.sigValue=float(back[headb]+"."+back[headb+1:])
                    self.exp=headb+1
                    self.sigString=f"{self.sigValue} * 10^{self.exp}"
                    return
            else: 
                self.sigValue=float(front[0]+"."+front[1:]+back)
                self.exp=(len(front)-1)
                self.sigString=f"{self.sigValue} * 10^{self.exp}"
                return



    
        #ASSUMPTIONS, 
            #10. vs 10,
                #10. means that 1.0 *10^1, 
                #10 means 1*10^1 [assumes not known]
 


    def __repr__(self):
        return "CHECK: "+self.sigString+" exp:"+str(self.exp)+", sigValue:"+str(self.sigValue)
    
class SigFig():
    #IMPORTANT: Keep https://stackoverflow.com/questions/15238120/keep-trailing-zeroes-in-python
        #https://copyprogramming.com/howto/python-how-to-keep-trailing-zeros-in-python#keep-trailing-zeroes-in-python
    def __init__(self, val:str):
        self.originalValue=str(val)
        self.sigString=""
        self.sigValue=None
        self.exp=None
        self.sigFront=""
        self.sigBack=""
        self.setSig(val)

    def setSig(self, val:str):
        

        headf=0 
        while(headf<len(val) and val[headf]=="0"):
            headf+=1
        if headf<len(val):
            val=str(val[headf:]) #new string should prevent some oddities with slicing
            #next look for decimal point 
            headf=0
            while(headf<len(val) and val[headf]!="."):
                headf+=1

            if headf<len(val):
                #decimal found
                front=val[:headf]
                back=val[headf+1:]
                #back is always significant, 
                if len(front)>0:
                    print(front[0]+"."+front[1:]+back) 
                    self.sigValue=Decimal(front[0]+"."+front[1:]+back )
                    self.exp=len(front)-1
                    self.sigString=f"{self.sigValue} * 10^{self.exp}"
                    self.sigFront=front[0]
                    self.sigBack=front[1:]+back
                    return 
                else: 
                    headb=0
                    while headb<len(back) and back[headb]=="0":
                        headb+=1
                    print(f"headb {headb}")
                    if headb<len(back):
                        self.sigValue=Decimal(back[headb]+"."+back[headb+1:])
                        self.exp=-headb-1
                        self.sigString=f"{self.sigValue} * 10^{self.exp}" 
                        self.sigFront=back[headb]
                        self.sigBack=back[headb+1:]
                        return
                    else:
                        self.sigValue=Decimal("0"+"."+back)
                        self.exp=0
                        self.sigString=f"{self.sigValue} * 10^{self.exp}"
                        self.sigFront="0"
                        self.sigBack=back
                        return 
            else: 
                #Decimal not found, 14 ->1.4, 1->1.
#NOTE FUTURE if front[-1]!=0, imply a decimal place.
                if len(val)>1:
                    self.sigValue=Decimal(val[0]+"."+val[1:])          
                    self.exp=len(val)-1
                    self.sigFront=val[0]
                    self.sigBack=val[1:]      
                elif len(val)==1:
                    self.sigValue=int(val)
                    self.exp=0
                    self.sigFront=val
                    self.sigBack=""      
                else: 
                    print("default values, empty input. Values chosen with least precision")
                    self.sigValue=int(0)
                    self.exp=0
                    self.sigFront="0"
                    self.sigBack=""      
                 
                self.sigString=f"{self.sigValue} * 10^{self.exp}" 
                return
            

        else: #Decimal not found, all 0's.

            self.sigValue=int(0)
            self.exp=0
            self.sigString=f"{self.sigValue} * 10^{self.exp}" 
            self.sigFront="0"
            self.sigBack=""      
            
            #set as 0, no decimal         
            return 
    
    
    
    
        #ASSUMPTIONS, 
            #10. vs 10,
                #10. means that 1.0 *10^1, 
                #10 means 1*10^1 [assumes not known]
 
    def getSigLength(self):
        return len(self.sigFront)+len(self.sigBack)


    def __repr__(self):
        return "CHECK: "+self.sigString+" exp:"+str(self.exp)+", sigValue:"+str(self.sigValue) +", front: "+str(self.sigFront)+", back: "+str(self.sigBack)
        



def main():
    #expect 0
    tester=SigFig("0") #base case
    print(tester)
    tester=SigFig("00") #1 leading 0s
    print(tester)
    #expect 0

    #expect 0.0
    tester=SigFig("0.0") #1 leading 0, decimal, 0 [so 1 sig of 0.]
    print(tester) 
    tester=SigFig("00.0") #1 leading 0, decimal 0 
    print(tester)
    #expect 0.0
    tester=SigFig("0.00") #decimal 00 
    print(tester)
    tester=SigFig("00.00") #1 leading 0, decimal 00 
    print(tester)

    #now to test values
    # expect 1 
    tester=SigFig("1")  
    print("oi", tester) 
    #expect 1.0 or 1.
    tester=SigFig("1.") 
    print(tester) 
    #expect 1.1
    tester=SigFig("1.1")  
    print(tester) 
    #expect 1.1
    tester=SigFig("01.1")  
    print(tester) 
    #expect 1.10 <-fails!
    tester=SigFig("1.10")  
    print(tester) 
    #expect 1.10
    tester=SigFig("01.10")  
    print(tester) 
    tester=SigFig("001.100")  
    print(tester) 
    tester=SigFig("101.1000009")  
    print(tester) 
    #Expect 1.0 * 10^-2
    tester=SigFig(".010")  
    print(tester) 
    tester=SigFig(".0010")  
    print(tester) 
    tester=SigFig(".00")  
    print(tester) 

    



    pass


if __name__=="__main__":
    main()

   
