#coding=utf-8
from Case_exec import *
# of中的重名问题
# code 中的多行问题 ?? 加一个 parser???
a = 233

of = make_of(globals())
Case(a) <- \
    Do(
        of(233) <= """a = "233"
print type(a)
print a""",
        of(243) <= "a+=2;print a",
    )

print memoryview(a)
