#coding=utf-8
from Match import *
class Tuple:
    def __init__(self,*args):
        for i,v in zip(range(1,len(args)+1),args):
            setattr(self,'_t'+str(i),v)
    def get(self):
        return [getattr(self,i) for i in dir(self) if i.startswith('_t') ]
    def __eq__(self,v):
        get = lambda t : [getattr(t,i) for i in dir(t) if i.startswith('_t') ]
        return all (map(lambda a : a[0]==a[1],
                      zip(get(self),get(v))))
    def __repr__(self):
        return "( "+ ', '.join(map(repr,self.get())) + " )"
def Case(v,*action):
    get = lambda t : [getattr(t,i) for i in dir(t) if i.startswith('_t') ]
    for f in action:
        try:
            return apply(f,get(v))
        except Exception as e:
            continue
    else:
        raise Exception("Case Error")
triple = Tuple(1,2,3)
print Case(triple,
           lambda a,b,c,d : Tuple(b,a,c),
           lambda a,b,_ : Tuple(a,b),
       )
"""
print( triple )
@matcher(Tuple,False)
def fst(self):
    return self.t1
@matcher(Tuple,False)
def snd(self):
    return self.t2
print( fst (triple) )
print( snd (triple) )
@matcher(Tuple,False)
def swap(self):
    self.t1,self.t2 = self.t2,self.t1
    return self
print( swap ( triple ) )
"""
