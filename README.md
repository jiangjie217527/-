# 目录导航

MCRatio means 磁聚焦法测量Mass-to-charge ratio(荷质比)

RLC means RLC电路实验

MM:磁性材料基本特性研究。磁性材料(Magnetic material,MM)

UB(Unbalanced bride,非平衡电桥)

迈克尔逊干涉仪(Michelson interferometer,MI)

# 环境配置

编程语言为python.没有环境或不会使用请自行配置或联系我。

本代码使用了
1. numpy
2. mathplotlib
3. pandas

在读取.xlsx文件的时候还可能用到openpyxl

在使用前如果不确定有无这四个package，(如果有pip的话)请在命令行中输入以下代码

~~~
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
pip install openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
~~~

# 中文乱码

对于windows系统，请把

~~~
plt.rcParams["font.sans-serif"]=['Noto Sans CJK JP'] #设置字体
~~~

修改成

~~~
plt.rcParams["font.sans-serif"]=['SimHei'] #设置字体
~~~

---

附：联系方式

qq:509745383
个人主页：jiangjie.xyz
