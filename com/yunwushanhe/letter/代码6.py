import numpy as np
import matplotlib.pyplot as plt

# 6个住户的总用电功率曲线（示例）
P_total = np.random.uniform(0, 100, 24*60)  # 每分钟一个数据点，随机生成在0-100W之间的总用电功率

# 初始化可上调、下调的电采暖设备序号及功率
num_devices = 6  # 电采暖设备数量
up_adjustable = np.random.choice(num_devices, size=(24*60), replace=True)
down_adjustable = np.random.choice(num_devices, size=(24*60), replace=True)
total_up_power = np.random.uniform(0, 10, size=(24*60))  # 每分钟一个数据点，随机生成在0-10W之间的总可上调功率
total_down_power = np.random.uniform(0, 10, size=(24*60))  # 每分钟一个数据点，随机生成在0-10W之间的总可下调功率

# 绘制可参与上调、下调的电采暖设备序号及功率曲线
time = np.arange(0, 24*60)
fig, ax1 = plt.subplots()

ax1.plot(time, total_up_power, 'g-', label='Total Up Power')
ax1.plot(time, total_down_power, 'r-', label='Total Down Power')
ax1.set_xlabel('Time (minutes)')
ax1.set_ylabel('Power (W)')
ax1.set_title('Up/Down Power of Electric Heating Devices')
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.plot(time, up_adjustable, 'go', label='Up Adjustable')
ax2.plot(time, down_adjustable, 'ro', label='Down Adjustable')
ax2.set_ylabel('Device Number')
ax2.set_ylim([-1, num_devices+1])
ax2.set_yticks(range(num_devices+1))
ax2.set_yticklabels(range(num_devices+1))
ax2.legend(loc='upper right')

plt.show()