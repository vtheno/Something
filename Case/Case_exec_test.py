#coding=utf-8
from Case_exec import *
# of中的重名问题
# code 中的多行问题 ?? 加一个 parser???
# 就是缩进的问题...
# 解决思路1:
# 写个 emacs 插件,在新buffer里写,然后该位置用读文件的形式解决
# 然后把相应的 open('xxx').readlines() 替换显示 成文件内容
# 又多了一堆问题 索性这样将就这吧
a = 233
of = make_of(globals())
Case(a) <- \
    Do(
        of(233) <= \
"""
a = "233"
print type(a)
print "a"
def c():
    print "C"
    return "c"
print c()
""",
        of(243) <= \
"a+=2;print a",
    )


#print memoryview(a)
