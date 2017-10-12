#coding=utf-8
class Function:
    def __init__(self,fn,globals_env=globals()):
        self._fn = fn
        self.env = globals_env
        #print self.env
        # 传入环境要在函数定义后
    def __repr__(self):
        return "< {name} {func} >".format(name=self.__class__.__name__,func=self._fn)
    def __str__(self):
        return "< {name} {func} >".format(name=self.__class__.__name__,func=self._fn)
    def __neg__(self):
        return self
    def __getattr__(self,gn=None):
        self._gn = self.env[gn] if gn else None
        self.compose = lambda a:self._fn(self._gn(a)) if self._gn else None
        # 连续 复合 (组合) 的时候有些问题...emmmm
        #print type(self.compose),type(self.gn)
        return self.compose
    def __call__(self,arg):
        return self._fn(arg)
class Var:
    # self.env :: dict 
    # 可以构造一个局部环境 从而不影响 源环境的问题
    def __init__(self,name,globals_env=globals()):
        self._name = name
        self.env = globals_env
    def __lt__(self,val):
        self._val = val
        self.env[self._name] = val
        return self._val
    
#class Env:
#    def __init__(self,local_env):
#        self._env = local_env
#    def __getattr__(self,name):
#        return self._env[name]
#    ...

# 两个不同类之间的 __neg_ __le__ 方法的组合 来实现例如 <- 
# 实现 从容器类里获取值 (或者Monad) 
class Data(object):
    def __init__(self,value):
        self._value = value
    def __repr__(self):
        return "< {name} {v} :: {t} >".format(name=self.__class__.__name__,
                                              v=self._value,t = type(self._value))
    def __neg__(self):
        #print self.__repr__()
        return self._value
    
def f(a):
    print "fn:",a
    return a+1
def g(b):
    print "gn:",b
    return b+1
this = globals()
A = Function(f,this)
G = Function(g,this)
#print "A.G:",type(A.G),type(A)
#print Var('a',globals()) <- Function(g,this)
#print a.f(233)
r = [Var('a',this) <- A,
     Var('a',this) <- Data("123"),
     Var('a',this) <- Data(233)]
del a
print r
