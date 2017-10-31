#coding=utf-8
#  
#  _("""
#  print (a if a>b else b)
#  """) | where(a = 1,b = 2)
# 
def where(env = None,**maps):
    env = {} if env == None else env
    # 确保每次调用未初始值不延续到下一次调用
    assert isinstance(env,dict) and isinstance(maps,dict),"TypeError"
    def set_(name,val):
        # 无法用 globals()=dict(globals().items()+env.items()),写成函数的原因是匿名函数内 "不直接支持" 赋值
        env[name] = val
        return True
    map(set_,maps.keys(),maps.values())
    return env

class _:
    def __init__(self,*args): 
        self.args = list(args)
        self.cos  = map(lambda x:compile(x,'','exec'),self.args)
    def __or__(self,env):
        assert isinstance(env,dict),"TypeError"
        def excute(co):
            #exec co in self.env
            # 此处的eval比较简洁没有其它内置
            return eval(co,self.env)
        self.env = env
        map(excute,self.cos)
        #print self.env.keys()
        #print self.env.values()
        return self.env
#def _(name,env):
#    def tmp(args):
#        print args
#    env[name] = tmp
#    return True
#print _(">",globals())
# 除非有办法改 paser 的报错 不然还是绕不过去
def test():
    myenv = {}#globals() or {}
    #print where(b = 1 if a else 2)
    _("""
a = 233
c = lambda id:id
print a,b,c
print locals()
    """) | where(b = 1)
    # 调用结果就是在 源传入环境上 调用 名称
    _("""
print a > b and a or b
print locals()
    """) | where(b = 2,a = 2) # 类似 let 局部 还没法实现let*
    # 这里遇到了和 Case_exec.py 一样的缩进问题...
test()
