import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = np.array(pd.read_excel(io="./Mdata2.xlsx")).transpose()
x = data[0]
y = data[2]

D = data[3][0:5]
num_D = data[6][0:5]

ave_delta_D = data[5][0] * 1000000

# 计算回归系数
slope, intercept = np.polyfit(x, y, 1)
_lambda = slope * 2 * 1000000

y2 = slope * x + intercept
print("\lambda=", _lambda, "nm", " b=", intercept * 1000000, "nm")
print("r^2=", np.corrcoef(y, y2)[0, 1] ** 2)
print("\delta\lambda=", _lambda ** 2 / 2 / ave_delta_D, "nm")
#
# # 绘制拟合曲线
plt.figure(1)
plt.scatter(x, y)
plt.plot(x, slope * x + intercept, color='red')
#
k, b = np.polyfit(num_D, D, 1)
plt.figure(2)
plt.scatter(num_D, D)
plt.plot(num_D, k * num_D + b)
plt.show()
