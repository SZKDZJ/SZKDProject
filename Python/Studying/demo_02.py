"""基本知识：Numbers Strings 赋值"""

#数值类型
# 数值类型的数据是不允许改变的。即，如果改变数值类型数据的值，将重新分配内存空间,原本的数值还在原来分配的内存空间里

c = 1
print(id(c))
c = 2
# 1 还在 第一个id(c) 的地址
print(id(c))
print()
#int  不限制大小
#运算  基本一样
#整数除法  m//n 整除，抛弃余数；m/n 小数；m%n 求余数；divmod(m,n) 得到两个整数：整数除法和余数
# m**n 幂；abs(m) 绝对值
#大小比较 一样；允许连续比较 7>3>=3 True  7<22<10 False
# <> （a<>b）is True    if the values are not equal the result is True
#数的进制：无前缀 decimal；0b前缀 binary；0o前缀 octal；0x前缀 hexadecimal
print('int')
m, n=5, 2
print('5.0//2.0=',5.0//2.0)
print('5/2 =',m/n)
print('divmod(m,n) =',divmod(m,n))
print('m**n =',m**n)
print('7 > 3 >= 3',7>3>=3)
print('7 < 22 < 10',7<22<10)
print('33 bin ',bin(33))
print('33 oct ',oct(33))
print('33 hex ',hex(33))

#float 浮点数 国际标准 17位小数 超过 科学计数法 有效位数
"""浮点数 进制转换导致精度误差；尽量避免== 用a-b小于一个非常小的数字，只要小于一个非常小的数字看作相等"""
print('0.2+0.1=',0.2+0.1)

#Imaginary复数类型 python内置
#支持常见数字  a+bj a、b为整数
#支持常见运算；(a+bj).imag 提取虚部；(a+bj).real 提取实部
#只能做相等比较，无大小判断
#abs(a+bj)取模；abs((a+bj)-(c+dj))两点距离

#数学模块 math 面向int float
#dir(math)查看数学模块包含的内容   引用pi math.pi
#cmath模块 面向复数
#模块包含：数学函数+复数在平面直角坐标和极坐标之间转换

#逻辑类型 bool  True/False
#配合if/while...
#逻辑运算 “与” and 同时成立--True；“或” or 只要一个成立--True; “非' not 写在逻辑值--True/False前面
#优先级 not>and>or 单目运算符 双目运算符
#各种类型对应的真值：int/float/复数 0--假 非0--真；字符串 空串""--假 非空串--真；序列类型(包含字符串) 空序列--假 非空序列--真；空值None 无意义--假
# list = []  Tuple = () Die = {} set()
print()
print('bool')
a = 'python'
print(a and True)
print(a or False)
print('' or True)


#字符串类型    字符串类型的数据也是不允许改变的。即，如果改变字符串类型数据的值，将重新分配内存空间。
#表示方法:单引号和双引号的灵活使用，能够让你在字符串中包含引号和撇号
"abc"
'abc'
"I told my mother’s friends,'Python is my favorite language'"
'''abc
def'''
"""abc
def"""
#转义符号"\" 特殊字符
'\n 换行''\v 纵向制表符 \t 横向制表符'
#字符的编号 从0开始，顺向编号；最后一个从-1开始，反向编号
#变量名称：第一个必须是文字，后面才可以数字
#获取字符串长度 len函数
#切片操作 slice  s[start:end:step]--":"隔开 “step"步长，以..跳开提取；取时包含“start"不包”ens"(前闭后开)
# + _将两字符串进行连接 * _将字符串重复若干次-->新字符串
#“==” “=”
#判断字符串是否包含某个字符串 '' in a    '' not in a
#删除空格 str.strip() 前后空格 str.lstrip() 前/左部空格 str.rstrip 后/右部空格  该方法不改变原变量值，如果要永久删除空白，需要为变量重新赋值
#判断字母数字 str.isalpha() 是否全字母 str.isdigit() 是否全数字 str.isalnum() 是否仅有数字和字母而没有特殊字符 eg + = -
#高级操作 split() 分割 join 合并 upper变大写/lower变小写/swapcase变成相反的(大->小，小->大)   ljust/centre/rjust 文本排版左中右对齐  replace 替换子串
#存储数据时，方法lower() 很有用。很多时候，你无法依靠用户来提供正确的大小写，因此需要将字符串先转换为小写，再存储它们。
#以后需要显示这些信息时，再将其转换为最合适的大小写方式。
# title() 方法以首字母大写的方式显示每个单词
print()
print('String')
print('abc'+'def')
print('abc'*3)
print('abc''def')
print(len('abc'))
print(len('峨眉'))
print(str.strip('      abc          '))
print(str.isalpha('abc'))

#取索引0的字符
S='Severus Snape'
print(S[0],' ',S[7])

# ord 单个字符在字符集里编号  chr 相反ord
print(ord('a'))
print(chr(11))

print('切片')
print(S[4:9:2])
print(S[0:6])

print('切割')
print('You are my sunshine.'.split(' '))
print('合并')
print('-'.join(['Love','You']))
print('大小写')
S = S.lower()
print(S)
print(S.title())
print('排版')
print('Severus Snape'.center(20),'aa')
print('替代')
print('Draco Malfoy'.replace('Draco','Lucius'))

#原始字符串 r R 输出转义字符
print(r'\n  prints  \n')

#String Formatted Output
#Python用一个元组将多个值传递给格式化的模板，每个值对应一个字符串格式符
print ("My name is %s, and my age is %d. " % ('jly', 41))

#f-strings
name = 'Severus'
working = 'Doctor'
phrase1 = f'His name is {name}.He is a {working}'
print(phrase1)

#先解析input 函数再替换
print(f'name: {input('Input name: ')} age: {input('Input age: ')} sex: {input('Input sex: ')}') # 甚至可以在 { } 中放入 input 函数，让用户输入


#type()--返回类型
#不用定义，用哪个类型的数值，变量就是哪个类型



#命名 赋值语句 <名字>=<数据> 名字：字母+数字 可有_  不能用特殊字符
#引用 名字和数值的关联    当定义变量a时，Python解释器做了两件事情：
#（1）在内存中创建了一个'ABC'的字符串；
#（2）在内存中创建了一个名为a的变量，并把它指向'ABC'
#名字 变量 variable 类型随数据类型变化而变化
#合并赋值
a = b = c = 1
#顺序依次赋值
d, e, f = 7,8,9
#简写赋值语句
p = 5
p /= 3 + 4
print('\n',p)

print("\n类型转换")
print('str(''abc'') =',str('abc'))
print('bool(''abc'') =',bool('abc'))
print('int(''5.566'') =',int(5.566))
print('float(''7'') =',float(7))
#判断 is None
#if ''is None:
    #print('False')
#else:
    #print('True')

#常量
# using all uppercase variable names to represent constants is just a habitual usage

