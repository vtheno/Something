#coding=utf-8
#env = {}
"""
example: 
>> c = lambda a:a
>> Case(c) <- Do( Of(c) <= "this is c" ) # when

# "this is c"
>> Case(c) <- Do( Of(a) <= "this is a",
                  Of(c) <= "this is c",
                ) 
# "this is c"
>> Case(c) <- ( Do( Of(a) <= "this a",
                    Of(b) <= "this b",
                  ) <= "this otherwise" )
# "this otherwise"
"""
# 无法在 Of 内 进行赋值操作
class Case:
    def __init__(self,var):
        self._var = var

    def __lt__(self,rsub):
        #__le__
        self.env = rsub.getEnv() 
        if self.env.has_key(self._var):
            return self.env[self._var]
        else:
            if self.env.has_key("otherwise"):
                if self.env["otherwise"] != "Nothing":
                    return self.env["otherwise"]
                else:
                    pass
            else:
                pass
    def __repr__(self):
        return "< {n} {v} >".format(n=self.__class__.__name__,
                                    v=self._var)

class Of:
    def __init__(self,name):
        self._name = name
        self._env = {}
        
    def __le__(self,val):
        self._val = val
        self._env[self._name] = val
        return self
        
    def __repr__(self):
        return "< {n} {v} >".format(n=self.__class__.__name__,
                                    v=self._env)

    def getEnv(self):
        return self._env

class Do:
    def __init__(self,*DoArgs):
        self.DoArgs = map(lambda x:x.getEnv(),list(DoArgs))
        self._env = {"otherwise":"Nothing"}
        for i in self.DoArgs:
            self._env = dict(self._env.items()+i.items())

    def __neg__(self):
        return self

    def __le__(self,otherwise):
        self._env["otherwise"] = otherwise
        return self

    def __repr__(self):
        return "< {n} {v} >".format(n=self.__class__.__name__,
                                    v=self._env)

    def getEnv(self):
        return self._env

def test():
    print (Of('a') <= "Something")
    c = lambda a:a
    #print Do(
    #        Of('a') <= "Something",
    #        Of(233) <= "233",
    #        Of(c) <= c(1),
    #    )
    print Case(c) <- \
        Do(
            Of('a') <= "Something",
            Of(233) <= "233",
            Of(c) <= c(1),
        )
    #print Case(c)
    print Case(c) <- ( Do( Of(1) <= "this a",
                           Of(2) <= "this b",) <= "this otherwise")
    #print (Of(lambda a:a) <= 'c' ).getEnv().items()
    #print Case('a') <- Do(Of('c') <= "some")

#test()
