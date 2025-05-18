#Geometry Manager

"""The Pack Geometry Manager"""
# block method, in generation order, fast, common
# syntax：component_object.pack (<option>)
import tkinter as tk

root = tk.Tk()
w = tk.Label(root, text="Red Sun", bg="red", fg="white")
w.pack(fill = 'x')
w = tk.Label(root, text="Green Grass", bg="green", fg="black")
w.pack(fill = 'x')
w = tk.Label(root, text="Blue Sky", bg="blue", fg="white")
w.pack(fill = 'x')
root.mainloop()

"""The Grid Geometry Manager"""

import tkinter as tk
root = tk.Tk()
root.geometry('200x200+280+280')
root.title('计算器示例')
color = ('green', 'yellow') # 定义背景色
for Bi in range(1, 10):
    Li = tk.Button(root, text=str(Bi), width=5, bg=color[Bi%2])
    Li.grid(row=(Bi-1)//3, column=(Bi-1)%3) # Grid 网格布局
L0 = tk.Button(root, text='0')
#L0.grid(row = 3, column = 0, columnspan=2, sticky=E+W )# 跨两列
Lp = tk.Button(root, text='.')
#Lp.grid(row = 3, column = 2, sticky=E+W ) # 左右贴紧
root.mainloop()





import json

#连接文本
#写文件  with 关键字恰当时候关闭文件
#with open("D:\\AaStudying\\a软件工程\\python\\Word_List.txt","a") as Word_List:
#    Word_List.write("hogwarts\n")
#读文件,Making a List of Lines from a File
with open("D:\\AaStudying\\a软件工程\\python\\Word_List.txt") as Word_List:
    fileLines = Word_List.readlines()
for fileLine in fileLines:
    print(fileLine)

#处理异常
"""try:
    print(5/0)
except ZeroDivisionError:
    print("You can't divide by zero!")
    """

#存储用户
filename = 'users.json'
try:
    with open(filename) as f_obj:
        username = json.load(f_obj)
except FileNotFoundError:
    username = input("What is your name? ")
    with open(filename, 'w') as f_obj:
        json.dump(username, f_obj)
    print("We'll remember you when you come back, " + username + "!")
else:
    print("Welcome back, " + username + "!")