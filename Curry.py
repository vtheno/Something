def _f(x): pass
fnType = type(_f)

class Curry:
    def __init__(self,fn):
        assert type(fn) == fnType,"CurryError {} not is functions".format(fn)
        self._fn = fn
        self._co = self._fn.func_code
        self._argcount = self._co.co_argcount # arg count :: int
        self._args = list(self._co.co_varnames)
        self.make_lambda = lambda n,b:" (lambda {name}: {body}) ".format(name=n,body=b)
        self.make_list = lambda f,t: " {} , {}".format(f,t)
        # [arg1,arg2,arg3,arg4] ...
        # maker fn
        # maker it likes Cons and List 
        # self._body = 'apply(fn,{}'.format(map(str,self._args))
        self.body_args =  self.make_strlst(self._args)
        self._body = 'apply(self._fn,{})'.format(self.body_args)
        # 'self._fn(*{})'.format(self.body_args)
        self._tmp = self.maker(self._args)
        self.curry_func = eval(self._tmp,locals())
        #print self._tmp
    def __repr__(self):
        return "< {n} {v} >".format(n=self.__class__.__name__,
                                    v="( {fn} {arg} )".format(fn=self._fn,arg=self._args)
                                    )
    def make_strlst(self,lst_str):
        return '[ ' + self.lst2str(lst_str) + ' ]'

    def lst2str(self,lst):
        if lst == []:
            return ''
        else:
            return self.make_list(lst[0],self.lst2str(lst[1:]))

    def maker(self,args):                                   
        if args == []:                              
            return self._body                           
        else:                                       
            return self.make_lambda(args[0],self.maker(args[1:]))

    def __lshift__(self,arg):
        #print arg
        tmp = self.curry_func(arg)
        #print tmp
        if type(tmp) != fnType:
            return tmp
        return Curry(tmp)
    def __call__(self,arg):
        return self.__lshift__(arg)
        
@Curry
def abc(a,b):
    return a + b
print abc << 1 << 2 
print abc << 1
print abc(233)

# Uncurry 的话 进行递归展开计算出参数个数
# 用dir去追踪命名空间... 追踪源码
# 类似py的object hasekll的类型类 lisp的风格
# 这个语言不提供任何函数,只提供定义
