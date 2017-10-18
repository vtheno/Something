#coding=-utf-8
# from write scheme in 48 hours
def foldl(fn,acc,lst): 
   if lst == []:                                  
       return acc
   else:
       return foldl(fn,fn(acc,lst[0]),lst[1:])
def flip(fn):
    return lambda a,b:fn(b,a)
def foldr(fn,end,lst):
    if lst == []:
        return end
    return fn(lst[0],foldr(fn,end,lst[1:]))
print foldl(lambda a,b:(a,b),0,range(1,4))
print reduce(lambda a,b:(a,b),range(1,4),0)
print foldr(lambda a,b:(a,b),0,range(1,4))
def id(a): return a
def compose(f,g):
    def _x(x):
        return f(g(x))
    return _x
