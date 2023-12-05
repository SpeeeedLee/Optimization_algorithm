import random
import numpy as np


X = np.random.randint(2, size=(15))
print(X)


X_parent_1 = X[:8]

print(X_parent_1)

X_parent_1 = X_parent_1 + X_parent_1[::-1]

print(X_parent_1)

X_parent_1 = np.concatenate((X_parent_1, X_parent_1))
print(X_parent_1)
