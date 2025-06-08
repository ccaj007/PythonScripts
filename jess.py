from collections import Counter

name = ['ball', 'bat', 'glove', 'glove', 'glove']
price = [2, 3, 1, 2, 1]
weight = [2, 5, 1, 1, 1]

def numDuplicates(name, price, weight):
    products = zip(name, price, weight)
    return sum(count for item, count in Counter(products).items() if count > 1)

duplicates = numDuplicates(name, price, weight)
print(duplicates)




