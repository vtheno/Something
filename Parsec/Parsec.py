#coding=utf-8
from Match import *
"""
datatype 'a List = Nil
                 | Cons of 'a * 'a list
"""
List = type("List",(),{})
Nil = type("Nil",(List,),{"__repr__":lambda self:"[]"})
nil = Nil()

@Tail
def Helper(lst,acc=[]):
    if lst.null():
        return acc
    return Helper(lst.tl,[repr(lst.hd)]+acc )
def helper(lst):
    return reversed(force(Helper(lst,[])))

class Cons(List):
    def __init__(self,hd,tl):
        self.hd = hd
        assert isinstance(tl,List)
        self.tl = tl
    def __repr__(self):
        if isinstance(self.tl,Nil):
            return "[ {} ]".format(repr(self.hd))
        temp = ','.join ( helper(self) )
        #return "[ {} ,{} ]".format(repr(self.hd),self.tl)
        return "[" + temp + "]"
@matcher(Nil,False)
def __eq__(self,a):
    if isinstance(a,Nil):
        return True
@matcher(Cons,False)
def __eq__(self,a):
    if isinstance(a,Cons):
        if a.hd == self.hd:
            return self.tl == a.tl
    return False

@matcher(Cons)
def tail_foldl(self,f,acc):
    return self.tl.tail_foldl(f,f(acc,self.hd))
@matcher(Nil)
def tail_foldl(self,f,acc):
    return acc
def foldl(f,acc,LIST):
    return force(LIST.tail_foldl(f,acc))
def foldl1(f,LIST):
    return force(LIST.tl.tail_foldl(f,LIST.hd))
@matcher(Nil,False)
def Tfoldr(self,f,end):
    return end
@matcher(Cons,False)
def Tfoldr(self,f,end):
    return f(self.hd,self.tl.Tfoldr(f,end))
def flip(f):
    return lambda a,b: f(b,a)
def foldr(f,end,LIST):
    " https://wiki.haskell.org/Fold#Overview "
    f2 = flip(f)
    lst = reverse ( LIST )
    return foldl(f2,end,lst)
def foldr1(f,LIST):
    lst = reverse( LIST )
    f2 = flip(f)
    return foldl1(f2,lst)
@matcher(Nil)
def rev(self):
    return self
@matcher(Cons)
def rev(self):
    return self.tail_foldl(lambda a,b:Cons(b,a),nil)
def reverse(LIST):
    return force(LIST.rev())
@matcher(Nil,False)
def __add__(self,ys):
    return ys
@matcher(Cons,False)
def __add__(self,ys):
    #print "__add__:",self
    #return reverse ( foldl(lambda b,a:Cons(a,b),reverse(ys),self )
    #return reverse ( foldl(lambda b,a:Cons(a,b),reverse(self),ys) )
    return foldr (Cons,ys,self)
@matcher(Nil)
def tail_map(self,f,acc):
    return acc
@matcher(Cons)
def tail_map(self,f,acc):
    #print "tail_map:",self.hd
    return self.tl.tail_map(f,Cons( apply(f,self.hd) ,acc) )
def Map(f,LIST):
    lst = reverse(LIST)
    return force(lst.tail_map(f,nil))
@matcher(Nil)
def element(self,obj,acc):
    return acc
@matcher(Cons)
def element(self,obj,acc):
    if self.hd == obj:
        return True
    return self.tl.element(obj,acc)
def elem(obj,lst):
    return force(element(lst,obj,False))
@matcher(Nil,False)
def null(self):
    return True
@matcher(Cons,False)
def null(self):
    return False

def Concat(lst):
    return foldl (lambda a,b:a + b,nil,lst)

@matcher(Nil)
def tail_length(self,acc):
    return acc
@matcher(Cons)
def tail_length(self,acc):
    return self.tl.tail_length(acc+1)
def length(lst):
    return force ( lst.tail_length (0) )
@matcher(Nil)
def tail_toPylist(self,acc):
    return acc
@matcher(Cons)
def tail_toPylist(self,acc):
    return self.tl.tail_toPylist ( [self.hd]+acc )
def toPylist(lst):
    return force( reverse(lst).tail_toPylist( [] ) ) 
@Tail
def tail_toList(lst,acc):
    if lst == []:
        return acc
    return tail_toList(lst[1:],Cons(lst[0],acc))
def toList(lst):
    #print lst
    lst = list(reversed(lst))
    return force ( tail_toList(lst,nil) )
#print isinstance(Cons(1,nil),List)
#tmp = toList([1,2,3])
#print tmp
#tmp2 = force(tail_toPylist(tmp,[]))
#print tmp2
#print force(tmp.rev())
#print reverse(tmp)
#print tmp
#print ( tmp + tmp )
#print Map(lambda x:x+1,(tmp+tmp))
#print Map(lambda x:x+1,nil)
def mret(v):
    def curry_ret(inp):
        return Cons((v,inp),nil)
    return curry_ret
def zero(inp):
    return nil
def uncurry(f):
    return lambda a,b:f(a)(b)

def bind(p,f):
    def cbind(inp):
        temp = p(inp)
        func = uncurry(f)
        #print "temp:",temp,f,func
        #reverse ( force( Concat (Map(func,temp) , nil) ) )
        return Concat( Map(func,temp) )
    return cbind
def sat(p):
    @matcher(Nil,False)
    def csat(self,p):
        #print "Nil csat"
        return zero( nil )
    @matcher(Cons,False)
    def csat(self,p):
        if p(self.hd):
            return mret ( self.hd )(self.tl)
        else:
            return zero( self.tl )
    def currysat(inp):
        return inp.csat(p)
    return currysat
#print sat(lambda x:x=='a')(toList('abc'))
def char(c):
    return sat(lambda x:c==x)
@matcher(Nil,False)
def string(self):
    return mret ( nil )
@matcher(Cons,False)
def string(self):
    return bind(char(self.hd),lambda _:
            bind(self.tl.string(),lambda _:
            mret ( Cons(self.hd,self.tl) )))
def alt(p):
    def calt(q):
        def ccalt(inp):
            t1 = p(inp)
            t2 = q(inp)
            return t1 + t2
        return ccalt
    return calt
def seq(p):
    def cseq(q):
        return bind(p,lambda v: 
               bind(q,lambda w:
                mret ( (v,w) ) ))
    return cseq

def many(p):
    return alt(bind(p,lambda x:
                bind(many(p),lambda xs:
                     mret(Cons(x,xs))  )))(mret(nil))
def many1(p):
    return bind(p,lambda x:
            bind(many(p),lambda xs: mret(Cons(x,xs)) ))
def sepby1(p):
    def csepby1(sep):
        temp = many (bind(sep,lambda _ : 
                      bind(p, lambda y : mret (y) )))
        return bind (p,lambda x : 
                bind(temp,lambda xs: mret ( Cons(x,xs) ) ))
    return csepby1
def sepby(p):
    def csepby(sep):
        return alt (sepby1(p)(sep)) (mret( nil ) )
    return csepby
def bracket(open):
    def cbracket(p):
        def ccbracket(close):
            return bind(open,lambda _:
                    bind(p,lambda x :
                    bind(close,lambda _:
                    mret ( x ) )))
        return ccbracket
    return cbracket
def chainl1(p):
    def cchainl1(op):
        rest = lambda x : alt(bind(op,lambda f :
                            bind(p,lambda y :
                            rest (f (x,y) ) ))) ( mret (x) )
        return bind(p,rest)
    return cchainl1
def chainr1(p):
    def cchainr1(op):
        return bind(p,lambda x:
                alt(bind(op,lambda f : 
                bind( chainr1(p)(op) ,lambda y :
                mret ( f(x,y) )) ) ) ( mret(x) ) )
    return cchainr1

def ops(xs):
    def cops(t):
        p,op = t
        return bind(p,lambda _ : mret (op) )
    return foldr1(uncurry(alt),Map(lambda p,op:bind(p,lambda _:mret(op)),xs))

def chainl( p ):
    def cchainl(op):
        def ccchainl(v):
            return alt( chainl1(p)(op) ) (mret (v) )
        return ccchainl
    return cchainl
def chainr( p ):
    def cchainr(op):
        def ccchainr(v):
            return alt( chainr1(p)(op) ) (mret (v) )
        return ccchainr
    return cchainr
def nat(inp):
    Op = lambda m,n : 10  *  m + n
    temp = bind(digit,lambda x : mret ( ord(x) - ord('0') ) )
    return chainl1 (temp) ( mret (Op) )(inp) 
digit = sat (lambda x : '0' <= x and x <= '9')
"""
one = toList("123")
two = toList("456")
print "elem:",elem("4",two)
print nat(one)
print one + two
"""

lower = sat (lambda x : 'a' <= x and x <= 'z')
upper = sat (lambda x : 'A' <= x and x <= 'Z')

letter  = alt(lower)(upper)
alphanum = alt(letter)(digit)
"""
ident = bind(lower,lambda x : 
        bind (many(alphanum),
        lambda xs : mret (Cons(x,xs)) ))
"""
ident = bind(letter,lambda x:
             bind (many(alphanum),lambda xs:
            mret( Cons(x,xs) ) ) )
                   
"""
a = char('a')
q = char(",")
b = char('b')
test = toList('abc')
manya = many(a)(toList('aaab'))
print sepby1(a)(q)(toList("a,a,a,a"))
print manya
print a(test)
print q(toList(',a'))
print b(toList('bcd'))

open = char('(')
close = char(')')
bt = bracket(open)(a)(close)
print bt(toList('(a)'))

ttt = toList([1,2,3])
print ttt
print foldl(lambda a,b:(a,b),0,ttt)
print foldr(lambda a,b:(a,b),0,ttt)
print ttt.Tfoldr(lambda a,b:(a,b),0)
print foldl1(lambda a,b:(a,b),ttt)
print foldr1(lambda a,b:(a,b),ttt)

addop = sat(lambda x: x == '+')
subop = sat(lambda x: x == '-')
test = toList( [(addop,lambda a,b:a+b),(subop,lambda a,b:a-b)] )

print test
tempops = ops( test )
print tempops(toList("+"))
Int = bind(digit,lambda x : mret(int(x)))
print chainl1(Int)(tempops)(toList('1+2+3-1'))
print chainr1(Int)(tempops)(toList('1+2+3-1'))
data = toList("data").string()
print data(toList("data"))
"""
def spaces(inp):
    isSpace = lambda x: x == ' ' or x == '\n' or x=='\t'
    return bind(many1(sat (isSpace) ),lambda _ :
                mret ( () ) )(inp)
#print "spaces:",spaces(toList(" \t\n"))
def comment(inp):
    return bind(string(toList("--")),lambda _:
            bind(many(sat(lambda x : x!="\n")),lambda _:
            mret ( () ) ))(inp)
#print "comment:",comment(toList("-- hello"))
def first(p):
    @matcher(Nil,False)
    def cfirst(self):
        return self
    @matcher(Cons,False)
    def cfirst(self):
        return Cons(self.hd,nil)
    return lambda inp : (p(inp)).cfirst()
def alt1(p,q):
    def calt1(inp):
        return first ( alt(p)(q) )(inp)
    return calt1
def junk(inp):# unit Parser 
    return bind (many ( alt1(spaces,comment) ) ,
                 lambda _ : mret ( () ) ) (inp)
#tmp = junk(toList("-- hi -- \n  \n\t"))
#print length(tmp)
#for i in toPylist(tmp):
#    print "tmp:",i
#print "----------"
def token(p):#parse
    return bind(p,lambda v:
            bind(junk,lambda _ :
            mret ( v ) ) )
def parse(p):#token
    return bind(junk,lambda _ :
            bind(p,lambda v : mret (v) ))
natural = token(nat)
#print natural(toList("1234"))
def symbol(xs):
    return token(string(xs))
#print symbol(toList("data"))(toList("data"))
def identifier(ks):
    def h(x):
        #print x,ks,elem(x,ks),type(x),type(ks)
        if elem(x,ks):
            return zero
        return mret(x)
    return token( bind(ident,h) )

#data = toList("data")
#typ = toList("type")
#datas = toList( [data,typ] )
#print "elem:",elem(data,datas)
#print data == data
#t = identifier(datas)(data)
#print "data:",t
#print "len:",length( t )
def read(e):
    def cread(input):
        inp = toList(input)
        result = e(inp)
        assert isinstance(result,Cons),"Parse not all: " + repr(result)
        if isinstance(result.hd[1] ,Nil):
            return result.hd[0]
        raise Exception("Parse not all: "+repr(result))
    return cread
