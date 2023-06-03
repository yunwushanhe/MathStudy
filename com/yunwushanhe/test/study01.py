import matplotlib.pyplot as plt
import numpy as np

# 生成横轴数据
x = np.linspace(0, 10, 100)

# 生成两个纵轴数据
y1 = np.sin(x)
y2 = np.cos(x)

# 创建一个新的图形并设置标题
fig = plt.figure()
fig.suptitle('Two curves on the same x-axis')

# 添加子图并设置其位置
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx() # 创建一个新的纵坐标

# 绘制第一个曲线
ax1.plot(x, y1, color='blue', label='sin(x)')
ax1.set_xlabel('x')
ax1.set_ylabel('sin(x)')
ax1.tick_params(axis='y', labelcolor='blue')

# 绘制第二个曲线
ax2.plot(x, y2, color='red', label='cos(x)')
ax2.set_xlabel('x')
ax2.set_ylabel('cos(x)')
ax2.tick_params(axis='y', labelcolor='red')

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines+lines2, labels+labels2, loc='lower left')

plt.show()