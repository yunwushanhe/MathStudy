import numpy as np
import matplotlib.pyplot as plt

# 定义模型参数
C_in = 1.1e6  # 室内空气等效热容
C_wall = 1.86e8  # 墙体等效热容
R_1 = 1.2e-3  # 室内空气和墙体内侧的等效热阻
R_2 = 9.2e-3  # 墙体外侧和室外空气的等效热阻
q_out = -15  # 室外温度
q_in_initial = 20  # 室内初始温度
P_N = 8.0  # 电采暖设备的额定功率
delta_t = 1  # 时间步长（分钟）
num_steps = 24 * 60 // delta_t  # 总步数

# 初始化数据
q_in = np.zeros(num_steps)  # 室内温度数组
q_wall = np.zeros(num_steps)  # 墙体温度数组
P_heat = np.zeros(num_steps)  # 电采暖设备制热功率数组
t = np.arange(0, num_steps * delta_t, delta_t)  # 时间数组

# 设置初始条件
q_in[0] = q_in_initial
P_heat[0] = P_N

# 计算温度变化
for i in range(1, num_steps):
    # 计算墙体温度
    q_wall[i] = (q_wall[i - 1] * (R_2 + R_1) + q_out * R_2 + q_in[i - 1] * R_1) / (R_2 + R_1)

    # 计算室内温度变化
    dQ_in = (P_heat[i - 1] - (q_in[i - 1] - q_wall[i]) / R_1) / C_in
    q_in[i] = q_in[i - 1] + dQ_in * delta_t

# 计算功率上调和下调的可持续时间
up_time = 0  # 上调可持续时间
down_time = 0  # 下调可持续时间

for i in range(num_steps):  # DAMA
    # 上调可持续时间
    if q_in[i] >= 25:
        up_time += delta_t
    # 下调可持续时间
    if q_in[i] <= 15:
        down_time += delta_t

# 绘制计算结果
plt.figure(figsize=(10, 6))
plt.plot(t, q_in, label='Indoor Temperature')
plt.axhline(y=25, color='r', linestyle='--', label='Upper Threshold')
plt.axhline(y=15, color='b', linestyle='--', label='Lower Threshold')
plt.xlabel('Time (min)')
plt.ylabel('Temperature (°C)')
plt.title('Indoor Temperature Variation')
plt.legend()
plt.grid(True)
plt.show()

# 输出结果
print("可持续上调时间：", up_time, "分钟")
print("可持续下调时间：", down_time, "分钟")