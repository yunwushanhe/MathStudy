import numpy as np
import matplotlib.pyplot as plt

# 室内温度变化模型参数
C_in = 3.5  # 住户室内热容量，单位：kWh/℃
R1 = 0.03   # 墙体和室内之间的热阻，单位：℃/kW

# 初始化数据
T_sim = 1440  # 模拟时间范围内的总时间步数，每分钟一个时间步
theta_in = np.zeros((600, T_sim))  # 住户室内温度数组，每行代表一个住户，每列代表一个时间步
P_heat = np.zeros((600, T_sim))    # 住户电采暖设备功率数组，每行代表一个住户，每列代表一个时间步

# 初始化室内温度分布，假设在温控区间内均匀分布
theta_in[:, 0] = np.linspace(18, 22, 600)

# 循环模拟时间范围内的温度变化
for t in range(T_sim - 1):
    for i in range(600):
        # 计算室内温度的变化
        d_theta_in = P_heat[i, t] / C_in - (theta_in[i, t] - theta_wall[t]) / (R1 * C_in)
        theta_in[i, t+1] = theta_in[i, t] + d_theta_in

# 计算住宅区电采暖设备的总用电功率曲线
P_total = np.sum(P_heat, axis=0)

# 计算住宅区电采暖负荷可参与上调、下调的总功率曲线
is_adjustable = np.random.randint(0, 2, size=(600, T_sim))  # 随机初始化可调节状态，0表示不可调节，1表示可调节
P_adjustable = np.sum(P_heat * is_adjustable, axis=0)

# 绘制曲线
time = np.arange(0, T_sim) / 60.0  # 时间步转换为小时
plt.figure(figsize=(10, 6))
plt.plot(time, P_total, label='Total Power')
plt.plot(time, P_adjustable, label='Adjustable Power')
plt.xlabel('Time (hours)')
plt.ylabel('Power (kW)')
plt.title('Total Power and Adjustable Power')
plt.legend()
plt.grid(True)
plt.show()