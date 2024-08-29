from django.test import TestCase

A = {'a': 0, 'b': 1}

B = [1, 2, 3]

if 1 in B:
    print(B.values() == 1)