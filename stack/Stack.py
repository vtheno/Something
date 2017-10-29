#coding=utf-8
class Stack:
    # key is addr
    # val is value
    def __init__(self,val={},addr=-1,name=None):
        assert type(val)==dict and type(addr)==int and (type(name) == str or name is None)
        self.val = val
        self.addr = addr # stack top pointer 
        self.name = name if name!=None else self.__class__.__name__
    def push(self,x):
        self.addr +=1
        self.val[self.addr] = x
        return x
    def pop(self):
        #print "pop:",self.val,self.addr
        # dict pop => tmp = dict[keys()[-1]] ; del dict[keys()[-1]];
        t = self.val.pop(self.addr)
        self.addr -= 1
        return t
    def peek(self):
        return self.val[self.addr]
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "< {} var:{} addr:{} >".format(self.name,self.val.values(),self.val.keys())
def intOstr(inp):
    # buffer :: string
    # buffer = readfile()
    # 
    assert type(inp) == str
    if inp.isdigit():
        return int(inp)
    else:
        return inp
class Interpreter:
    # reg 寄存器保存临时结果的计算
    # stack 堆栈以保存直接运行的结果
    """
    AST CODE = {linenum:line_context,...}
    
    """
    env           = locals()
    def __init__(self,C,L):
        self.machine_stack       = Stack({},-1,"S")  # machine data stack
        self.machine_reg         = Stack({},-1,"R")  # machine store memory reg
        self.machine_code        = Stack(C ,-1,"C")  # instruction memory # code excute in 
        self.machine_labels      = Stack(L ,-1,"L")  # key is line ,value is label
        self.ip = 0
        self.run = True
        def temp(name,body):
            return self.template(name,body,self.env)
        temp("add","self.push((lambda num1,num2:int(num1+num2))(self.pop(),self.pop()))")
        temp("sub","self.push((lambda num1,num2:int(num2-num1))(self.pop(),self.pop()))")
        temp("mul","self.push((lambda num1,num2:int(num1*num2))(self.pop(),self.pop()))")
        temp("div","self.push((lambda num1,num2:int(num2/num1))(self.pop(),self.pop()))")
        temp("mod","self.push( (lambda a1,a2:a2%a1)(self.pop(),self.pop()) )")
        temp("dup","( lambda peekValue:self.push(peekValue) ) (self.machine_stack.peek())")
        temp("swap","( lambda num1,num2:[self.push(num1),self.push(num2)][1] )(self.pop(),self.pop()) ")
        self.op = {
            'push' : self.push,# int load 
            'add' : self.add,
            'sub' : self.sub,
            'mul' : self.mul,
            'div' : self.div,
            'mod' : self.mod,
            'pop'  : self.pop,
            'dup'  : self.dup,# copy top
            'swap' : self.swap,
            'load' : self.load,
            'store': self.store, 
            'jz'   : self.jz,
            'jnz'  : self.jnz,
            'jmp'  : self.jmp,
            'show': self.show,
            'halt' : self.stop,
        }
    def push(self,arg):
        return self.machine_stack.push(arg)
    def pop(self):
        return self.machine_stack.pop()
    def template(self,opname,opbody,env):
        code = "lambda self:{body}".format(name=opname,body=opbody)
        env[opname] = eval(code,env)
        return True
    def store(self,arg):
        tmp = self.pop()
        self.machine_reg.val[arg] = tmp
        return tmp
    def load(self,arg):
        tmp = self.machine_reg.val.get(arg)
        return self.push(tmp)
    def show(self):
        top = self.machine_stack.peek()
        print top
        return top
    def stop(self):
        self.run = False
    def setLabel(self,ip,name):
        self.machine_labels.val[ip] = name
    def excute(self):
        code = self.machine_code.val.values()
        labels = filter(lambda x:len(x) == 3 or
                        (len(x)==2 and x[0] not in self.op) or
                        (len(x)==1 and x[0] not in self.op)
                        ,code)
        # label maybe => [label] or [label,op] or [label,op,arg]
        #print labels
        # this need check => eq? labelname opname ,but now not
        map(self.setLabel,map(code.index,labels),map(lambda _: intOstr(_[0]) ,labels))
        # why intOstr(_[0]) (int or str) because ,maybe label is digit
        #print self.machine_labels,self.ip,self.run
        # 第一趟分析出label并记录所有label的信息
        # 第二趟才开始执行 ,
        while self.run:
            line = code[self.ip]
            if len(line) == 1:
                op = line[0]
                if op in self.op:
                    self.op.get(op)()
                else:
                    _ = op
                    
            if len(line) ==3:
                _,op,arg = line
                self.op.get(op)(intOstr (arg) )
            if len(line) ==2:
                op,arg = line
                if op not in self.op:
                    label = op
                    op    = arg
                    self.op.get(op) ()
                else:
                    self.op.get(op)(intOstr (arg) )
            #print self.ip,line,self.machine_stack.val.values(),self.machine_reg.val.values()
            self.ip+=1
    def jmp(self,I):
        # print "index:",self.machine_labels.val.keys()[self.machine_labels.val.values().index(I)]
        try:
            assert I in self.machine_labels.val.values()
            self.ip =  self.machine_labels.val.keys()[self.machine_labels.val.values().index(I)] - 1
        except AssertionError:
            print "jmp <{i}> ERROR,{i} not define,or {i} not is label".format(i=I)
            self.run = False

    def jz(self,I):
        try:
            assert I in self.machine_labels.val.values()
            top = self.pop()
            if top == 0:
                self.ip =  self.machine_labels.val.keys()[self.machine_labels.val.values().index(I)] -1
        except AssertionError:
            print "jz <{i}> ERROR,{i} not define,or {i} not is label".format(i=I)
            self.run = False

    def jnz(self,I):
        try:
            assert I in self.machine_labels.val.values()
            top = self.pop()
            if top != 0:
                self.ip =  self.machine_labels.val.keys()[self.machine_labels.val.values().index(I)] -1
        except AssertionError:
            print "jnz <{i}> ERROR,{i} not define,or {i} not is label".format(i=I)
            self.run = False


def test():
    """
    label :: str or int
    arg   :: int
    op    :: str
    label name can't equal op name
    """
    with open('stack.sasm') as f:
        buffers = filter(lambda x:x!='', map(lambda a: '' if a.startswith("#") else a.strip('\n').strip(' ').strip('\t').split(),f.readlines()))
        buffers = filter(lambda x:x!=[],buffers)
        C = dict(zip(range(len(buffers)),buffers))
        
    L = {}
    i = Interpreter(C,L)
    i.excute()
    print '_________________'
    print i.machine_stack,i.machine_reg
    
test()
