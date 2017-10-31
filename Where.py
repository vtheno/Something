#coding=utf-8
#  
#  _("""
#  print (a if a>b else b)
#  """) | where(a = 1,b = 2)
  
def make_where(env):
    assert isinstance(env,dict),"TypeError"
    def set_(name,val):
        # 无法用 globals()=dict(globals().items()+env.items())
        env[name] = val
        return True
    def where(**maps):
        assert isinstance(maps,dict),"TypeError"
        #print " e is globals() ",e == globals()
        map(set_,maps.keys(),maps.values())
        return env
    return where
class _:
    def __init__(self,*args): 
        self.args = list(args)
        self.cos  = map(lambda x:compile(x,'','exec'),self.args)
    def __or__(self,env):
        assert isinstance(env,dict),"TypeError"
        def excute(co):
            #exec co in self.env
            return eval(co,self.env) # 此处的eval比较简洁没有其它内置
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
    where = make_where(myenv)
    a = 233
    #print where(b = 1 if a else 2)
    _("""
a = 233
c = lambda id:id
print a,b,c
    """) | where(b = 1,c=a)
    # 调用结果就是在 源传入环境上 调用 名称
    _("""
print a > b and a or b
    """) | where(a = 1,b = 2)
    # 这里遇到了和 Case_exec.py 一样的缩进问题...
test()
