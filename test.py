from sortedcontainers import SortedKeyList
import numpy as np

# SortedKeyList sorts in an ascending order
un_sorted = [1,2,3,4,5]
sorted = SortedKeyList (un_sorted, key = lambda x : -x)
print(sorted)

# does slicing has a permanent effect on list?
init_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(init_list [2:])
print(init_list)

# does SortedKeyList remain sorted after changing key? no
dict = {"hello" : 1, "world" : 2}
list = ["world", "hello"]
sorted_list = SortedKeyList(list, key = lambda x : dict[x])
print(dict)
print(sorted_list)

dict["hello"] = 3
print(dict)
print(sorted_list)

# but you can remove that specific element whose key has changed and then reappend it into the list
sorted_list.pop(0)
sorted_list.add("hello")
print(sorted_list)

# broadcast and multiply element-wise
ones = np.ones((4,3))
another = [1,2,3]
ele_wise_mult = np.multiply(ones, another)
print(ele_wise_mult)


list = [[1,2], [3,4]]
array = np.array(list)
print(array)

list1 = list
list1.clear()
print(list1)