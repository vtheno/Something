#coding=utf-8
# this is simple typecheck 
class Anything:
    __name__ = 'a'
    def __repr__(self) : return "<type:{}>".format(self.__name__)
    pass
anything = Anything()
class TypeCheck:
    """
    @TypeCheck(result=int,i = int)
    def abc(i):
        return i + 1
    @TypeCheck(result=int)
    def abc():
        return 666
    @TypeCheck(result=anything)
    def abc():
        return abc
    """
    def __init__(self,*arg,**kawg):
        self.type_maps = kawg
        self.func = arg[0] if len(arg)>0 else None
        if kawg == {}:
            # not typecheck
            self.__call__ = self.func.__call__
            # else def __call__:
    def __call__(self,fn):
        self.func = fn
        self.co  = self.func.func_code
        self.argnames = list(self.co.co_varnames)
        self.argcount = self.co.co_argcount
        # init result
        try:
            if self.co.co_argcount == 0 :
                assert self.type_maps.has_key("result"),"Your need default result type"
            assert len(self.type_maps) == self.argcount+1,"type arg len not equal {f} arg length".format(f=self.func.func_name)
            test = filter(lambda x : x not in self.argnames,self.type_maps.keys())
            test.remove('result')
            assert test == [] ,"type:{} is not arg:{}".format(test,self.argnames)
        except AssertionError,e:
            raise TypeError(e)
        return self.excute
    def __repr__(self):
        if self.type_maps !={}:
            def construct(a):
                return "{a} -> ".format(a=a)
            r = ''
            for k,v in zip(self.type_maps.keys(),self.type_maps.values()):
                if k =='result':
                    continue
                r+=construct(v.__name__)
            r += '{r}'.format(r=self.type_maps['result'].__name__)
            return "  {} :: {}  ".format(self.func.__name__,r)
        else:
            return self.func.__repr__()

    def checkEnv(self,env):
        for i,v in zip(env.keys(),env.values()):
            v_type =self.type_maps[i]
            if isinstance(v_type,Anything):
                continue
            assert isinstance(v,v_type) ,"arg {v} type not is {i}".format(v=i,i=self.type_maps[i])

    def checkR(self,r,r_type):
        if isinstance(r_type,Anything):
            return r
        assert isinstance(r,r_type),"{r} not is result={t}".format(t=self.type_maps['result'],r=type(r))
        return r

    def excute(self,*arg,**kawg):
        try:
            l = len(arg)
            k = len(kawg)
            # case(0) of abs(self.argcount - (l+k))
            assert l+k == self.argcount,"input arg length {c} func arg length".format(
                c='>' if l+k > self.argcount else '<')
            # of abs(l-k) 
            if l == 0 and k == 0:
                # 无输入参数
                env = {}
                if self.func.func_defaults == None:
                    assert self.argcount == 0,"func need some arg"
                else:
                    env = dict(zip(self.argnames,self.func.func_defaults))
                r = self.func(*arg,**kawg)#eval(self.co,env)
                r_type = self.type_maps['result']
                return self.checkR(r,r_type)
            # of k
            if k == 0:
                # all arg 所有的都是未指定参数名的的参数
                env = dict(zip(self.argnames,arg))
                self.checkEnv(env)
                r = self.func(*arg,**kawg)#eval(self.co,env)
                #r = eval(self.co,env)
                r_type = self.type_maps['result']
                return self.checkR(r,r_type)
            # of l
            if l == 0:
                # all kawg 所有的都是指定参数名的参数
                env = kawg
                self.checkEnv(env)
                r = self.func(*arg,**kawg)#eval(self.co,env)
                #r = eval(self.co,env)
                r_type = self.type_maps['result']
                return self.checkR(r,r_type)
            # of abc(self.argcount - (l+k))
            if l+k == self.co.co_argcount:
                # 部分指定了名 的参数 部分没有指定名的参数
                maps = set(kawg.keys())
                names = set(self.argnames)
                tmpr = list(names - maps)
                tt = dict(zip(tmpr,arg))
                env = dict(tt.items()+kawg.items())
                self.checkEnv(env)
                r = self.func(**env)#eval(self.co,env)
                #r = eval(self.co,env)
                r_type = self.type_maps['result']
                return self.checkR(r,r_type)
        except AssertionError,e:
            raise TypeError(e)

__all__ = ['TypeCheck','anything']
