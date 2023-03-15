# use map to multiply all these numbers by 2

numbers = [1,2,3,4,5]

print(list(map(lambda x: x * 2, numbers)))

# user filter to list all of the even numbers

print(list(filter(lambda x: x % 2 == 0, numbers)))

# use reduce to multiply all numbers together

from functools import reduce

print(reduce(lambda total, x: total * x, numbers, 1))