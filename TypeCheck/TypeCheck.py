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
    def excute(self,*arg,**kawg):
        try:
            l = len(arg)
            k = len(kawg)
            assert l+k == self.argcount,"input arg length {c} func arg length".format(
                c='>' if l+k > self.argcount else '<')
            if l == 0 and k == 0:
                # 无输入参数
                env = {}
                if self.func.func_defaults == None:
                    assert self.argcount == 0,"func need some arg"
                else:
                    env = dict(zip(self.argnames,self.func.func_defaults))
                r = eval(self.co,env)
                assert type(r) == self.type_maps['result'],"{r} not is result={t}".format(t=self.type_maps['result'],r=type(r))
                return r
            if k == 0:
                # all arg 所有的都是未指定参数名的的参数
                env = dict(zip(self.argnames,arg))
                for i,v in zip(env.keys(),env.values()):
                    assert type(v) == self.type_maps[i] ,"arg {v} type not is {i}".format(v=i,i=self.type_maps[i])
                r = eval(self.co,env)
                assert type(r) == self.type_maps['result'],"{r} not is result={t}".format(t=self.type_maps['result'],r=type(r))
                return r
            if l == 0:
                # all kawg 所有的都是指定参数名的参数
                env = kawg
                for i,v in zip(env.keys(),env.values()):
                    assert type(v) == self.type_maps[i] ,"arg {v} type not is {i}".format(v=i,i=self.type_maps[i])
                r = eval(self.co,env)
                assert type(r) == self.type_maps['result'],"{r} not is result={t}".format(t=self.type_maps['result'],r=type(r))
                return r
            if l+k == self.co.co_argcount:
                # 部分指定了名 的参数 部分没有指定名的参数
                maps = set(kawg.keys())
                names = set(self.argnames)
                tmpr = list(names - maps)
                tt = dict(zip(tmpr,arg))
                env = dict(tt.items()+kawg.items())
                for i,v in zip(env.keys(),env.values()):
                    assert type(v) == self.type_maps[i] ,"arg {v} type not is {i}".format(v=i,i=self.type_maps[i])
                r = eval(self.co,env)
                assert type(r) == self.type_maps['result'],"{r} not is result={t}".format(t=self.type_maps['result'],r=type(r))
                return r
        except AssertionError,e:
            raise TypeError(e)

__all__ = ['TypeCheck']
