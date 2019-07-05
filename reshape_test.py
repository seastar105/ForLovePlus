import numpy as np

a = np.array([i for i in range(1,101)])
b = a.reshape(5,5,4)[:,:,-2::-1]
print(a)
print(b)