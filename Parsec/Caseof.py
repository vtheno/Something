#coding=utf-8
class m(object):
    def __init__(self,pattern,v):
        self.pattern = pattern
        self.v = v
class MatchPattern(object):
    def __rshift__(self,v):
        return m(self,v)
class MatchEq(MatchPattern):
    def __init__(self,value):
        self.value = value
    def match(self,value):
        return value == self.value
eq = MatchEq
class MatchType(MatchPattern):
    def __init__(self,typ):
        self.type = typ
    def match(self,value):
        return isinstance(value,self.type)
typ = MatchType
class MatchPred(MatchPattern):
    def __init__(self,pred):
        self.pred = pred
    def match(self,value):
        return self.pred(value)
pred = MatchPred
class MatchOtherwise(MatchPattern):
    def __init__(self):
        pass
    def match(self,value):
        return True
otherwise = MatchOtherwise()
class b2v(MatchPattern):
    def __init__(self,name):
        self.name = name
    def match(self,value):
        setattr(self,self.name,value)
        return True
class plist(MatchPattern):
    def __init__(self,head_name,tail_name=None):
        self.head_name = head_name
        self.tail_name = tail_name
    def match(self,value):
        if not isinstance(value,list):
            return False
        setattr(self,self.head_name,value[0])
        if self.tail_name != None : 
            setattr(self,self.tail_name,value[1:])
        return True
class ptuple(MatchPattern):
    def __init__(self,*names):
        self.names = names
    def match(self,value):
        if not isinstance(value,tuple):
            return False
        nlen = len(self.names) 
        vlen = len(value)
        assert nlen <= vlen ,"variable too more"
        i = 0
        while i < nlen:
            setattr(self,self.names[i],value[i])
            i+=1
        else:
            if i > nlen:
                setattr(self,self.names[-1],value[i-1:])
        return True
#print match(typ(int),5)
#print match(pred(lambda x:x>0),-1)
class caseof(object):
    def __init__(self,value):
        self.value = value
        self.lines = list([])
    def __or__(self,line):
        self.lines += [line]
        return self
    def __invert__(self):
        for i in self.lines:
            #print i.pattern,i.v
            if i.pattern.match(self.value):
                return i.v
        self.lines = [ ]
        raise Exception("UnMatch")
def delay(value):
    if callable(value):
        yield value()
    else:
        yield value
def force(promise):
    r = promise
    t = type(delay('x'))
    try:
        while isinstance(r,t):
            r = next(r)
    except StopIteration :
        pass
    finally:
        return r
#x = plist('x','xs')
#print force( ~ (caseof([1,2,3]) | x >> delay(lambda :x.x) ))
t = ptuple('a','b','c')
print force(~(caseof(233) | (lambda v : v >> delay(lambda:v.a))(b2v('a')) ) )
print force(~(caseof((1,2,3)) | t >> delay(lambda :(t.c,t.b,t.a)) ) )
def msum(lst,acc):
    p = plist('x','xs')
    return ~(caseof(lst) \
             | pred(lambda x:x==[]) >> delay(acc) \
             | p >> delay(lambda : msum(p.xs,p.x+acc)) )
print force(msum([1,2,3,4],0)) 
def foldl(func,acc,lst):
    p = plist('x','xs')
    return ~(caseof(lst) \
             | pred(lambda x:x==[]) >> delay(lambda : acc ) \
             | p >> delay(lambda : foldl(func,func(acc,p.x),p.xs) ) )
print force(foldl(lambda a,b:(a,b),[],[1,2,3,4]))
"""
t = caseof(5) 
print t | eq(5) >> delay("eq 5") \
    | eq(6) >> delay("eq 6") \
    | eq(7) >> delay("eq 7")
print t.lines
print ~t
"""
def fact(n):
    return ~( caseof(n)               \
             | pred(lambda n:n==0) >> delay(1)\
             | pred(lambda n:n > 0) >> delay(lambda: n *  force(fact(n-1)))
          )
def tail_fact(n,acc):
    return ~( caseof(n) \
              | pred(lambda n:n==0) >> delay(acc) \
              | otherwise >> delay(lambda :tail_fact(n-1,n  *  acc))
              )
#print force(fact(500))
#print force(tail_fact(10000,1))
def isEmpty(lst):
    return lst == []
def tl(lst):
    return lst[1:]
def hd(lst):
    return lst[0]
def length(lst,acc):
    return ~(caseof(lst) \
             | pred(isEmpty) >> delay(acc) \
             | otherwise >> delay ( lambda : length(tl(lst),acc+1)))
def mlen(lst):
    return force(length(lst,0))
"""
def length(lst,acc):
    if lst==[]: return delay(acc)
    return delay(lambda : length(lst[1:],1+acc))
"""
#print mlen(range(10000))
