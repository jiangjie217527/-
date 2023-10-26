import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from odf.opendocument import load
from odf import text,teletype

data = np.array(pd.read_excel(io="./data.xlsx")).transpose()
plt.figure(1)
l1=plt.plot(data[0],data[1],label="U-f")
plt.legend(handles=l1)
plt.show()
plt.figure(2)
l2=plt.plot(data[0],data[3],label="real phi-f")
l3=plt.plot(data[0],data[4],label="theorem phi-f")
plt.legend(handles=l2+l3)
plt.show()
