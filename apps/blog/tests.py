# from django.test import TestCase

# Create your tests here.


def jaigasht(n, r):
    import math
    return math.factorial(n) / math.factorial(abs(n-r))


def func(n):
    from itertools import product
    room2 = list(product(
        [i for i in range(n+1)], repeat=2))
    del_room = []
    for item in room2:
        if item[0]+item[1] != n:
            del_room.append(item)
            f = 'sdfa'
    for item in del_room:
        room2.remove(item)
    return room2


print(len(func(1)))
print(len(func(2)))
print(len(func(3)))
print(len(func(5)))
print(func(1))
print(func(2))
print(func(3))
print(func(5))
