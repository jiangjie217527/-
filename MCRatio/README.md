MCRatio means Mass-to-charge ratio(荷质比)

完全放弃识图成excel了，有的字我自己都认不出来。所以这是唯一要花大量时间的内容。

根据“取-x0 至 x0 之间的距离为螺距 l”，计算$x_0$为l/2

数据给了$D_{in},D_{out}$,但是计算只需要直径D，所以采用了平均值

将数据按照表格中的提示填入data.xlsx,不区分方向正反

运行main.py，在终端中python main.py即可运行。

11.2更新 计算不确定度

计算方法回顾

分A类不确定度和B类...

首先定义标准偏差$\sigma_{\bar{x}}=\sqrt{\frac{\sum(\bar{x}-x_i)^2}{n(n-1)}}=\frac{\sigma_x}{\sqrt{n}}$

测量次数很大时()$\Delta_A=2\sigma_{\bar{x}}$

测量次数不大时(6-10次)$\Delta_A=\frac{t_{0.95}}{\sqrt{n}}\sigma_x$

同时当测量次数为6次的时候，$\frac{t_{0.95}}{\sqrt{n}}=1.05$

B类误差为仪器允差/1.05但是由于读数是精确的，所以不存在B类误差

在计算完直接测量量的误差之后，要找到误差传递公式

咕咕姑～
