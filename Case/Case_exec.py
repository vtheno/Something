#coding=utf-8
#env = {}
"""
example: 
       see -> test()
"""
# 无法在 Of 内 进行赋值操作
class Case:
    def __init__(self,var):
        self._var = var

    def __lt__(self,rsub):
        #__le__
        if isinstance(rsub,Do):
            self.env = rsub.getEnv() 
            # add type check pass some bad 
        else:
            return
        if self.env.has_key(self._var):
            return self.env.get(self._var)()
        else:
            return 
    def __repr__(self):
        return "< {n} {v} >".format(n=self.__class__.__name__,
                                    v=self._var)

class Do:
    def __init__(self,*DoArgs):
        self.DoArgs = map(lambda x: x.getEnv() if isinstance(x,Of) else None,list(DoArgs))
        self.DoArgs = filter(lambda x: x != None,self.DoArgs)
        # add type check pass some bad 
        #print self.DoArgs
        self._env = {}
        for i in self.DoArgs:
            self._env = dict(self._env.items()+i.items())

    def __neg__(self):
        return self

    def __repr__(self):
        return "< {n} {v} >".format(n=self.__class__.__name__,
                                    v=self._env)

    def getEnv(self):
        return self._env

class Of:
    def __init__(self,name,le_env):
        self._name = name
        self._env = {}
        self._le_env = le_env
        # _le_env 是外部 环境 暂时不知道怎样动态确定环境
    def __le__(self,val):
        self._val = val
        def delay():
            #exec val in self._le_env
            tmp = compile(self._val,'','exec')
            # compile 解决多行和字符串的问题
            exec tmp in self._le_env
            return self._le_env
        self._env[self._name] = delay
        return self
        
    def __repr__(self):
        return "< {n} {v} >".format(n=self.__class__.__name__,
                                    v=self._env)

    def getEnv(self):
        return self._env

def make_of(env):
    """ of = lambda x:Of(x,globals()) """
    """ #of = make_of(globals()) """
    def of(name):
        return Of(name,env)
    return of


def test():
    Case(1) <- \
        Do ( of(0) <= 'print 233',
             of(1) <= "print 'other'",
        ) 
