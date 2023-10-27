import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
import math

MAX = 100

data = np.array(pd.read_excel(io="./data.xlsx")).transpose()
U_0 = data[10][0]
des_U = data[11][0]
f_0 = data[9][0]
s = int(data[12][0])
e = int(data[13][0])
L = data[6][0]
C = data[7][0]
R = data[8][0]
# 拟合
model = make_interp_spline(data[0][s:e], data[1][s:e])
xs = np.linspace(data[0][s], data[0][e - 1], 5000000)
ys = model(xs)

l_min = MAX
r_min = MAX
l = 0
r = MAX
flg = 1
for i in range(len(xs)):
    if ys[i] > U_0 - 0.1:
        flg = 2
    if flg == 1 and abs(des_U - ys[i]) < l_min:
        l_min = abs(ys[i] - des_U)
        l = i
    if flg == 2 and abs(des_U - ys[i]) < r_min:
        r_min = abs(ys[i] - des_U)
        r = i
print("des_u", des_U)
print("f(x)", ys[l], ys[r])
print("x", xs[l], xs[r])
print("Q", f_0/(xs[r] - xs[l]))
print("Q_the", math.sqrt(L*C)/(R*C))

plt.figure(1)
l1 = plt.plot(data[0], data[1], label="U-f")
plt.legend(handles=l1)
plt.show()
plt.figure(2)
l2 = plt.plot(data[0], data[3], label="real phi-f")
l3 = plt.plot(data[0], data[4], label="theorem phi-f")
plt.legend(handles=l2 + l3)
plt.show()
