#coding=utf-8
def Concat(lst):
    return reduce (lambda a,b: a + b,lst,[])
def pbind(p,f):
    def cbind(lst):
        return Concat( map(f,p(lst)) )
    return cbind
l = [1,2,3]
print pbind(lambda x:x,lambda a: [ a+1 ] )(l)
def bind(self,f):
    return Concat(map (f,self))
# (>>=) :: m a -> (a -> m b) -> m b
List = type("List",(list,),{"__ge__":bind})
t = List(l)
print t >= (lambda x : [ x+1 ] )
print [i + 1 for i in t]
class Maybe:
    pass
class Nothing(Maybe):
    def __repr__(self):
        return "Nothing"
    def __ge__(self,f):
        return self
class Just(Maybe):
    def __init__(self,v):
        self.v = v
    def __repr__(self):
        return "Just {}".format(repr(self.v))
    def __ge__(self,f):
        return Just(f(self.v))
"""
Maybe Monad
"""
