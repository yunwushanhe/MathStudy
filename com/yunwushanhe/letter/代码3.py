import numpy as np
import matplotlib.pyplot as plt

# 定义模型参数
R1 = 1.2e-3  # 室内空气和墙体内侧的等效热阻（℃/W）
R2 = 9.2e-3  # 墙体外侧和室外空气的等效热阻（℃/W）
Cin = 1.1e6  # 室内空气等效热容（J/℃）
Cwall = 1.86e8  # 墙体等效热容（J/℃）
PN = 8.0  # 电采暖设备额定功率（kW）
theta_in0 = 20  # 室内初始温度（℃）
theta_out = -15  # 室外温度（℃）

# 计算稳态解
theta_in_steady = (PN * R2 * theta_out + theta_in0 * (Cwall / R1 + Cwall / R2) + theta_out * Cin) / (Cin + Cwall / R1 + Cwall / R2)
theta_wall_steady = (theta_in_steady * Cin + theta_in0 * Cwall / R1 + theta_out * Cwall / R2) / (Cin + Cwall / R1 + Cwall / R2)

# 计算可持续时间
t = np.arange(0, 24 * 60 + 1, 1)  # 时间点，间隔1min
P_heat = np.zeros_like(t)  # 电采暖设备制热功率
theta_in = np.zeros_like(t)  # 室内温度
theta_wall = np.zeros_like(t)  # 墙体温度

# 初始化状态
P_heat[0] = PN
theta_in[0] = theta_in0
theta_wall[0] = theta_wall_steady

# 模拟计算
for i in range(1, len(t)):
    # 判断是否进行功率调节
    if theta_in[i-1] > 22:
        P_heat[i] = 0  # 关闭电采暖设备
    elif theta_in[i-1] < 18:
        P_heat[i] = PN  # 开启电采暖设备
    else:
        P_heat[i] = P_heat[i-1]  # 维持当前状态

    # 更新温度
    d_theta_in = (P_heat[i] - (theta_in[i-1] - theta_wall[i-1]) / R1) * (1 / Cin)
    d_theta_wall = ((theta_in[i-1] - theta_wall[i-1]) / R1 - (theta_wall[i-1] - theta_out) / R2) * (1 / Cwall)
    theta_in[i] = theta_in[i-1] + d_theta_in
    theta_wall[i] = theta_wall[i-1] + d_theta_wall

# 计算功率调节的可持续时间
upward_duration = len(np.where(P_heat == PN)[0])
downward_duration = len(np.where(P_heat == 0)[0])

# 绘制计算结果
plt.figure(figsize=(12, 6))
plt.plot(t / 60, P_heat, label='Power')
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
plt.axhline(y=PN, color='red', linestyle='--', linewidth=0.8)
plt.xlabel('Time (hours)')
plt.ylabel('Power (kW)')
plt.title('Power Adjustment of Typical Household Heating Load')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(t / 60, theta_in, label='Indoor Temperature')
plt.axhline(y=18, color='blue', linestyle='--', linewidth=0.8)
plt.axhline(y=22, color='orange', linestyle='--', linewidth=0.8)
plt.xlabel('Time (hours)')
plt.ylabel('Temperature (°C)')
plt.title('Indoor Temperature of Typical Household')
plt.legend()
plt.grid(True)
plt.show()