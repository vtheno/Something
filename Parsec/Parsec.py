#coding=utf-8
from TypeCheck import TypeCheck
from Infix import Infix
# type object  is anything 
# parsec Learn from : Higher-Order Functions for Parsing by Graham Hutton
class parser(object):
    " Data Type"
    def __init__(self,v,inp):
        # need two arg
        self.value = v,inp
        self.result = v
        self.rest = inp
    def __iter__(self):
        return iter(self.value)
    def __repr__(self):
        return "(  result: {} , rest: {}  ) ".format(self.result,self.rest)

class mlist(object):
    " My List"
    " mlist(1,2) :: ( 1 :: object . (2 .empty) :: mlist)"
    def __init__(self,fst,snd):
        self.fst = fst
        self.snd = snd
        self.value = (fst,snd)
    def empty(self):
        return self.value == (None,None) #"empty"
    def __repr__(self):
        if self.empty():
            return "empty"
        return "({} . {})".format(self.value[0],self.value[1])
    def __iter__(self):
        return iter(self.value)
    def __invert__(self):
        tmp = [ [] ]
        def un_construct(mlst):
            if mlst.empty():
                return []
            else:
                #tmp[0]+=mlst.fst
                #print mlst.fst
                tmp[0].extend (mlst.fst)
                return un_construct(mlst.snd)
        un_construct(self)
        #print tmp
        return tmp[0]#''.join (tmp[0])

@TypeCheck(result=mlist,a=mlist,mlst=mlist)
def extend(a,mlst):
        if a.empty():
            return mlst
        return mlist(a.fst,extend(a.snd,mlst) )

@TypeCheck(result=mlist,string=str)
def make_inp(string):
    xxs = list(string)
    def cons(lst):
        if lst==[]:
            return mlist(None,None)
        return mlist(lst[0],cons(lst[1:]))
    return cons(xxs)

def succeed(v):
    # v -> (mlist -> parser)
    @TypeCheck(result=parser,inp=mlist)
    def p(inp):
        return parser(v,inp)
    return p

" fail is parsec"
fail_flag = "Fail"
fail = succeed(fail_flag)
#print fail(make_inp("123"))

def sat(eq_p):
    # eq_p =>   eq a b = a == b ,:: a -> b -> bool 
    @TypeCheck(result=parser,lst=mlist)
    def p(lst):
        if lst.empty():
            return fail(lst)
        else:
            r,rs = lst
            print "sat:",r,rs
            if eq_p(r):
                print "sat:",type(r)
                return succeed(mlist(r,mlist(None,None)))(rs)
            else:
                return fail(rs)
    return p

@TypeCheck(result=bool,a=object,b=object)
def eq(a,b):
    return a==b

def literal(char):
    # literal 无法做类型检查 ,but uncurry 之后就可以
    # it :: char -> parser 
    @TypeCheck(result=bool,a=object)
    def eq_p(a):
        return eq(a,char)
    return sat(eq_p)
@Infix
def alt(p1,p2):
    @TypeCheck(result=parser,inp=mlist)
    def p(inp):
        r,rest = p1(inp) # p1(inp) :: parser
        #print  isinstance(p1(inp)),parser)
        if r!=fail_flag:
            return succeed(r)(rest) # succeed(r)(rest) :: parser
        return p2(inp)
    return p


@Infix
def then(p1,p2):
    @TypeCheck(result=parser,inp=mlist)
    def p(inp):
        r1,rest1 = p1(inp) # :: parser
        #print type(r1)
        if r1==fail_flag:
            return fail(inp)
        #print "Then1:",r1,extend(r1,rest1)
        r2,rest2 = p2(rest1) #p2(rest1) == r :: parser
        #print type(r2)
        if r2==fail_flag:
            return fail(inp)
        def append(mlst1,mlst2):
            if mlst1.empty():
                return mlst2
            return mlist(mlst1.fst,append(mlst1.snd,mlst2))
        r = append(r1,r2)
        return succeed(r)(rest2)
        #return succeed(succeed(r1)(r2))(rest2)
        #return succeed(r)(rest2)
        # this is seq  递归遍历 construct = mlist(*[r1,r2]) ,cons a ,b = mlist(a,b)
    return p

@Infix
def using(l_p,f):
    @TypeCheck(result=parser,inp=mlist)
    def p(inp):
        r,rs = l_p(inp) # l_p(inp) <=> result :: parser 
        if r!=fail_flag:
            print "using:",r,rs
            return f(r,rs)
        else:
            return fail(rs)
    return p

@TypeCheck(result=parser,a=object,b=object)
def cons(a,b):
    r = a
    rs =b
    #print "type:",type(r),type(rs),r,rs
    if isinstance(r,str):
        if r == fail_flag:
            return fail(rs)
    else:
        print "cons:",a,b
        r = mlist(''.join(~a),mlist(None,None))
        #print "r:",r
        return succeed(r)(rs)
def many(l_p):
    @TypeCheck(result=parser,inp=mlist)
    def p(inp):
        #print inp
        return (
            ( (l_p |then| many(l_p) ) |using| cons )
            |alt|
            succeed( mlist(None,None) ) )(inp) # if l_p(inp) |then| many(l_p)  fail then succeed
    return p

def some(l_p):
    # l_p like literal 
    @TypeCheck(result=parser,inp=mlist)
    def p(inp):
        return  ( (l_p |then| many(l_p)) |using| cons )(inp)
    return p

lst = make_inp("abcde")
nums = make_inp("1234")
r = sat(lambda a:a=="a")(lst)
#print isinstance(r,parser),r
#print literal('a')(lst)
a = literal('a')
b = literal('b')
c = literal('c')
#print ( literal('a') |alt| fail)(lst)
#print (fail |alt| literal('a'))(lst)
#print (a |alt| (b |alt| c))(lst)
#print ( (a |alt| b) |alt| c) (lst)
#print (a |then| b)(lst)
#print (a |then| b |then| c) (lst) 
#print  (a |then| (b |then| c))(lst)
print "----------------"
#print "many:",many(a)(make_inp("aaab"))
#print "some:",some(a)(make_inp("aaab"))

def isdigit(c):
    # eq_p
    return '0'<=c<='9'
num = sat(isdigit)
numbers = some(num)
def isalpha(c):
    return 'a' <= c <= 'z' or 'A'<= c <= 'Z'
word = some(sat(isalpha))
#print num(make_inp("1234"))
#print (numbers)(make_inp("12345"))
#print word(make_inp("abcdef!"))

def string(mlst):
    # mlst :: mlist
    @TypeCheck(result=parser,inp=mlist)
    def p(inp):
        if mlst.empty():
            return succeed( mlist(None,None) )(inp)
        else:
            x,xs = mlst
            return (( literal(x) |then| string(xs)) |using| cons )(inp)
    return p
#print string(make_inp("abc"))(make_inp("abc,def"))

def snd(x,y):
    # snd (x,y) = y
    # just get rest -> return new parser class 容器
    print "snd:",x,"|",y
    return succeed(y)(mlist(None,None))

@Infix
def xthen(p1,p2):
    # p1 :: literal p
    # p2 :: literal p
    @TypeCheck(result=parser,inp=mlist)
    def p(inp):
        return ( (p1 |then| p2) |using| snd )(inp)
    return p

def fst(x,y):
    # fst (x,y) = x
    # const x y = x
    print "fst:",x,y,type(x),type(y)
    return succeed(x)(mlist(None,None))
@Infix
def thenx(p1,p2):
    # p1 :: literal p
    # p2 :: literal p
    @TypeCheck(result=parser,inp=mlist)
    def p(inp):
        return ( (p1 |then| p2 ) |using| fst)(inp)
    return p

print xthen(a,b)(make_inp("abcde"))
#print thenx(a,b)(make_inp("abcde"))
def value(x,y):
    r = {}
    #print "type:", type(x),type(y)
    #print "x,y:",x,y
    if isinstance(x,str):
        if x!="Fail":
            r["Num"]=long(x)
            return succeed(r)(y)
        else:
            return fail(y)
    else:
        print "x:",x
        r["Num"]= long(''.join(~x))
        return succeed(mlist(r,mlist(None,None)))(y)
def op(x,y):
    r = {}
    if isinstance(x,str):
        if x!="Fail":
            r['op']=x
            return succeed(r)(y)
        else:
            return fail(y)
    else:
        r['op'] = ''.join(~x)
        return succeed(mlist(r,mlist(None,None)))(y)
test = ( literal("[") |xthen| ( numbers |thenx| literal("]")) )
t =  test (make_inp("[123]"))
print t.result
plus = ( (numbers|using|value )|then| (literal("+")|using|op) |xthen| (numbers|using|value ))
#n = make_inp("1+2")
#print plus(n)
#print expr(make_inp("(123)"))

# 由于我的TypeCheck只是简单的做类型检查,所以可能有许多麻烦
# 因为上述的fail 类型是 methd ...所以构造会不同
# sat 是 succeed的变体
# 传入一个参数 类型为 object -> bool
# 由于我们有了make_inp 把东西放到 parser类里
# 理清楚这里的类型 就好做了
# 区分清楚哪些函数的类型
# 函数是一个过程 函数参数 转换 到函数返回值 类型的过程

