import sys

i = 1
test = ' '
while i<501:
    test = '1' + test
    i += 1
print(sys.getsizeof(test))