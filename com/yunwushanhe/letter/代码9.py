import numpy as np
import matplotlib.pyplot as plt

# 定义变量和参数
load_data = np.random.rand(600, 24)  # 600个住户的电采暖负荷数据
max_down_adjustable_power = 5000  # 假设持续最大向下调节功率值为5000W
max_up_adjustable_power = 3000  # 假设持续最大向上调节功率值为3000W
temperature_data = np.random.uniform(18, 22, size=(600, 24))  # 600个住户的初始室内温度数据，假设在温控区间内均匀分布
temperature_range = (18, 22)  # 温控区间的最小温度和最大温度

# 循环模拟每个时间步长内的温度变化
for t in range(24):
    for i in range(600):
        # 计算当前时刻的电采暖设备功率
        if t in peak_hours:
            power = max_down_adjustable_power
        elif t in valley_hours:
            power = -max_up_adjustable_power
        else:
            power = 0
        
        # 使用温变过程等值模型计算室内温度的变化
        d_theta = (power / C_in) - ((temperature_data[i, t] - wall_temperature[t]) / (R1 * C_in))
        temperature_data[i, t+1] = temperature_data[i, t] + d_theta

# 统计开关状态发生变化的电采暖设备数量
num_devices_changed = np.sum(np.diff(temperature_data, axis=1) != 0, axis=0)

# 绘制所有住户的室内温度曲线
time = np.arange(25)  # 时间轴，包括24小时和初始时刻
plt.figure(figsize=(10, 6))
for i in range(600):
    plt.plot(time, temperature_data[i], alpha=0.3)
plt.xlabel('Time')
plt.ylabel('Indoor Temperature')
plt.title('Indoor Temperature of All Households')
plt.grid(True)
plt.show()

# 检验参与调节后温度变化是否满足温控区间约束
num_devices_out_of_range = np.sum((temperature_data[:, 1:] < temperature_range[0]) | (temperature_data[:, 1:] > temperature_range[1]), axis=0)

# 输出结果
print(f"开关状态发生变化的电采暖设备数量：{num_devices_changed}")
print(f"不满足温控区间约束的住户数量：{num_devices_out_of_range}")