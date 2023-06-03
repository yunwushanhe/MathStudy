import numpy as np
import matplotlib.pyplot as plt

# 典型住户温变过程等值模型参数
R1 = 1.2e-3  # 热阻 R1/(℃/W)
Cin = 1.1e6  # 热容 Cin/(J/℃)

# 温控区间上下限
theta_upper = 22.0
theta_lower = 18.0

# 墙体温度数据（示例）
theta_wall = np.random.uniform(15.0, 25.0, 24*60)  # 每分钟一个数据点，随机生成在15-25°C之间的墙体温度

# 初始化室内温度、电采暖设备状态和功率
theta_in = np.random.uniform(theta_lower, theta_upper, 24*60)  # 初始室内温度均匀分布在温控区间内
heater_status = np.ones(24*60)  # 初始状态都为开启
P_heat = np.zeros(24*60)  # 初始功率都为0

# 模拟时间范围
T_sim = 24*60

# 循环模拟时间范围内的温度变化
for t in range(1, T_sim):
    for i in range(24*60):
        # 计算室内温度的变化
        d_theta_in = P_heat[i] / Cin - (theta_in[i] - theta_wall[t]) / (R1 * Cin)
        theta_in[i] += d_theta_in

        # 判断是否需要调整电采暖设备的开关状态
        if theta_in[i] > theta_upper and heater_status[i] == 1:
            heater_status[i] = 0
        elif theta_in[i] < theta_lower and heater_status[i] == 0:
            heater_status[i] = 1

    # 计算总用电功率
    P_total = np.sum(P_heat)

# 绘制总用电功率曲线
time = np.arange(0, T_sim)
plt.plot(time, P_total)
plt.xlabel('Time (minutes)')
plt.ylabel('Total Power (W)')
plt.title('Total Power Consumption')
plt.show()