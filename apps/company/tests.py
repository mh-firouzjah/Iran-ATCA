import random
from pprint import pprint

# from django.test import TestCase

# Create your tests here.

rows = 4
cols = 4
mat = [[0 for col in range(cols)] for row in range(rows)]
tuples = [(row, col) for col in range(cols) for row in range(rows)]
string = '134862'
print('\n'.join([' '.join([str(cell) for cell in row]) for row in mat]))
print('----------------------')
for item in string:
    indexes = tuples.pop(random.choice(range(len(tuples))))
    mat[indexes[0]][indexes[1]] = int(item)

print('\n'.join([' '.join([str(cell) for cell in row]) for row in mat]))

# import numpy as np

# s = '991234567'

# arr = np.array([int(i) for i in s] + [0] * (16 - len(s)))
# np.random.shuffle(arr)
# print(arr.reshape((4, 4)))
