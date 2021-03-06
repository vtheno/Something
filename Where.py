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
class maps(dict):
    __init__ = dict.__init__
    def __getattr__(self,name):
        return self[name]
    def __setattr__(self,name,value):
        self[name] = value
        return value

class Let:
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
        return maps(self.env)
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
    Let("""
a = 233
c = lambda id:id
print a,b,c
print locals()
    """) | where(b = 1)
    # 调用结果就是在 源传入环境上 调用 名称
    tmp = Let("""
print a > b and a or b
print locals()
    ""","""
print "a:",a
print "b:",b
"""
          ) | where(b = (lambda fn:fn)(66) ,
                    a = 213) # 类似 let 局部 还没法实现let*
    print tmp.a,tmp.b
    # 这里遇到了和 Case_exec.py 一样的缩进问题...

__all__ = ['where','maps','Let']
