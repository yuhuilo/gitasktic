#!/usr/bin/env python
# coding: utf-8

<<<<<<< HEAD
<<<<<<< HEAD
iter = [0,1,2,4,5,6,8,9]
=======
#I sure hope this works
iter = [0,1,2,4,5,6]
>>>>>>> revertime
=======
iter = [0,1,2,4,5,6,8,9]
>>>>>>> ea535d5f2d362128422ecd2c4fdbf48f6b846149
def miss_num_func():
    return [x for x in range(iter[0], iter[-1]+1)
                                if x not in iter]

print(miss_num_funct(iter))
