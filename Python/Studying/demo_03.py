"""基本知识：序列类型 List Tuple Dictionary Set"""

#序列类型 sequence 字符串是其中一种  按整数顺序排列的数据
#从0开始索引；切片；len函数；“+”连接；“*”重复多次；"in"判断是否存在

#复合型数据类型  list tuples dictionaries字典 sets集合
#list tuples String 有序  输入输出是一个顺序
#dictionaries字典 sets集合 无序 输入是一个顺序，输出乱序


"""List"""
print()
print('Lists'.center(50))
print()
#list
list1=['Severus','Snape','Draco','Malfoy']
print(list1[0])#取索引
print(list1[1:6])#切片访问  多出来，不报错
print(list1[-1])#倒序访问  因为要求start<end
print(list1[-4:-2])
#改list
list1[2] = 'lucius'
print(list1)
#增加list
list1.append('Malfoy')# 使用列表的append()方法，增加元素至列表尾部
list1.insert(4,'Draco') # 使用列表的insert()方法，增加元素至列表指定位置
print(list1)
#删除list
del list1[2] # 使用Python内置函数del，删除列表指定元素
print(list1)
s = list1.pop(0)  # 可以使用pop() 来删除列表中任何位置的元素
print(s)
print(list1)# 每当使用pop()时，被弹出的元素就不再在列表中了
list1.remove('Malfoy')# 使用方法列表的remove()方法来删除指定值的元素
print(list1)  #方法remove() 只删除第一个指定的值。如果要删除的值可能在列表中出现多次，就需要使用循环来判断是否删除了所有这样的值。

#Making Numerical Lists
list(range(10)) #range(stop)
list(range(0, 30, 5))#range(start, stop[, step])
list(range(0, -10, -1))

#多维列表 嵌套列表  类似矩阵 但可以任意维，矩阵不可以
list2 = [['Gr']]
# 多一个索引来访问某个元素
matrix1 = [[[1,2], [2,4], [5,6], [3,4]],[[5,7], [6,8], [7,8], [10,11]]]
print('多维列表索引',matrix1[0][2][1])

#List comprehensions
matrix2 = [ [0 for col in range(6)] for row in range(3)]
print(matrix2)
squares = [x ** 2 for x in range(10)] #
# variable = [out_exp_res for out_exp in input_list if out_exp == 2]
multiples = [i**2 for i in range(30) if i % 3 == 0]

# List Operator
print([1,2,3]+[4,5,6]+[7,8,9]) #list combination (列表组合)
print([122]*3) #list repeats (列表重复)
print(3 in [1,2,3])  #List member operations  (元素是否存在于列表中)
#iterative operation (迭代操作)
for x in [1,2.3]:
    print(x,end=' ')

#Built-in functions for list
# len(list) Return the length (the number of items) of a list
len([1, 2, 3, 4, 5])
# max(list) Return the largest item in an iterable (list)
max([1, 2, 3, 4, 5])
# min(list) Return the smallest item in an iterable (list)
min([1, 2, 3, 4, 5])
#list(seq)  Convert other sequence type data to list
list((1, 2, 3, 4, 5))#[1, 2, 3, 4, 5]
list({1, 2, 3, 4, 5})#[1, 2, 3, 4, 5]
list({'a':1, 'b':2, 'c':3})#['a', 'b', 'c']

# Methods of list
list2 = [0,2,1,3,4]
#list.append(obj) 在列表末尾添加新的对象
list2.append(5)
#list.insert(index, obj) 将对象插入列表指定位置
list2.insert(1,'a')
#list.extend(seq) 在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
list3 = ['A','B','C']
list2.extend(list3)
#list.pop(index) 移除列表中的某个元素（无参数，则默认移除最后一个元素），并且返回该元素的值
list2.pop(0)
#list.remove(obj) 移除列表中某个值的第一个匹配项
list2.remove('A')
#list.sort([func]) 对原列表进行排序
# list 的 sort 方法返回的是对已经存在的列表进行操作，而内建函数 sorted 方法返回的是一个新的 list，而不是在原来的基础上进行的操作。
list4 = [2,3,10,2,44]
list4.sort() #隐含比较操作，列表中只能有一种数据类型
list4.sort(reverse=True)
list5=sorted(list4)
#list.reverse() 反转列表中元素顺序
list2.reverse()
#list.index(obj) 从列表中找出某个值第一个匹配项的索引位置
list2.index(5)
#list.count(obj)统计某个元素在列表中出现的次数
list2.count(6)

# Copying a List 正确拷贝
# 区别   friend_foods = my_foods[:] 和  friend_foods = my_foods
list6 = list2[:]


"""Tuple"""
print()
print('Tuple'.center(50))
print()
#Tuples  几乎不可改变 常量def为Tuples   不支持某一项赋值
#定义
person = ('JLY', 'Female', 160, 50)
Options = "a", "b", "c", "d"
tup_empty = ()
tup_1 = (50,)

#访问
print(person[0])  # output the first element of the tuple
print (Options[0:2]) # slice operation
print (Options[1:]) # slice to the last element

#Join
tup1 = (12, 34, 56)
tup2 = (78, 90)
tup3 = tup1 + tup2  # Concatenate tuples to create a new tuple
print(tup3)
tup4 = tup1 * 2  # output tuple twice
print(tup4)

#不可变性
tup1 = (12, 34, 56)
#tup1[0] = 100
# TypeError: 'tuple' object does not support item assignment
#Although you can’t modify a tuple, you can assign a new value to a variable that represents a tuple.
tup1 = (78, 90)
print (tup1)
#可变的Tuples  里面定义了一个可改变的元素，就可以改变、添加
tup = [['Severus','Snape','Draco','Malfoy'],'Lucius','Malfoy']
tup[0][1] = '1' # Modify the value of the first element in the tuple
print(tup)
tup[0].append('4') # Modify the value of the first element in the tuple again
print(tup)

person = ('JLY', 'Female', 160, 50)
#del person[3]
# TypeError: 'tuple' object doesn't support item deletion
print(person)
del person # you can use the del statement to delete the entire tuple
#print(person)

# Tuples Operator
tup3 = (1, 2, 3) + (4, 5, 6)#tuple combination (元组组合)
tup4 = ('Hi!',) * 4 #tuple repeats (元组重复)
print(3 in (1, 2, 3)) # tuple member operations  (元素是否存在于元组中)
for x in (1, 2, 3):
    print(x, end=" ") #iterative operation (迭代操作)

#Built-in functions for tuples
#len(tuple)
len((1, 2, 3, 4, 5))#Return the length (the number of items) of a tuple
#max(tuple)
max((1, 2, 3, 4, 5)) #Return the largest item in an iterable (tuple)
#min(tuple)
min((1, 2, 3, 4, 5))#Return the smallest item in an iterable (tuple)
#tuple(seq)   Convert other sequence type data to tupl
tuple([1, 2, 3, 4, 5])
tuple({1, 2, 3, 4, 5})
tuple({'a':1, 'b':2, 'c':3})

# You can use tuples to assign values to multiple variables at once
(x, y, z) = (1, 2, 3)
a, b, c = 3, 4, 5
#可直接交换值
x, y = y, x

#strings, lists和tuples之间的转换
nums_L = [1, 3, 5, 7, 8, 13, 20]
nums_T = tuple(nums_L)
nums_S = str(nums_T)


"""Dictionary"""
print()
print('Dictionary'.center(50))
print()
#Dictionaries   a standard mapping type 映射类型
# { key1:value1, key2:value2 }
# key must be unique   value can be any type of data, and does not need to be unique
#  mutable(可变的) types may not be used as keys. 例如，List/Dictionary
#  key(可以是): 数值numbers String Tuple

#Create a Dictionary
stu1 = {'SN': 20234987, 'Name': 'Jelly', 'Score': 98}
info_dict = {'Name': 'xmj', 'Age': 17, 'Name': 'Manni'} #后name覆盖前面的
# Accessing Values in a Dictionary
print(stu1['Name'])
# print(stu1['Age'])#key 不存在 报错： NameError: name 'Age' is not defined
v = stu1.get('Age')
print(v) #使用get方法，尽管key不存在，不报错，返回None
# Adding New Key-Value Pairs
print(stu1)
stu1['Age'] = 19
print(stu1)
# Modifying Values in a Dictionary
stu1['Score'] = 100
print(stu1)
# Removing Key-Value Pairs
del stu1['Name'] # del statement to completely remove a key-value pair
print(stu1)
stu1.clear() # Empty all elements of the dictionary
print(stu1)
del stu1  # Delete the dictionary, the dictionary does not exist
#print(stu1)  #报错：NameError: name 'stu1' is not defined
# Break a larger dictionary into several lines
stu2 = {
    'Name':'Helen',
    'SN':20231000,
    'Math Score':120,
    'English Score':90,
}    #可以在最后一个键值对后加上"," 以便准备添加新的键值对

#Pyhthon 有几种遍历整个 Dictionary 的方式，遍历key-value pairs/遍历keys/遍历values
#                           Looping Through All Key-Value Pairs
# items() method 将在字典中的每个键值对形成一个元组Tuple，并返回这些元组
print()
print(stu2)
print(stu2.items())
#So
#for key, value in stu_dict.items():
#    print(key, value)
for k,v in stu2.items():
    print(f'\nKey: {k}')
    print(f'Value: {v}')
print()
#                          Looping Through All the Keys in a Dictionary
# keys() method 将在字典中所有key值形成一个列表，并返回这个列表
print(stu2.keys())
#So
#for key in stu_dict.keys():
#    print(keys)
# 但是，遍历字典时，会默认遍历所有的键(Key)，所以不用keys()方法也可以
# 可是，显式使用keys()方法，可以让代码更容易理解。
print()
for k in stu2:
    print(k)
print()
for k in stu2.keys():
    print(k)
print()
#还可以使用keys() 确定某个人是否接受了调查
favorite_languages = {
 'jen': 'python',
 'sarah': 'c',
 'edward': 'ruby',
 'phil': 'python',
}
if 'Helen' not in favorite_languages.keys():
    print("Please take our poll!")
print()
for language in favorite_languages.values():
    print(language.title())
print()
# 由于字典中的value值是可以重复的，所以为了去重，可以使用set()方法，将list转换为set，自然就去重了
for language in set(favorite_languages.values()):
    print(language.title())

"""Set"""
print()
print('Set'.center(50))
print()
# Sets  an unordered无序的 collection集合 of distinct不同的 hashable不可变的 objects 可哈希的对象
# 用途： membership testing/ removing duplicates from a sequence去重/ computing mathematical operations 交集、并集、差集、对称差集
# Create a Set
# Use a comma-separated list of elements within braces
Set1 = {'Tom', 'Jim', 'Mary', 'Tom', 'Jack', 'Rose'}
# Use the type constructor set()
Set2 = set() #创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典
Set3 = set('foobar')
Set4 = set(['a', 'b', 'foo'])
# Use a set comprehension
Set5 = {x for x in 'abracadabra' if x not in 'abc'}
print(Set5)

#Set Operator
s1 = {'a','b','c'}
s2 = {'a','b','c','d','e','f','g','h','i','j'}
s3 = {'a','b','c','d','e','f','g','h','i','j'}
s4 = {'d','e','f','g','h'}
# issubset(other)测试set与other的子集、超集关系
print(s1<=s2) #是否s1是s2子集 <-> s2是s1超集
print(s2<s3) #是否s2是s3真子集
print(s1.issubset(s2))
print(s2.issuperset(s3))
print('a' in s1) # s1是否包含元素a
print('b' not in s2) # 有 not in
# union, intersection, difference, symmetric_difference并、交、差、对称差集
# set | other | ... Return a new set with elements from the set and all others.
s5 = s1 | s4
print(s5)
# set & other & ... Return a new set with elements common to the set and all others
s6 = s1 & s2
print(s6)
# set - other - ... Return a new set with elements in the set that are not in the others.
s7 = s2 - s1
print(s7)
#  set ^ other Return a new set with elements in either the set or other but not both
s8 = s1 ^ s2
print(s8)

# Built-in functions for sets
#len(set)
#Return the number of elements in set s.
#max(set)
#Return the largest item in an iterable (set )
#min(set)
#Return the smallest item in an iterable (set )
#set(stu2)
#Convert other sequence type data to set
print(set(stu2))

#Methods of Sets
# set.add(elem)
# Add element elem to the set.
s1.add('z')
# set.remove(elem)
# Remove element elem from the set. Raises KeyError if elem is not contained in the set.
#s1.remove('y') #报错
# set.discard(elem)
# Remove element elem from the set if it is present.
s1.discard('a')
# set.pop()
#随机删除 Remove and return an arbitrary element from the set. Raises KeyError if the set is empty空集合.
s10 = s1.pop()
print(s10)
# set.clear()
# Remove all elements from the set.
s1.clear()
# set.copy()
# Return a shallow copy of the set.
s9 = s2.copy()
print(s9)
# set.isdisjoint(other)
# Return True if the set has no elements in common with other. Sets are disjoint if and onlyif their intersection is the empty set
print(s4.isdisjoint(s2))

"""Comprehensions"""
print()
# A comprehension is a structure that can construct a new sequence data from a sequence data.
# There are three types of Comprehensions：

# List Comprehensions（列表推导式）
#variable = [out_exp_res for out_exp in input_list if out_exp == 2]

# dict Comprehensions（字典推导式）
mcase = {'a': 10, 'b': 34, 'A': 7, 'Z': 3}
mcase_freq = {
    k.lower(): mcase.get(k.lower(), 0) + mcase.get(k.upper(), 0) # 键值对生成元素表达式
    # get方法访问一个不存在的键时，没有异常，返回None，也可以指定一个返回的默认值。这里就是返回0
    for k in mcase.keys()  #迭代 mcase 中的 key-->k，将 k 传入上面的键值对生成表达式中
    if k.lower() in ['a','b'] # # 根据条件过滤元素
}
print(mcase_freq)

# set Comprehensions（集合推导式）
squared = {x**2 for x in [1, 1, 2]} #虽然迭代 list[1,1,2] 给 x 有三个值，但是最终生成集合类型数据，是没有重复数据的，所以少了一个 1
