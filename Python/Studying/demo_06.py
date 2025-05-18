"""Functions"""
from functools import wraps

'''Defining a Function'''
#在Python中，函数声明和函数定义是视为一体的
#在Python中不用指定返回值的类型。
#函数参数数量任意，也不用指定类型（Python中变量都是弱类型的，Python会根据值来维护变量的类型）
#return可有可无，可出现在函数体任何位置。如果没有return语句，会自动返回None（空值），如果有return语句，但后面没接任何表达式或值，则也返回None。
#def <name> (<formal parameters>):
#   the body of the function
#   return <return expression> # Non-essential

'''Calling a Function'''
#函数调用
#Calling the function before the function definition is not allowed in Python
def hcf(x, y): # 定义一个函数，该函数返回两个数的最大公约数
    if x > y:
        smaller = y
    else:
        smaller = x
    for i in range(1, smaller + 1): # for i in range(smaller, 0, -1):
       if x % i == 0 and y % i == 0:   # x, y 同时整除 i，则 i 是最大公约数
           z = i
           return z
num1 = int(input("输入第一个数字:"))
num2 = int(input("输入第二个数字: "))
print(f"{num1} 和 {num2} 的最大公约数为: {hcf(num1, num2)}")     # 函数调用

'''Passing Information to a Function'''

'''Arguments and Parameters'''
#实参和形参
# Parameters: Variables变量 in parentheses括号 after the function name when defining a function
def add(a, b):  # Here a and b are the parameters
    return a + b
# Arguments：a piece of information that’s passed from a function call函数调用 to a function.
add(1,2) # Here 1 and 2 are the arguments
x = 2
y = 2
add(x, y)  # Here 1 and 2 are the arguments

'''Passing Arguments'''
#传递实参
# 在C语言中，调用参数时必须依照函数定义时的参数个数以及类型来传递参数，否则就会发生错误。
# 在Python中函数参数定义和传递的方式相比就灵活的多
# a function definition can have multiple parameters-->a function call may need multiple arguments
# 类别：
#     Default Values：在函数定义时，写下默认值
#     positional arguments：No default value provided for parameter;必须按照函数参数顺序传参
#     keyword arguments：在传递参数时，each argument consists of a variable name and a value;
#     lists and dictionaries of values：直接传递列表、字典，python会维护变量类型

#Default Values
def display1(a='hello',b='world'):  #函数定义的时候，分别给出了2个参数a和b的默认值
    print(a+b)
#函数调用的时候，如果不给函数传递参数，就分别采用默认值，如果给了参数，但是没指明参数名，则从左向右匹配。
print('传递实参：默认值')
display1()
display1(b='China')
display1('China')
#使用默认值可简化函数调用，还可清楚地指出函数的典型用法；若没有默认值，只传一个实参会报错
def display2(a,b):
    print(a,b)
#display2('China') #报错

# Positional Arguments
#可用display2
display2('hello', 'world')
display2('China', 'hello')
#默认参数必须放在非默认参数之后
#def display3(x,a='hello',b='world',y): #报错
#位置传参缺点：传参时顺序错乱，导致错误结果；位置参数数量固定，无法处理可变数量的参数

# Keyword Arguments
# 避免用户需要牢记位置参数顺序，可以使用关键字传参
display2(a='world', b='hello')
display2(b='hello', a='world')

#Equivalent Function Calls
# positional arguments, keyword arguments, and default values 混用时，注意函数调用
# 注意：先写位置传参,再写关键字传参
def describe_pet(pet_name, animal_type='dog'):
    """Display information about a pet."""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")
# A dog named Willie.
describe_pet('willie')
describe_pet(pet_name='willie')
# A hamster(仓鼠) named Harry.
describe_pet('harry', 'hamster')
describe_pet(pet_name='harry', animal_type='hamster')
describe_pet(animal_type='hamster', pet_name='harry')

'''Passing an Arbitrary(任意) Number of Arguments'''
# you won’t know ahead of time how many arguments a function needs to accept.
# 不能提前知道函数需要多少个参数；'*' and '**' both indicate that 0 to any number of parameters can be accepted
# 使用 * 将没有匹配的值都放在同一个元组中
#   如果要让函数接受不同类型的实参，必须在函数定义中将接纳任意数量实参的形参放在最后。
#   Python先匹配位置实参和关键字实参，再将余下的实参都收集到最后一个形参中
print()
print('传参：任意参数')
def storename(name, *nickName):
    print('real name is %s' % name)
    if nickName:
        print('小名是', end=' ')
    for nickname in nickName:
        print(nickname, end=' ')
    print('')#换行
storename('张海')
storename('张海', '小海')
storename('张海', '小海', '小豆豆')
# 使用**将没有匹配的值都放在一部字典中
def demo(**p):
    for item in p.items():
        print(item, end=' ')
demo(x=1, y=2, z=3)

#Passing a List
print()
def greet_users(names):
    """Print a simple greeting to each user in the list."""
    for name in names:
        msg = f"Hello, {name.title()}!"
        print(msg)
usernames = ['hannah', 'ty', 'margot']
greet_users(usernames)
# Modifying a List in a Function
'''值传递'''
#python参数传递是值传递，类似于C
#In most cases, modifying the value of a parameter inside a function will not affect the argument.
def addOne(a):
    a += 1
    print(a)
a = 3
addOne(a)
print(a)
'''Modifying a List in a Function'''
def modify1(m, k):
    m = 2
    k = [4, 5, 6]
    return
def modify2(m, k):
    m = 2
    k[0] = 0
    return
n = 100
L = [1,2,3]
modify1(n, L)
print (n, L) # Output：100 [1, 2, 3]
modify2(n, L)
print (n, L) # Output：100 [0, 2, 3]
#原因：在Python中参数传递采用的是值传递方式，在执行函数modify1时，先获取n和L的id( )值，然后为形参m和K分配空间，
#     让m和K分别指向对象100和对象[1,2,3]。m=2这句让m重新指向对象2，而K=[4,5,6]这句让K重新指向对象[4,5,6]。
#     这种改变并不会影响到实参n和L，所以在执行modify1之后，n和L没有发生任何改变；
#     在执行函数modify2时，同理，让m和K分别指向对象2和对象[1,2,3]，
#     然而K[0]=0让K[0]重新指向了对象0（注意这里K和L指向的是同一段内存），
#     所以对K指向的内存数据进行的任何改变也会影响到L，因此在执行modify2后，L发生了改变。

#A mutable(可变的) object can modify the arguments value, while an immutable(不可变的) object cannot modify the arguments value
def modify(d):
    d['age'] = 38
    d = {'name':'Dong', 'sex':'Female'}  #并没有作用
    return
a = {'name':'Dong', 'age':37, 'sex':'Male'}
print(a)
modify(a)
print(a)

#在Python中，函数和方法也是对象。它们可以被赋值给变量，可以作为参数传递给其他函数，还可以作为返回值从函数中返回
#You can even assign a function to a variable
def hi(name="China"):
    return "hi " + name
print(hi())
greet = hi
print(greet())
#函数作为参数传递   Passing a function as an argument to another function
#Higher-order function(高阶函数):函数作为实参传递给其他函数，或作为返回值从其他函数中返回
def apply_twice(f, x):
    return f(f(x))     #可以作为返回值从函数中返回
def square(x):
    return x*x
result = apply_twice(square, 2)    #作为实参传递给其他函数
print('高阶函数：',result)

"""Python Decorator 装饰器"""
#装饰器：利于系统安全性 日志、授权
#装饰器可以在不改动函数的前提下，对函数功能进行扩充
#第一种(但是改变了func函数的名字)
def hi():
    print("hi England!")
def DoSomethingBefore(func):
    print('Hello Hogwarts')
    func()
DoSomethingBefore(hi)
print('被装饰函数名字（原本）：hi')
print('被装饰函数名字（后来）：',hi.__name__)


#第二种(繁琐,且改变了被装饰函数的名字)
def a_new_decorator(a_func): #定义一个装饰函数：输入被装饰函数，输出装饰好的函数
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction
def a_func_requiring_decoration():  #定义一个需要装饰的函数
    print("I am the function which needs some decoration to beautify")
a_func_requiring_decoration = a_new_decorator(a_func_requiring_decoration)
#a_new_decorator该函数被 wrapTheFunction() 装饰
#a_func_requiring_decoration()
print('被装饰函数名字（原本）：a_func_requiring_decoration')
print('被装饰函数名字（后来）：',a_func_requiring_decoration.__name__)

#第三种(good，第二种升级版，省略了一条步骤，但仍然改变了被装饰函数的名字)
def a_new_decorator(a_func):
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction
@a_new_decorator  #a_func_requiring_decoration = a_new_decorator(a_func_requiring_decoration)
def a_func_requiring_decoration():
    print("I am the function which needs some decoration to beautify")
#a_func_requiring_decoration()
print('被装饰函数名字（原本）：a_func_requiring_decoration')
print('被装饰函数名字（后来）：',a_func_requiring_decoration.__name__)
print('不是我们想要的，我们希望被装饰的函数看起来什么都没变')

#第四种(best)
def a_new_decorator(a_func):
    @wraps(a_func) # python提供的装饰器 需要导包
                   #  @wraps接受一个函数来进行装饰，并加入了复制函数名称、注释文档、参数列表等等的功能。
                   #  这可以让我们在装饰器里面访问在装饰之前的函数的原有属性。
                    #无 @ wraps(a_func)：
                    #print(a_func_requiring_decoration.__name__)
                    #Output：
                    #Result：wrapTheFunction
                    #添加 @ wraps(a_func)：
                    #print(a_func_requiring_decoration.__name__)
                    #Output：
                    #Result：a_func_requiring_decoration
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction
@a_new_decorator
def a_func_requiring_decoration():
    print("I am the function which needs some decoration to beautify")
print('被装饰函数名字（原本）：a_func_requiring_decoration')
print('被装饰函数名字（后来）：',a_func_requiring_decoration.__name__)

# Application Scenarios Ⅰ for Decorators —— Authorize(授权
#def requires_auth(f):
#    @wraps(f)
#    def decorated(*args, **kwargs):
#        auth = request.authorization
#        if not auth or not check_auth(auth.username, auth.password):
#            authenticate()
#        return f(*args, **kwargs)
#    return decorated

# Application Scenarios Ⅱ for Decorators —— Log (日志)
def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging
@logit
def addition_func(x):
    return x + x
@logit  #添加日志
def addition_func_2(x):
    return x * x
result = addition_func(4)  #使用addition_func会记录下来
print(result)
result = addition_func_2(4)
print(result)


#Define Functions in a Function
def hi(name="yasoob"):
    print("now you are inside the hi() function")
    def greet():
        return "now you are in the greet() function"
    def welcome():
        return "now you are in the welcome() function"
    print(greet())
    print(welcome())
    print("now you are back in the hi() function")
hi()#无论何时调用hi(), greet()和welcome()将会同时被调用
    # greet()和welcome()函数在hi()函数之外是不能访问的

"""Lambda expressions (匿名函数)"""
#匿名函数
#The expression lambda parameters: expression yields生成 a function object.
#The unnamed object behaves like a function object defined with:
#def <lambda > (parameters):
#    return expression
# 只可以包含一个表达式，表达式的计算结果为函数的返回值
# 不允许包含其他复杂的语句，但在表达式中可以调用其他函数
f = lambda x,y,z: x+y+z
print(f(1,2,3))
#You can use a lambda expression as the return value of a function
def math(k):
    if(k==1): return lambda x, y : x+y #相当于返回一个函数
    if(k==2): return lambda x, y : x-y
    if(k==3): return lambda x, y : x*y
    if(k==4): return lambda x, y : x/y
# Call functions
action = math(1)
print("10+2=",action(10, 2))
action = math(2)
print("10-2=",action(10, 2))
action = math(3)
print("10*2=",action(10, 2))
action = math(4)
print("10/2=",action(10, 2))

#Return Values
#返回值
# 1、Returning a Simple Value  可在返回时处理数据：return full_name.title()
# 2、Returning a Dictionary/List（返回多个值：Lists）
#     A function can return any kind of value you need it to, including more complicated data structures  like lists and dictionaries.
#     Functions in Python can return multiple values which will be returned in a tuple or other type of collection.
# 3、Returning a function
def hi(name="aaa"):
    def greet():
        return "now you are in the greet() function"
    def welcome():
        return "now you are in the welcome() function"
    if name == "aaa":
        return greet # 没加括号——不执行，只是传递
    else:
        return welcome # 没加括号——不执行，只是传递
func1 = hi()   #相当于func1 = greet
func1() # Output: 'now you are in the greet() function'
func2 = hi("jly")   #相当于func2 = welcome
func2() # Output: 'now you are in the welcome() function'

'''The scope of a variable'''
#变量作用域
# The variable name in different scopes can be the same without affecting each other
# Sometimes it is also possible to change the scope of a variable with special keywords.
#四级：
#L (Local):函数内的区域，包括局部变量和参数
#E (Enclosing): 外面嵌套函数的区域，常见的是闭包函数的外层函数
#G (Global):全局作用域
#B (Built-in):内建作用域
#Python检索变量的时候，采用L(局部作用域)-->E(局部外的区域(例如闭包))-->G-->B的规则查找

#Local variables
# 函数内定义的变量作用域只在函数内，函数结束，自动删除
# References to引用 local variables are faster than global variables

#Global variables
# A variable has been defined outside the function
# if you need to assign指定 a value赋值 to this variable in the function,
# and reflect the result of the assignment outside the function, can be defined by the keyword global.
#在函数内部使用全局变量，需要声明全局变量
x = 2 # Global variables
def fun1():
    print (x, end=" ")
def fun2():
    global x   #没有这个，python解释器会不清楚x，以为是局部变量
    x = x+1    #在Python中，如果在函数内部对全局变量进行修改，Python会把此变量当做局部变量
    print (x, end=" ")
fun1() # Output: 2
fun2() # Output: 3
print (x, end=" ") # Output: 3
#Variables specified明确规定 with the global keyword may not exist before
def fun3():
    global x
    x=2
    print (x, end=" ")
def fun4():
    x = 4
    x=x+1
    print (x, end=" ")
fun3()
fun4()
print (x, end=" ")

# nonlocal：keyword that modifies the scope of a variable in a nested function嵌套/内嵌函数.
def fun5():
    count = 1
    def fun_in():
        count = 12
    fun_in()
    print(count)
fun5() # Output Result：1
def fun6():
    count = 1
    def fun_in():
        nonlocal count # 作用域扩充到外层函数
        count = 12
    fun_in()
    print(count)
fun6() # Output Result：12

#Closure Function
# 在Python中，函数支持嵌套。如果在一个内部函数中对外部函数作用域（非全局作用域）的变量进行引用，那么内部函数称为闭包。闭包满足三个条件：
#① 存在于嵌套关系的函数中（内部函数）
#② 嵌套的内部函数引用了外部函数的变量
#③ 嵌套的外部函数将内部函数名作为返回值返回
def func_out(n1 = 0):
    count = [n1] # 外部函数的变量
    def func_inner( ):
        count[0] += 1
        print(count[0])
    return func_inner
quote = func_out(5) #由于在外部函数返回了闭包函数，并且将其赋值给了一个对象，所以认为内部函数(闭包函数)没有消亡
quote() #Output : 6
quote() #Output : 7
#Application of closures
def test(a, b):
    def test_in(c):
        print(a*b+c)
    return test_in
num = test(1,2) # 把test_in引用交给了num，同时把a, b变量也绑定给了num
num(1) # Output：3
num(2) # Output：4
num(3) # Output：5
#Function Composition
def square(x):
    return x * x
def make_adder(n):
    def adder(k):
        return k + n
    return adder
def compose1(f, g):
    def h(x):
        return f(g(x))
    return h
compose1(square, make_adder(2))(3)

#recursive call递归调用 to functions
#The execution实施、执行 process：
#  recursion(递推) process 、 regression(回归) process.
#  These two processes are controlled by the recursive abort中止 condition(终止条件)
#调用示例
#分析问题：分析大概思路
print()
print('递归调用实例'.center(30))
def move(source, target):
    print(source, "-->", target)
def hanoi(n, source, temp, target):
    if(n == 1):
       move(source, target)
    else:
       hanoi(n-1, source, target, temp) # 将 n-1 个盘子搬到中间柱
       move(source, target) # 将最后一个盘子搬到目标柱
       hanoi(n-1, temp, source, target) # 将 n-1 个盘子搬到目标柱
n = int(input("输入盘子数："))
print("移动", n, "个盘子的步骤是：")
hanoi(n, 'A', 'B', 'C')
# Returning a Function Using Its Own Name
def print_sums(n):
    print(n)
    def next_sum(k):
        return print_sums(n + k)
    return next_sum
print_sums(1)(3)(5)
print_sums(1)(3)(5)(7)