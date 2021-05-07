#!/usr/bin/env python
# coding: utf-8

iter = [0,1,2,4,5,6]
def miss_num_func():
    return [x for x in range(iter[0], iter[-1]+1)
                                if x not in iter]

print(miss_num_funct(iter))
