#coding=utf-8
# this is simple typecheck 
class TypeCheck:
    """
    @TypeCheck(result=int,i = int)
    def abc(i):
        return i + 1
    @TypeCheck(result=int)
    def abc():
        return 666
    """

    def __init__(self,*arg,**kawg):
        import types
        self.type_maps = kawg
        print self.type_maps
        self.func = arg[0] if len(arg)>0 else None
        if kawg == {}:
            # not typecheck
            self.__call__ = self.func.__call__
            # else def __call__:
    def __call__(self,fn):
        self.func = fn
        self.co  = self.func.func_code
        self.argnames = list(self.co.co_varnames)
        print self.argnames,self.type_maps.keys()
        # init result
        try:
            if self.co.co_argcount == 0 :
                assert self.type_maps.has_key("result"),"Your need default result type"
            assert len(self.type_maps) == self.co.co_argcount+1,"Error: type arg len not equal {f} arg length".format(f=self.func.func_name)
            test = filter(lambda x : x not in self.argnames,self.type_maps.keys())
            test.remove('result')
            assert test == [] ,"Error: type:{} is not arg:{}".format(test,self.argnames)
        except AssertionError,e:
            print e
            exit()
        return self.excute
    def excute(self,*arg,**kawg):
        try:
            if len(arg)==0 and len(kawg)==0:
                env = {}
                r = eval(self.co,env)
                # print type(self.type_maps['result']),type(r)
                assert type(r) == self.type_maps['result'],"Error: {r} not is result={t}".format(t=self.type_maps['result'],r=type(r))
                return r
            if len(kawg)==0:
                # all arg
                env = dict(zip(self.argnames,arg))
                print env
                for i,v in zip(env.keys(),env.values()):
                    assert type(v) == self.type_maps[i] ,"arg {v} type not is {i}".format(v=i,i=self.type_maps[i])
                r = eval(self.co,env)
                assert type(r) == self.type_maps['result'],"Error: {r} not is result={t}".format(t=self.type_maps['result'],r=type(r))
                return r
            if len(arg) == 0:
                # all kawg
                env = kawg
                for i,v in zip(env.keys(),env.values()):
                    assert type(v) == self.type_maps[i] ,"arg {v} type not is {i}".format(v=i,i=self.type_maps[i])
                r = eval(self.co,env)
                assert type(r) == self.type_maps['result'],"Error: {r} not is result={t}".format(t=self.type_maps['result'],r=type(r))
                return r
            if len(kawg)+len(arg) == self.co.co_argcount:
                maps = set(kawg.keys())
                names = set(self.argnames)
                tmpr = list(names - maps)
                tt = dict(zip(tmpr,arg))
                env = dict(tt.items()+kawg.items())
                for i,v in zip(env.keys(),env.values()):
                    assert type(v) == self.type_maps[i] ,"arg {v} type not is {i}".format(v=i,i=self.type_maps[i])
                r = eval(self.co,env)
                assert type(r) == self.type_maps['result'],"Error: {r} not is result={t}".format(t=self.type_maps['result'],r=type(r))
                return r
        except AssertionError,e:
            print e
            exit()

@TypeCheck(result=tuple,a=int,b=int)
def cba(a,b):
    return (a,b)
print cba(a=1,b=1)

@TypeCheck(result=NoneType)
def abc():
    print "abc"
    # return None
print abc()

