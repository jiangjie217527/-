import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from math import pi,sqrt

mu_0 = 4 * pi * 1e-7
L = 0.24
D_in = 0.09
D_out = 0.1
D = (D_in + D_out) / 2
l = 0.199
l_mid = 0.107
U_1 = [850, 900, 950]
x_0 = l / 2
data = np.array(pd.read_excel(io="./data.xlsx")).transpose()
N=data[0][0]

K = L**2 * 1e14/(2 * (sqrt((D/2)**2+(L/2+x_0)**2)-sqrt((D/2)**2+(L/2-x_0)**2))**2) # left n to the next formula

def cal_ans_1(n,U_a,I):
    return K*n**2*U_a/(N*I)**2


def cal_B(I):
    return 1/(2 * x_0) * mu_0 * N / L * I * (sqrt((D/2)**2+(L/2+x_0)**2)-sqrt((D/2)**2+(L/2-x_0)**2))


def cal_ans_2(I,theta,U_a):
    return 8 * U_a / l_mid**2 * ( theta / cal_B(I) )**2


def cal_l_3(I,theta,U_a,Xans):
    return sqrt(8 * U_a / Xans * ( theta / cal_B(I) )**2)



def cal_I_i(n):
    tmp = 0
    for i in data[n]:
        tmp += i
    return tmp/12
print("根据wiki,算出来1.7588e11是比较准确的")
print("method 1:")
ans_1 = []
for i in range(3):
    I = (cal_I_i(3 * i + 1)+cal_I_i(3 * i + 2)+cal_I_i(3 * i + 3))/6
    ans_1.append(cal_ans_1(1,850 + i * 50,I))
    print("在电压",850 + i * 50,"下，算得荷质比",ans_1[-1])


print("method 2:")
ans_2 = []
for i in range(10,16):
    I = 0
    for j in data[i]:
        I += j
    I /= 6
    ans_2.append(cal_ans_2(I,pi/2**(2-(i-10)%3),850 if (i - 10) % 6 < 3 else 950))
    print("在pi /",2**(2-(i-10)%3),"角度",850 if (i - 10) % 6 < 3 else 950,"电压",I,"平均电流","下算得荷质比",ans_2[-1])
Xans = np.mean(ans_2)
print("X方向结果平均值为",Xans)

l_mid_y = []
for i in range(16,22):
    I = 0
    for j in data[i]:
        I += j
    I /= 6
    l_mid_y.append(cal_l_3(I,pi/2**(2-(i-10)%3),850 if (i - 10) % 6 < 3 else 950,Xans))
    print("在pi /",2**(2-(i-10)%3),"角度",850 if (i - 10) % 6 < 3 else 950,"电压下有",I,"平均电流")

print("在y方向测得y偏转板中间位置到荧光屏距离约为",np.mean(l_mid_y))
