#coding=utf-8
"""
datatype 'a Nat = Zero | Succ of 'a
Nat = Zero | Succ('a')
"""
def init0(self,*v):
    self.index = map(lambda x:"v"+str(x),range(len(v)))
    for i,n in zip(self.index,v):
        setattr(self,i,n)
def repr0(self):
    tmp = [getattr(self,name) for name in self.index]
    if tmp:
        return "{} {}".format(self.__name__,tmp)
    return "{}".format(self.__name__)
def init1(self): 
    return 
class DT(object):
    def __init__(self):
        self.lines = [ ]
    def __repr__(self):
        return str(self.lines)
    def __getattr__(self,name):
        if name not in self.lines and not name.startswith('__'):
            self.__setattr__(name,self.mktype(name))
            self.lines += [name]
        return object.__getattribute__(self,name)
class Constructor(DT):
    def mktype(self,name):
        def curry_mktype(*typevar):
            setattr(self,name,
                    lambda f:
                    type(name,(f,),
                         {"__name__":name,
                          "__init__":init0,
                          "__repr__":repr0}))
            return self
        return curry_mktype
    def __or__(self,line):
        return self
    def __call__(self,f):
        for name in self.lines:
            tmp = getattr(self,name)(f)
            setattr(self,name,tmp)
        return self
    def __eq__(self,f):
        return self(f)
class Datatype(DT):
    def mktype(self,name):
        def curry_mktype(typevar=None):
            setattr(self,name,
                    type(name,(object,),
                         {"__name__":name,
                          "__init__":init0,
                          "__repr__":repr0}))
            return getattr(self,name)
        return curry_mktype

cs = Constructor()
dt  =  Datatype()
dt.Nat('a') == cs.Zero()    \
             |  cs.Succ('a')
zero = cs.Zero()
Succ = cs.Succ
print( zero )
print( Succ(zero) )
print( type(zero),type(Succ(zero)) )
print( type(Succ) )
print( isinstance(zero,dt.Nat) )
print( isinstance(Succ(zero),dt.Nat) )
print( dt.Nat )
from Match import *
@matcher(cs.Zero,False)
def toInt(self):
    return 0
@matcher(cs.Succ,False)
def toInt(self):
    return 1 + self.v0.toInt()
print( Succ(zero).toInt() )
print( dir(dt.Nat) )
dt.List('a') == cs.Empty() \
    | cs.Cons('a','b') 
print cs.Cons(1,cs.Empty())
@matcher(cs.Empty,False)
def mlen(self):
    return 0
@matcher(cs.Cons,False)
def mlen(self):
    return 1 + self.v1.mlen()
print mlen( cs.Cons(1,cs.Cons(2,cs.Empty())) )
