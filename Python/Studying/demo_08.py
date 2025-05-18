import numpy as np

# logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None, axis=0)
#在logspace中，起始位和终止位代表的是10的幂（默认基数为10）
print('使用 logspace 函数创建的等比数列数组为：\n', np.logspace(0, 2, 20))


"""2D arrays"""

# eye(N, M=None, k=0, dtype=<class 'float'>, order='C')
#类似单位矩阵
print('使用eye函数创建主对角为1的数组：\n', np.eye(3))

# diag(v, k=0)
print('使用diag函数创建类似对角的数组为：\n', np.diag([1, 2, 3 ,4]))

#vander(x, N=None, increasing=False)
#Vandermonde 矩阵的每一列都是输入一维数组或列表或元组的递减幂， 其中x最高多项式阶数为n-1
# 此数组创建有助于生成线性最小二乘模型
x = np.array([1, 2, 3, 5])
N = 3
print("Vandermonde矩阵:\n",np.vander(x, N))

x = np.array([1, 2, 3, 5])
np.vander(x)

x = np.array([1, 2, 3, 5])
np.vander(x, increasing=True)

"""ndarrays"""

# ones(shape, dtype=None, order='C'
print('使用ones函数创建元素皆为1的数组：\n', np.ones((5, 3)))

np.ones((2, 3, 2))

# zeros(shape, dtype=float, order='C')
print('使用zeros函数创建元素皆为0的数组：\n', np.zeros((2, 3)))

np.zeros((2,3,2))

""" Random sampling (numpy.random)"""

print('生成无约束条件的0-1之间的随机数组：\n', np.random.random(100))
print('生成服从均匀分布的随机数组：\n', np.random.rand(10, 5))
print('生成符合正态分布的随机数组：\n', np.random.randn(10, 5))
print('生成限定范围的随机整数数组：\n', np.random.randint(2, 10, size=[2, 5]))

# random.uniform(low=0.0, high=1.0, size=None)
np.random.uniform()
np.random.uniform(1, 5)
# 生成一维数组
np.random.uniform(1, 5, 4)
# 生成二维数组
np.random.uniform(1, 5, (4,3))

"""Replicating"""
# When you assign an array or its elements to a new variable,
# you have to explicitly(明确的) numpy.copy the array,  otherwise the variable is a view into the original array.
a = np.array([1, 2, 3, 4])
b = a[:2]
b += 1
print('a =', a, '\nb =', b)

a = np.array([1, 2, 3, 4])
b = a[:2].copy()
b += 1
print('a =', a, '\nb =', b)

a = [1, 2, 3, 4]
b = a[:2]
#b += 1  # Error
print('a =', a, '\nb =', b)

a = [1, 2, 3, 4]
b = a[:2]
b[0] += 1
b[1] += 1
print('a =', a, '\nb =', b)

# 从这个对比看出，numpy和python的区别，numpy自动迭代。list这种赋值就算是copy副本了，numpy不算。

"""Joining"""
#There are a number of routines to join existing arrays e.g. numpy.vstack, numpy.hstack, and numpy.block.
A = np.ones((2, 2))
B = np.eye(2, 2)
C = np.zeros((2, 2))
D = np.diag((-3, -4))
print(np.block([[A, B], [C, D]]))

"""Reading arrays from disk, either from standard or custom formats"""

# Common ASCII Formats
# ndarray --> ASCII file
arr = np.arange(100).reshape(10, 10)
np.savetxt("D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\arr.txt", arr, fmt="%d", delimiter=",")
# ASCII file --> ndarray
np.loadtxt("D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\arr.txt", delimiter=",")
# ASCII file --> ndarray
np.genfromtxt("D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\arr.txt", delimiter=",")

loaded_data = np.genfromtxt("D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\arr.txt", delimiter=",")
print('读取的数组为：\n', loaded_data)
loaded_data2 = np.genfromtxt("D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\arr.txt", delimiter=(4, 3, 2))
print('读取的数组为：\n', loaded_data2)

# Standard Binary Formats

# np.save(file, arr, allow_pickle=True, fix_ imports=True)
arr = np.arange(100).reshape(10, 10)    # 创建一个数组
print(arr)
# 保存数组，文件扩展名.npy自动添加
np.save("D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\save_arr", arr)

# np.savez('../tmp/savez_arr.npz', arr1, arr2
arr1 = np.array([[1, 2, 3], [4, 5, 6]])
arr2 = np.arange(0, 1.0, 0.1)
print('保存的数组1为：\n', arr1)
print('保存的数组2为：\n', arr2)
np.savez('D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\savez_arr', arr1, arr2)

#np.load("../tmp/save_arr.npy")
loaded_data = np.load("D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\save_arr.npy")    # 读取含有单个数组的文件
print('读取的数组为：\n', loaded_data)

# np.load("../tmp/save_arr.npz")
loaded_data1 = np.load("D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\savez_arr.npz")   # 读取含有多个数组的文件
print('读取的数组1为：\n', loaded_data1['arr_0'])
print('读取的数组2为：\n', loaded_data1['arr_1'])

# np.loadtxt("../tmp/arr.txt", delimiter=",")
loaded_data = np.loadtxt("D:\\AaStudying\\a软件工程\\python\\demo_08-Reading\\arr.txt", delimiter=",") # 读入的时候也需要指定逗号分隔
print('读取的数组为：\n', loaded_data)


"""higher dimensional arrays"""
