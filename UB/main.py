import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

plt.rcParams["font.sans-serif"]=['Noto Sans CJK JP'] #设置字体
plt.rcParams["axes.unicode_minus"]=False #正常显示负号

data = np.array(pd.read_excel(io="./data.xlsx")).transpose()

# =============铂电阻==============

R0 = data[3][1]
t = [0]
for i in data[0]:
    if isinstance(i,str):
        continue
    if not math.isnan(i):
        t.append(i)
sampleNum = len(t)
Rt = np.append(np.array([R0]),data[9][1:sampleNum])
t = np.array(t)
Rt = np.float64(Rt) # 必须要把读进来的float类型转化为numpy.float64才能拟合 
coefficient1 = np.polyfit(t,Rt,1)
print("R0 =",R0)
print("A =",coefficient1[0]/coefficient1[1])
p1 = np.poly1d(coefficient1)
Rval = p1(t)
plt.figure(1)
plot1 = plt.plot(t,Rt,'*',label="采样点")
plot2 = plt.plot(t,Rval,'r',label="线性拟合")
plt.xlabel('温度/(摄氏度)')
plt.ylabel('铂电阻阻值/(欧)')
plt.legend(loc=4)
plt.title('铂电阻')
plt.show()

# ===========热敏电阻=============

R0 = data[7][1]
T = [273.16]
for i in data[12]:
    if isinstance(i,str):
        continue
    if not math.isnan(i):
        T.append(i)
sampleNum = len(T)
R = np.append(np.array(R0),data[11][1:sampleNum+1])

# ===========热敏电阻对数============

cT = [1/273.16]
for i in data[13]:
    if isinstance(i,str):
        continue
    if not math.isnan(i):
        cT.append(i)
sampleNum = len(cT)
cT = np.array(cT)
lnRT = np.append(np.array(math.log(R0)),data[14][1:sampleNum+1])
lnRT = np.float64(lnRT)
coefficient2 = np.polyfit(cT,lnRT,1)
print("R0 =",R0)
print("B =",coefficient2[0])
p2 = np.poly1d(coefficient2)
lnRval = p2(cT)
plt.figure(2)
Tdata = np.linspace(min(T),max(T),10000)
Rdata = []
for i in range(10000):
    Rdata.append(R0 * math.exp(coefficient2[0]*(1/Tdata[i]-1/273.16)))
plot1 = plt.plot(T,R,'*',label="采样点")
plot2 = plt.plot(Tdata,Rdata,'r',label="线性拟合")
plt.xlabel('温度/(摄氏度)')
plt.ylabel('热敏电阻阻值/(欧)')
plt.legend(loc=4)
plt.title('热敏电阻')
plt.show()

plt.figure(3)
plot1 = plt.plot(cT,lnRT,'*',label="采样点")
plot2 = plt.plot(cT,lnRval,'r',label="线性拟合")
plt.xlabel('1/温度/(1/摄氏度)')
plt.ylabel('热敏电阻阻值的自然对数/(ln(欧))')
plt.legend(loc=4)
plt.title('热敏电阻自然对数')
plt.show()


