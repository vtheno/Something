from types import *
from TypeCheck import TypeCheck
@TypeCheck(result=TupleType,a=IntType,b=IntType)
def cba(a,b):
    return (a,b)
print cba(a=1,b=1)

@TypeCheck(result=int,a=int)
def abc(a):
    print "abc"
    return a-1
print abc('a')
