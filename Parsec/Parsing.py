#coding=utf-8
def mreturn(v):
    def curry_return(inp):
        return [(v,inp)]
    return curry_return
def zero(inp):
    return []
def uncurry(f):
    return lambda uncurry_a,uncurry_b : f (uncurry_a)(uncurry_b)
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
            print func.__code__.co_varnames
            print "now:",now
            temp.append( func(*now) )
        except Exception,e:
            print e,type(e),e.args
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
    return alt(
        bind(p)(lambda x:
        bind(many(p))(lambda xs: mreturn ([x]+xs) )))(
            mreturn([]))
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
def literal(x):
    return sat(lambda y: y==x)
def mString (lst):
    # lst : char list  => list ("xxx")
    if lst == []:
        return mreturn ([])
    else:
        x,xs = lst[0],lst[1:]
        return bind (literal(x)) (lambda _ : bind (mString(xs)) (lambda _:mreturn ([x]+xs) ) )
lower = sat (lambda x : 'a' <= x and x <= 'z')
upper = sat (lambda x : 'A' <= x and x <= 'Z')
digit = sat (lambda x : '0' <= x and x <= '9')
letter  = alt(lower)(upper)
alphanum = alt(letter)(digit)
ident = bind(lower)(lambda x : bind (many(alphanum)) (lambda xs : mreturn ([x]+xs)))
def sepby1(p):
    def _sepby1(sep):
        temp = many (bind(sep)(lambda _ : bind (p) (lambda y : mreturn (y) )))
        return bind(p)(lambda x : bind(temp)(lambda xs:mreturn([x]+xs)))
    return _sepby1
def sepby(p):
    def _sepby(sep):
        return alt (sepby1(p)(sep)) (mreturn([]))
    return _sepby
def bracket(op):
    def __bracket(p):
        def _bracket(cl):
            return bind(op)(lambda _ : bind(p)(lambda x:bind(cl)(lambda _ : mreturn(x))))
        return _bracket
    return __bracket
def chainl1(p):
    def __chainl1(op):
        rest = lambda x : alt(bind(op)(lambda f : \
                            bind(p)(lambda y : \
                            rest (f(x,y))))) (mreturn(x))
        return bind(p)(rest)
    return __chainl1
def chainr1(p):
    def __chainr1(op):
        return bind(p)(lambda x: \
                       alt(bind(op)(lambda f : \
             bind( chainr1(p)(op) )(lambda y :  \
                mreturn ( f(x,y) ))))(mreturn(x)))
    return __chainr1
def foldr1(func,lst):
    x,xs = lst[0],lst[1:]
    return reduce(func,xs,x)
def ops (xs):
    def __t(t):
        p,op = t
        return bind (p)(lambda _ : mreturn(op))
    return foldr1 (uncurry(alt),map(__t,xs))
def chainl( p ):
    def __chainl(op):
        def _chainl(v):
            return alt( chainl1(p)(op) ) (mreturn (v) )
        return _chainl
    return __chainl
def chainr( p ):
    def __chainr(op):
        def _chainr(v):
            return alt( chainr1(p)(op) ) (mreturn (v) )
        return _chainr
    return __chainr

def nat(inp):
    Op = lambda m,n : 10  *  m + n
    temp = bind(digit)(lambda x : mreturn ( ord(x) - ord('0') ) )
    return chainl1( temp )( mreturn(Op) )(inp)

isA = sat (lambda x:x=='a') 
isB = sat (lambda x:x=='b') 
print bind(isA)(lambda v:mreturn(v))(list('abc'))
print sepby1(isA)(sat(lambda x:x==' '))(list("a a a"))
print sepby(isA)(sat(lambda x : x==','))(list('a,a,a'))
"""
a   = list("aaab")
print seq(isA)(isB)(['a','b','c'])
print many(isA)(a)
print many1(isA)(a)
print mString(list("abc"))(list("abc"))
print ident(list("abc1"))
print sepby1(isA)(sat(lambda x:x==' '))(list("a a a"))
print sepby(isA)(sat(lambda x : x==','))(list('a,a,a'))
op = sat(lambda x: x == '(')
lp = sat(lambda x: x == ')')
print bracket(op)(ident)(lp)(list('(expression1)'))
addop = sat(lambda x: x == '+')
subop = sat(lambda x: x == '-')
tempops = ops( [(addop,lambda a,b:a+b),(subop,lambda a,b:a-b)] )
print tempops(list('+'))
Int = bind(digit)(lambda x : mreturn(int(x)))
print chainl1(Int)(tempops)(list('1+2+3-1'))
print chainr1(Int)(tempops)(list('1+2+3-1'))
print nat(list("123"))
"""
