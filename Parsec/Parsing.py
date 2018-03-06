#coding=utf-8
def mreturn(v):
    def curry_return(inp):
        return [(v,inp)]
    return curry_return
def zero(inp):
    return []
def uncurry(f):
    return lambda a,b : f (a)(b)
def concat(lst):
    temp = []
    for i in lst:
        temp.extend(i)
    return temp
def fmap(func,lst):
    temp = []
    while lst!=[]:
        now = lst[0]
        #print now
        try:
            temp.append( func(*now) )
        except Exception,e:
            print e
        finally:
            lst = lst[1:]
    else:
        return temp

def bind(p):
    def bind_(f):
        def bind__(inp):
            temp = p (inp)
            #print "bind:",temp
            return concat ( fmap (uncurry(f),temp))
        return bind__
    return bind_
def mappend(lst1,lst2):
    if lst1 == [] :
        return lst2
    return [lst1[0]] + mappend(lst1[1:],lst2)

def alt(p):
    def alt_(q):
        def calt(inp):
            temp1 = p(inp)
            temp2 = q(inp)
            return mappend(temp1,temp2)
        return calt
    return alt_

def seq(p):
    def seq_(q):
        return bind(p)(lambda v: bind(q)(lambda w: mreturn((v,w)) ))
    return seq_
def many(p):
    return alt(bind(p)(lambda x:bind(many(p))(lambda xs: mreturn ([x]+xs) )))(mreturn([]))
def many1(p):
    return bind(p)(lambda x:bind(many(p))(lambda xs: mreturn ([x]+xs) ))
def sat(p):
    def csat(inp):
        if inp == []:
            return zero([])
        else:
            x = inp[0]
            xs = inp[1:]
            if p(x):
                return mreturn (x)(xs)
            else:
                return zero (xs)
    return csat

isA = sat (lambda x:x=='a') 
isB = sat (lambda x:x=='b') 
a   = list("aaab")
print seq(isA)(isB)(['a','b','c'])
print many(isA)(a)
print many1(isA)(a)
