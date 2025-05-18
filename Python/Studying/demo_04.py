"""Control statements and Common Algorithms and Application Cases"""
import random

"""if"""
# if 语句没有(),后跟":"; 以缩进来区分
# if conditional_test:
#    do something

"""if-else"""
#if conditional_test:
#    statement segment 1
#else:
#    statement segment 2

"""if-elif-else"""
#if conditional_test1:
#    statement segment1
#elif conditional_test2:
#    statement segment2
# ......
#elif conditional_testn:
#    statement segmentn
#else:
#   statement segmentn+1

"""pass statement"""
#Similar to Null statements, it can be used in class and function definitions, or in branching structures
#当暂时没有确定如何实现功能，或者为以后的软件升级预留空间，或者其他类型功能时，使用 “pass” 来占位。
a = b = 2
if a < b :
    pass # in branch statement
else:
    z = a
class A :
    pass # in class definition
def demo() :
    pass # in function definition

"""while"""
#只有while 没有do-while
#while conditional_test:
#    do something
#conditional_test   可设定quit value
message = '' #先定义
while message != 'quit':
    message = input('\nTell me something, and I will repeat it back to you:')
    print(message)
#conditional_test    可设定常数
#This is an infinite loop program that can be terminated with the help of a break statement
count = 0
while 1:
    print ("The count is:", count)
    count = count + 1
    if count > 10:
        break
print ("Good bye!" )
#pratice:输入两个正整数，求它们的最大公约数(辗转相除法）
x,y = [int(x) for x in input('Enter two numbers: ').split()]
if x < y:
    x,y = y,x
m,n = x,y
r = x%y
while r != 0 :
    x = y
    y = r
    r = x%y
print('最大公约数为',y)

def f(t):
    s = []
    v = 2
    for v in range(1,t+1):
        if t % v == 0:
            s.append(v)
        v += 1 #python 不支持++ --
    return s
m1 = f(m)
m1.reverse()
n1 = f(n)
n1.reverse()
sign = 0
for i in n1:
    for j in m1:
        if j == i:
            print('最大公约数为',j)
            sign = 1
    if sign == 1:
        break

"""for"""
# iterate over the elements of a sequence序列 (such as a string, tuple or list) or other iterable object
#for 循环的本质就是先通过 iter() 函数获取可迭代对象的迭代器；
# 对于可迭代对象，都可以通过iter()函数获取这些可迭代对象的迭代器.
# 然后可以对获取到的迭代器不断的使用next()函数来获取可迭代对象的下一个元素（获取下一个值并将其赋值给item）
# 直至没有数据可获取，则产生StopIteration异常（当遇到 StopIteration 异常后，告知for的解释器，结束循环）
#for item in Iterable sequence:
#    do something

'''iter()  next()'''
list7 = [1,2,3,4,5] #对于可迭代对象
iter_l7 = iter(list7) #iter() 函数获取可迭代对象的迭代器
next(iter_l7) #使用next()函数来获取可迭代对象的下一个元素
next(iter_l7)
next(iter_l7)
next(iter_l7)
next(iter_l7)
#next(iter_l7) #产生StopIteration异常

#迭代类似于1-100的数字，可使用range(),其中 range()返回一个可迭代对象，不是列表；list()函数可以把返回的对象转为一个列表
#range(start,stop,step)  start/step缺省，start默认为0，step默认为1
print(range(5))
print(list(range(5)))
range(5) # 范围[0,5)
range(1,7) #范围[1,7)
range(1,7,2) #在[1,7)以2为步长提取数据

"""break"""
# 用于while循环和for循环，常常放在if语句中
# Once the break statement is executed, the entire loop will end immediately.
"""continue"""
#常放在if语句中，基于if语句中的条件终止当前循环，进入到下一循环

"""loop nesting"""
#The Python language allows a loop to be nested inside another loop.
#The nesting level is generally no more than 3 levels to ensure readability

"""Common Algorithms and Application Cases"""

# Find the approximate value of the natural logarithm e
#      This is a convergent series(收敛级数) that can be approximated by summing its first n terms前n项.
#      But where the calculation is, that is, how much is n to end the calculation......
#          This involves a calculation error(计算误差) problem.
#      We can set the calculation to stop when the value of the nth item第n项 is less than 10-5
print()
def factorial(x):
    s = 1
    for i in range(1,x+1):
        s = s*i
    return s
e = 0
for i in range(1000):
    a = 1/factorial(i)
    e = e + a
    if a < 10**(-5):
        break
print('e的近似值为',e)
#老师方法
i = 1
p = 1
sum_e = 1
t = 1 / p
while t > 0.00001:  # 误差判断
    p = p * i  # 计算 i 的阶乘
    t = 1 / p  # 计算 第 i 项，也是误差
    sum_e += t  # 累加
    i += 1
print("自然对数e的近似值", sum_e)

# Find the largest of 10 random integers in the interval [100, 200]
"""random"""
#生成0到1之间的随机浮点数‌：使用random.random()函数。
#‌在指定范围内生成随机浮点数‌：使用random.uniform(a, b)函数，其中a是下限，b是上限。
#生成指定范围内的随机整数‌：使用random.randint(a, b)函数，其中a是下限，b是上限。
#‌生成指定范围内的随机整数，可设置步长‌：使用random.randrange(start, stop[, step])函数，可以设置步长。
#从列表中随机选择一个元素‌：使用random.choice(sequence)函数，其中sequence是输入的列表或元组。
#从列表中随机选择多个不重复的元素‌：使用random.sample(population, k)函数，其中population是输入的列表或元组，k是要选择的元素数量。
print()
s = []
for i in range(10):
    x = random.randrange(100,201)
    s.append(x)
print('10 random integers in the interval [100, 200] is',s)
print('the largest of 10 random integers in the interval [100, 200] is',max(s))
#老师方法
x = random.randrange(100, 201) # 产生一个[100, 200]之间的随机数 x
maxn = x                      # 设定最大数
print(x, end = " ") # 输出不换行
for i  in range(2, 11):
    x = random. randrange(100, 201)  # 再产生一个[100, 200]之间的随机数 x
    print(x, end = " ")
    if x > maxn :
        maxn = x            # 若新产生的随机数大于最大数，则打擂成功，变新擂主
print ("\n最大数：", maxn)

# Buy 100 chickens for 100 yuan (enumeration 枚举算法)
#公鸡每只5元，母鸡每只3元，小鸡3只1元
# a + b + c =100
# 5*a + 3*b + c/3 = 100
print()
for a in range(21):
    if 100 - 5*a < 0 and 100 - a < 0:
        continue
    for b in range(34):
        if 100 - 5*a - 3*b < 0 and 100 - a -b < 0:
            continue
        for c in range(34):
            if 100 - 5*a - 3*b - c < 0 and 100 - a -b - 3*c < 0:
                continue
            sum_money = 100 - 5*a - 3*b - c
            sum_num = 100 - a -b - 3*c
            if sum_money == 0 and sum_num == 0:
                print('公鸡：',a,'母鸡：',b,'小鸡：',3*c)
#老师方法
for x in range(0, 100):
    for y in range(0, 100):
        z = 100 - x - y
        if z >= 0 and 5*x + 3*y + z/3 == 100 : #不用担心z为小数问题。x、y、100为整数，z/3必为整数
            print ("公鸡%d只，母鸡%d只，小鸡%d只" % (x, y, z))

# Output the first 20 terms of the Fibonacci sequence (递推算法)
#利用递推算法或迭代算法，可以将一个复杂的问题转换为一个简单过程的重复执行。
#这两种算法的共同特点是，通过前一项的计算结果推出后一项。
#不同的是，递推算法不存在变量的自我更迭，而迭代算法则在每次循环中用变量的新值取代其原值
f1 = 1
f2 = 1
fibonacci = [1,1,]
for i in range(18):
    f3 = f1 + f2
    f1 = f2
    f2 = f3
    fibonacci.append(f3)
print('the first 20 terms of the Fibonacci sequence is',fibonacci)

# Find the square root of the variable a（迭代算法）
x = int(input('输入需要求平方根的数：'))
while 1:
    p = random.uniform(1,x)
    if abs(x - p**2) < 10**(-5):
        print(f'{x}的平方根为{p}')
        print("%d 的平方根为 %f" % (x,round(p,3)))
        break
#缺点:精度不高，若高，程序运行缓慢；适于保留3位小数
#老师方法
#   Calculation formula for square root using iterative algorithm：x(n+1) = ( x(n) + a / x(n) ) / 2
#   分析：
#     （1） Set an initial value x0  (eg x0 = a/2)
#     （2）Use the formula to calculate x1, then x1 must be very different from the real square root.
#     （3）If the error is greater than 10-5, use x1 as x0, and re-calculate x1 until the error is less than 10-5
a = int(input("Input a positive number: ")) # Input a positive number
x0 = a / 2 # take an initial value
x1 = (x0 + a / x0) / 2
while abs(x1 - x0) > 0.00001 : # Determine whether the error is less than 10-5
    x0 = x1
    x1 = (x0 + a / x0) / 2
print("The square root is：", x0)