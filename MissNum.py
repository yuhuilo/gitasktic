def find_missing(lst):
    return[x for x in range(min(lst), max(lst)+1)
           # return [x for x in range(lst[0], lst[-1]+1)
           if x not in lst]


# Driver code
lst = [1, 2, 6, 4, 12, 9, 10]
print(find_missing(lst))

lst2 = [1, 2, 10]
print(find_missing(lst2))
