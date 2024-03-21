from sortedcontainers import SortedKeyList

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