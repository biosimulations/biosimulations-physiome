# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#
# A = np.array([[6, 1, 1],
#               [4, -2, 5],
#               [2, 8, 7]])
#
# A_inverse = np.linalg.inv(A)
# # print(A_inverse)




B = np.array([[1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0],
              [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
              [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
              [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
              [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
              [0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0],
              [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0],
              [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
              [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
              [0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0]])

# [0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0]
# [0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0]

BT = B.T


C = np.dot (BT,B)
# print(C.shape)

# print(C)


#forward and reverse kinetic rates from the original model
Y = np.log(np.array([[100],
                          [5000],
                          [562],
                          [61],
                          [5000],
                          [100],
                          [100],
                          [19800],
                          [135],
                          [1247],
                          [19800],
                          [100],
                          [1],
                          [1]]))
D = np.dot(BT,Y)
# print(D.shape)
sol = np.dot(np.linalg.pinv(C),D)
# print(sol.shape)
# print(sol)

# print(np.linalg.matrix_rank(C))
#
# # print(kinetic_rates)
# # #
# solution = kinetic_rates @ B_inv
# #
print("solution: ")
print(np.exp(sol))

