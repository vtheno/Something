#coding=utf-8
# type object  is anything 
# parsec Learn from : Higher-Order Functions for Parsing by Graham Hutton
from Infix import Infix
from TypeCheck import TypeCheck

class Parser(object):
    """ 容纳 处理的结果或状态 以及余下内容的 容器类型:""" 
    def __init__(self,head,tail):
        self.head=head
        self.tail=tail
    def __repr__(self):
        return "( result : {} ,rest:{} )".format(self.head,self.tail)
    def isFail(self):
        return self.head == None
    def __iter__(self):
        return iter([self.head,self.tail])

class mlist(object):
    """ Lisp 中的 cons 列表 ,当然 这里可以替换为py的list"""
    def __init__(self,head,tail):
        self.head=head
        self.tail=tail
    def __repr__(self):
        args = repr(self.head) if self.head!=None else ""
        if self.tail !=None:
            args +=', {}'.format(repr(self.tail))
        return "({})".format(args)
    def empty(self):
        return self.head == None and self.tail == None
    def __len__(self):
        if self.empty():
            return 0
        else:
            return 1+len(self.tail)
    def __getitem__(self,i):
        if i == 0:
            return self.head
        return self.tail[i-1]
    def __iter__(self):
        return iter([self.head,self.tail])
    def __invert__(self):
        """ 这里将它转换到普通列表 """
        tmp = [ [] ]
        def un_construct(mlst):
            if mlst.empty():
                return []
            else:
                tmp[0].extend (mlst.head)
                return un_construct(mlst.tail)
        un_construct(self)
        print tmp[0]
        return tmp[0]#''.join (tmp[0])

empty_m =mlist(None,None)
#print empty_m,empty_P
print "empty:",empty_m == empty_m
@TypeCheck(result=mlist,string=str)
def str2mlist(string):
    lst = list(string)
    def construct(tmp):
        if tmp == []:
            return empty_m
        return mlist(tmp[0],construct(tmp[1:]))
    r= construct(lst)
    return r

@TypeCheck(result=mlist,s1=mlist,s2=mlist)
def mlist_extend(s1,s2):
    if s1.empty():
        return s2
    return mlist(s1.head,mlist_extend(s1.tail,s2))


def succeed(v):
    @TypeCheck(result=Parser,inp=mlist)
    def curry_succeed(inp):
        return Parser(v,inp)
    return curry_succeed

fail_flag = empty_m
@TypeCheck(result=Parser,inp=mlist)
def fail(inp):
    return succeed(fail_flag)(inp)

def sat(p):
    #p :: * -> bool
    @TypeCheck(result=Parser,inp=mlist)
    def curry_sat(inp):
        if inp.empty():
            return fail(inp)
        else:
            x,xs = inp
            if p(x):
                return succeed(mlist(x,empty_m))(xs)
            else:
                return fail(xs)
    return curry_sat

def literal(c):
    @TypeCheck(result=bool,a=object)
    def curry_eq_p(a):
        return a==c
    return sat(curry_eq_p)
@Infix
def alt(p1,p2):
    @TypeCheck(result=Parser,inp=mlist)
    def curry_alt(inp):
        r,rest = p1(inp) # p1(inp) :: parser
        #print  isinstance(p1(inp)),parser)
        if r!=fail_flag:
            return succeed(r)(rest) # succeed(r)(rest) :: parser
        return p2(inp)
    return curry_alt

@Infix
def then(p1,p2):
    # p1 p2 :: literal(xxx)
    @TypeCheck(result=Parser,inp=mlist)    
    def curry_then(inp):
        r,rs = p1(inp)
        if r!=fail_flag:
            r1,rs1 = p2(rs)
            if r1!=fail_flag:
                #print r,r1,mlist_extend(r,r1)
                res = mlist_extend(r,r1)
                #print "res:",res
                return succeed(res)(rs1)
        return fail(inp)
    return curry_then
@Infix
def using(p,f):
    @TypeCheck(result=Parser,inp=mlist)
    def curry_using(inp):
        tmp = p(inp)
        r = f(tmp)
        return r
    return curry_using
def cons(pc):
    r,rs = pc
    if r == fail_flag:
        return fail(rs) # pc is fail
    else:
        r = mlist(''.join(~r),empty_m)
        return succeed(r)(rs)
def many(p):
    @TypeCheck(result=Parser,inp=mlist)    
    def curry_many(inp):
        return (
            ( (p |then| many(p) ) |using| cons )
            |alt|
            succeed( mlist(None,None) )
        )(inp) # if l_p(inp) |then| many(l_p)  fail then succeed
    return curry_many

def some(l_p):
    # l_p like literal 
    @TypeCheck(result=Parser,inp=mlist)
    def p(inp):
        return  ( (l_p |then| many(l_p)) |using| cons )(inp)
    return p

def string(mlst):
    # mlst :: mlist
    @TypeCheck(result=Parser,inp=mlist)
    def p(inp):
        if mlst.empty():
            return succeed( mlist(None,None) )(inp)
        else:
            x,xs = mlst
            return (( literal(x) |then| string(xs)) |using| cons )(inp)
    return p
print string(str2mlist("abc"))(str2mlist("abc,def"))

@TypeCheck(result=Parser,pc=Parser)
def snd(pc):
    r,rs = pc
    print "snd:",r.head,r.tail
    r = r.tail
    return succeed(r)(rs)

@Infix
def xthen(p1,p2):
    @TypeCheck(result=Parser,inp=mlist)
    def curry_xthen(inp):
        return ( (p1 |then| p2) |using| snd )(inp)
    return curry_xthen

@TypeCheck(result=Parser,pc=Parser)
def fst(pc):
    r,rs = pc
    r = r.head
    if isinstance(r,mlist):
        return succeed(r)(rs)
    else:
        if r==None:
            return pc # fail is fail
        r = mlist(r,empty_m)
        return succeed(r)(rs)

@Infix
def thenx(p1,p2):
    @TypeCheck(result=Parser,inp=mlist)
    def curry_xthen(inp):
        return ( (p1 |then| p2) |using| fst )(inp)
    return curry_xthen

t = str2mlist("aabcdef")
#print t==t
#print succeed('a')(t)
#print fail(t).isFail()
#
#print sat(lambda c:c=='a')(t)
a = literal('a')
#print a(t)
#print (a|then|a)(t)
c= many(a)(t)
print "c:",c
print "head:",c.head
print "tail:",c.tail
print (a |xthen| a)(t)
print (a |thenx| a)(t)

lef = literal("[")
rig = literal("]")
isdigit = lambda x:'0'<=x<='9'
def unconstruct(mlst):
    if mlst.empty():
        return []
    return [mlst.head] + list(unconstruct(mlst.tail))
def value(pc):
    r,rs = pc
    print "value:",r,rs
    res = unconstruct(r)
    res = {"Num":res[0]}
    return succeed(mlist(res,empty_m))(rs)
number = some(sat(isdigit)) |using| value
t2 = str2mlist("1234")
print number(t2)
expr = lef |xthen| number |thenx| rig
print expr(str2mlist("[123]"))
op_add = literal("+") 
plus = (number |thenx| op_add) |then| number
plus2 = number |then| (op_add |xthen| number)
t3 = str2mlist("12+23")
print plus(t3)
print plus2(t3)
def add(pc):
    r,rs = pc
    res = {}
    res["OP"] = "add"
    res['args'] = unconstruct(r)
    return succeed(res)(rs)

print (plus |using| add)(t3)
print a(str2mlist("bbb"))
print many(a) (str2mlist('bbb'))
