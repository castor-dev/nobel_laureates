# put your python code here
n_list = input().split()
x = input()
x_indexes = []
i = 0

for n in n_list:
    if n == x:
        x_indexes.append(str(i))
    i+=1

if len(x_indexes) == 0:
    print('not found')
else:
    print(" ".join(x_indexes))

