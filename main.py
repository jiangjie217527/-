import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# from scipy.interpolate import make_interp_spline

data = np.array(pd.read_excel(io="./data.xlsx")).transpose()
print(data)
fig, ax = plt.subplots()
ax.plot(data[0], data[1], label="1")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines["bottom"].set_position(("data",0))
ax.spines["left"].set_position(("data",0))
plt.show()
