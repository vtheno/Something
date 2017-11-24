#coding=utf-8
# python3.5+
# __annotations__
# 用于调试时的辅助装饰器
# 真正上线运行时删掉即可
def typecheck(fn):
    assert isinstance(fn,type(lambda _:_))
    func     = fn
    types    = fn.__annotations__
    # if arg type is function then check???
    #
    defaults = fn.__defaults__
    if defaults != None:
        raise TypeError("Not support defaults arg value")
    name     = fn.__name__
    code     = fn.__code__
    Vars     = code.co_varnames
    argcount = code.co_argcount
    if len(types)-1!=argcount:
        raise TypeError("Not support not declare arg type")
    def checktype(maps,types,check_return):
        keys = list(types.keys())
        if check_return:
            keys = ['return']
        else:
            keys.remove('return')

        for i in keys:
            #print (i,maps.keys(),types.keys())
            flag = not isinstance(maps[i],types[i])
            if flag:
                err_msg = "type({}) not equal {}".format(i,types[i].__name__)
                raise TypeError(err_msg)
        return True

    def check(maps):
        checktype(maps,types,False)
        result   = {'return':func(**maps)}
        checktype(result,types,True)
        return result['return']

    def function(*args,**kawg):
        l = len(args)
        k = len(kawg)
        if l+k != argcount:
            raise TypeError("{} takes {} positional arguments but {} were given".format(name,argcount,l+k))
        if all(map(lambda x:x==0,[l,k])):
            Maps = {}
        elif l == 0 :
            Maps = kawg
        elif k == 0:
            Maps = dict(zip(Vars,args))
        elif l+k == argcount:
            Maps = kawg
            tmpkey = list(set(Vars) - set(Maps.keys()))
            Maps.update(dict(zip(tmpkey,args)))
        
        return check(Maps)

    function.types = types
    return function

def debug():
    @typecheck
    # b:str='233'
    def aaa(a:int,b:int) -> str:
        print( a,b )
        return "b"
    print( aaa(2,1) )
    print ( aaa.types)

debug()
__all__ = ['typecheck']
