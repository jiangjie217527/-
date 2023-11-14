import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
# from scipy.interpolate import make_interp_spline

L = 3.61e-2
S = 1.25e-5
N1 = N2 = 100
plt.rcParams["font.sans-serif"]=['Noto Sans CJK JP'] #设置字体
plt.rcParams["axes.unicode_minus"]=False #正常显示负号

# ================相关参数(已在excel中计算)

data = np.array(pd.read_excel(io="./data.xlsx")).transpose()
H = []
B = []
T = []
U = []
U1 = []

def collect(n,t):
    for i in data[n]:
        if isinstance(i,str):
            continue
        if not math.isnan(i):
            t.append(i)

collect(2,T)
collect(3,U)
collect(9,H)
collect(10,B)
collect(12,U1)
T = np.array(T)
U = np.array(U)
H = np.array(H)
B = np.array(B)
U1 = np.array(U1)
len1 = len(H)
len2 = len(T)
HB = np.hstack((H[:,np.newaxis],B[:,np.newaxis]))
t = HB[0]
for i in HB:
    if i[0] < t[0]:
        t = i
tmp = [t]
for i in range(len1):
    nxt = np.array([-50,3])
    miny = 3
    for j in HB:
        if j[0] > tmp[-1][0] and tmp[-1][1] < j[1] <= miny:
            if (j[1] == miny and j[0] > nxt[0]) or j[1] < miny: # 此时nxt必然有意义
                miny = j[1]
                nxt = j
    if not miny == 3:
        tmp.append(nxt)
        ind = 0
        for i in range(len(HB)):
            if HB[i][0] == nxt[0] and HB[i][1] == nxt[1]:
                ind = i
                break
        HB = np.delete(HB,ind,axis=0)
for i in range(len1):
    nxt = np.array([50,-3])
    maxy = -3
    for j in HB:
        if j[0] < tmp[-1][0] and maxy <= j[1] < tmp[-1][1]:
            if maxy < j[1] or (maxy == j[1] and j[0] < nxt[0]):
                maxy = j[1]
                nxt = j
    if not maxy == -3:
        tmp.append(nxt)
        ind = 0
        for i in range(len(HB)):
            if HB[i][0] == nxt[0] and HB[i][1] == nxt[1]:
                ind = i
                break
        HB = np.delete(HB,i,axis=0)
tmp=np.array(tmp).transpose()

# ================数据提取
plt.figure(1)
plt.plot(tmp[0],tmp[1],'r',label = "样点连线")
plot2 = plt.plot(H,B,'o',label = "采样点")
plt.legend(loc=4)
plt.xlabel('H/(A/m)',x = 1.02)
plt.ylabel('B/(T)',y = 1.02)
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines["bottom"].set_position(("data",0))
ax.spines["left"].set_position(("data",0))
plt.title('磁滞回线')


# =================磁滞回线作图

plt.figure(2)
plt.plot(T,U,'r',label = "U-T")
plt.xlabel('T/(摄氏度)',x = 1.02)
plt.ylabel('U/(mV)',y = 1.02)
plt.title('测的电压和温度关系')
plt.legend(loc=1)
plt.figure(3)
plt.plot(T[1:len(U1)+1],U1,'r',label = 'U\'-T')
plt.xlabel('T/(摄氏度)',x = 1.02)
plt.ylabel('U\'(mV/摄氏度)',y = 1.02)
plt.title('测得电压的一阶变化率和温度关系')
plt.legend(loc=1)
ind = -1
minU1 = 0
for i in range(len(U1)):
    if U1[i] < minU1:
        minU1 = U1[i]
        ind = i
print("变化率最大的温度(Tc)",T[ind+1])
plt.show()
