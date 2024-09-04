
class Move:
    
    def __init__(self,initial,final):
        #initial and final square
        self.initial = initial
        self.final = final
        
    def __str__(self):
        s = []
        s.append(((self.initial,self.final)))
        return s
    
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final