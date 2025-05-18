"""基本知识：Input Output Import  Using Help"""

#input  默认string
# 如果需要输入整数或小数，则需使用int或float函数进行转换,将字符串转为整数再执行加法运行
x = input("Enter a number: ")
print(type(x))

#Output
"""print函数所有参数均可省略"""
print()
# 无参数时，print函数输出一个空行
#缩进
for i in range(10):
    print(i,' ',end='')
print()
print(123,'abc',45,'book') # 输出多个对象，对象之间默认空格分隔
#可用sep参数指定特定符号作为输出对象的分隔符号
print(123,'abc',45,'book', sep='#')
print('price'); print(100) #默认输出结尾，输出在两行
print('price',end='='); print(100)#指定输出结尾，输出在一行
print()
#注释(文档字符串)
def add(a,b):
    """Hello,world!"""
    print(a+b)
    #return a+b
"""In[1]:add.__doc__"""
"""文档字符串是包、模块、类或者函数里的第一个语句，可以通过对象的 _ _doc_ _ 成员自动提"""

#import
import math
print(math.sin(0.5))
import random
x = random.random()#获得[0.1]随机小数
y = random.randint(1,100) #获得[1,100]上的随机整数
print(x," ",y)

#导包顺序，避免命名混乱,包的覆盖  内嵌-->第三方-->自己的
#自己命名sin变量，覆盖sin函数

"""内容过多，有多行内容，一行的最后用' \
    '换行或用('  '
'   ') 圆括号中的行会连接起来"""

# 因为 可变 不能当 key - value

#Using help
#查看内置函数和类型的帮助信息
help(max)
#查看模块中的成员函数信息
import os
help(os.fdopen)  # 查看os模块中的fdopen成员函数信息
#查看整个模块的信息
import math #查看前，注意先import导入该模块
help(math) #查看math整个模块的帮助信息
dir(math) #查看数学模块包含的内容
