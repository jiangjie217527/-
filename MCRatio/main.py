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
# load data
# 计算方法1的荷质比
def cal_ans_1(n,U_a,I):
    return K*n**2*U_a/(N*I)**2

# 计算方法1结果的不确定度误差传递公式
def cal_delta_A_res_1(U_a,Delta_a,I):
    return 2*K*U_a/N**2/I**3*Delta_a


# 计算磁感应强度
def cal_B(I):
    return 1/(2 * x_0) * mu_0 * N / L * I * (sqrt((D/2)**2+(L/2+x_0)**2)-sqrt((D/2)**2+(L/2-x_0)**2))


# 计算方法2的荷质比
def cal_ans_2(I,theta,U_a):
    return 8 * U_a / l_mid**2 * ( theta / cal_B(I) )**2


# 计算方法2,x方向结果的不确定度误差传递公式
def cal_delta_A_res_2(Delta_a,theta,U_a,I):
    return 8 * U_a/ l_mid**2 *  theta**2 * 4 * x_0**2/(cal_B(I)**2)/I*Delta_a * 2


#计算方法2,y方向板长的不确定度误差传递公式
def cal_delta_A_res_3(Delta_a,theta,U_a,I,r):
    return sqrt(8*U_a/r)*theta/cal_B(I)/I*Delta_a


# 计算y板到荧光屏的长度
def cal_l_3(I,theta,U_a,Xans):
    return sqrt(8 * U_a / Xans * ( theta / cal_B(I) )**2)


# 计算一列的电流平均值
def cal_I_i(n):
    tmp = 0
    for i in data[n]:
        tmp += i
    return tmp/12


# 计算6个直接测量量的不确定度
def cal_Delta_A_6(n,x):
    ave = np.mean(x)
    tmp = 0
    for i in x:
        tmp += (ave - i)**2
    return 1.05*sqrt(tmp/(n-1))


print("根据wiki,算出来1.7588e11是比较准确的")
print("---------------method 1:-------------------------")
ans_1 = []
I_1 = [] # 每个电压下电流平均值
for i in range(3):
    I = (cal_I_i(3 * i + 1)+cal_I_i(3 * i + 2)+cal_I_i(3 * i + 3))/6
    I_1.append(I)
    ans_1.append(cal_ans_1(1,850 + i * 50,I))
    print("在电压",850 + i * 50,"下，算得荷质比",ans_1[-1])
print("平均值为",np.mean(ans_1))
# 以下为计算不确定度
Delta_A = [] # 不同电压下每次聚焦的不确定度
Delta_A_I_res = [] # 不同电压下电流的不确定度
Delta_A_MC = [] # 不同电压下结果的不确定度
Delta_A_MC_res = [] # 三个电压平均值最终结果的不确定度
for i in range(1,10):
    t_1 = cal_Delta_A_6(6,data[i][0:6])
    t_2 = cal_Delta_A_6(6,data[i][6:12])
    Delta_A.append(sqrt(t_1**2+t_2**2)/2)
    # print("电压",850+(int)((i-1)/3)*50,"下，正反、合并的不确定度为",t_1,t_2,Delta_A[-1])
    if (i%3)==0:
        print("电压为",850+(int)((i-1)/3)*50)
        ans = ans_1[(int)((i-1)/3)]
        Delta_A_I_res.append(sqrt(Delta_A[-1]**2+Delta_A[-2]**2+Delta_A[-3]**2)/6)
        Delta_A_MC.append(cal_delta_A_res_1(850+(int)((i-1)/3)*50,Delta_A_I_res[-1],I_1[(int)((i-1)/3)]))
        print("该电压下电流不确定度为",Delta_A_I_res[-1])
        print("结果不确定度为",Delta_A_MC[-1],"相对不确定度为",Delta_A_MC[-1]/ans)
t = 0
for i in range(3):
    t += Delta_A_MC[i]**2
print("总共不确定度为",sqrt(t)/3,"相对不确定度",sqrt(t)/3/np.mean(ans_1))
print("---------------method 2:-------------------------")
ans_2 = []
Delta_A_2 = []
Delta_A_res_2 = []
for i in range(10,16):
    I = 0
    for j in data[i]:
        I += j
    I /= 6
    ans_2.append(cal_ans_2(I,pi/2**(2-(i-10)%3),850 if (i - 10) % 6 < 3 else 950))
    print("在pi /",2**(2-(i-10)%3),"角度",850 if (i - 10) % 6 < 3 else 950,"电压",I,"平均电流","下算得荷质比",ans_2[-1])
    Delta_A_2.append(cal_Delta_A_6(6,data[i][0:6])*sqrt(2))
    Delta_A_res_2.append(cal_delta_A_res_2(Delta_A_2[-1],pi/2**(2-(i-10)%3),850 if (i - 10) % 6 < 3 else 950,I))
    print("算的结果不确定度和相对不确定度为",Delta_A_res_2[-1],Delta_A_res_2[-1]/ans_2[-1])
Xans = np.mean(ans_2)
t = 0
for i in range(6):
    t += Delta_A_res_2[i]**2
print("X方向结果平均值",Xans)
print("不确定度和相对不确定度为",sqrt(t)/6,sqrt(t)/6/Xans)
print("========================================")
Delta_A_3 = []
Delta_A_res_3 = []
l_mid_y = []
for i in range(16,22):
    I = 0
    for j in data[i]:
        I += j
    I /= 6
    l_mid_y.append(cal_l_3(I,pi/2**(2-(i-10)%3),850 if (i - 10) % 6 < 3 else 950,Xans))
    Delta_A_3.append(cal_Delta_A_6(6,data[i][0:6])*sqrt(2))
    print("在pi /",2**(2-(i-10)%3),"角度",850 if (i - 10) % 6 < 3 else 950,"电压下有",I,"平均电流",l_mid_y[-1],"距离")
    Delta_A_res_3.append(cal_delta_A_res_3(Delta_A_3[-1],pi/2**(2-(i-10)%3),850 if (i - 10) % 6 < 3 else 950,I,Xans))
    print("算的结果不确定度和相对不确定度为",Delta_A_res_3[-1],Delta_A_res_3[-1]/l_mid_y[-1])
Yans = np.mean(l_mid_y)
t = 0
for i in range(6):
    t += Delta_A_res_3[i]**2
print("在y方向测得y偏转板中间位置到荧光屏距离约为",Yans)
print("不确定度和相对不确定度为",sqrt(t)/6,sqrt(t)/6/Yans)
