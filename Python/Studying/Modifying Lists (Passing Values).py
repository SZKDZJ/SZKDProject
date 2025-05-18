list1 = [1,2,3,4]
list2 = list1[:]
print(id(list1))
print(id(list2))


print(list1)
for i in range(len(list1)):
    print(id(list1[i]))
print(list2)
for i in range(len(list2)):
    print(id(list2[i]))

for i in range(4):
    if id(list1[i]) == id(list2[i]):
        print('True')
    else:
        print('False')

for i in range(4):
    list2[i] = i+2
    print(id(list2[i]))

for i in range(4):
    if id(list1[i]) == id(list2[i]):
        print('True')
    else:
        print('False')