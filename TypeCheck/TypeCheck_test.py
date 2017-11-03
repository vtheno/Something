from types import *
from TypeCheck import TypeCheck,anything
@TypeCheck(result=TupleType,a=IntType,b=IntType)
def cba(a,b):
    return (a,b)


@TypeCheck(result=int,a=int,b=int)
def abc(a,b):
    return a+b
def test(code,env):
    try:
        xx = compile(code,'','exec')
        print code,
        exec xx in env#eval(xx,env)
        #print abc('a')
    except TypeError,e:
        print e

@TypeCheck(result=anything,a=anything)
def anys(a):
    return a
print anys(anys)
codes = ["print abc('a','b')",
         "print abc(1)",
         "print abc(1,2)",
         "print abc(1,2,3)",
         "print abc(1,a=2)",
         "print abc(1,b=2)",
         "print abc(1,a=1,b=2)",
         "print abc(a=1,b=2)",
         "print abc(b=1,a=2)",
         "print abc(a=1,b=2,c=3)",
]
map(lambda x:test(x,globals()),codes)

print abc
