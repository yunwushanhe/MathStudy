import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# 定义常微分方程
def room_temperature(t, y, R1, R2, Cin, Cwall, Pheat):
    theta_in, theta_wall = y
    d_theta_in = (Pheat - (theta_in - theta_wall) / R1) / Cin
    d_theta_wall = ((theta_in - theta_wall) / R1 - (theta_wall - theta_out) / R2) / Cwall
    return [d_theta_in, d_theta_wall]

# 定义参数
R1 = 1.2e-3
R2 = 9.2e-3
Cin = 1.1e6
Cwall = 1.86e8
PN = 8.0 * 1e3
theta_out = 0  # 假设室外温度恒定为0°C
theta_in0 = 20  # 初始室内温度

# 定义时间范围
t_start = 0
t_end = 3600  # 假设求解的时间范围为1小时
t_span = (t_start, t_end)

# 定义初始条件
initial_conditions = [theta_in0, theta_in0]  # 初始室内温度和墙体温度相等

# 定义电采暖设备功率
def heat_power(t):
    if t < 1800:
        return PN
    else:
        return 0

# 数值求解常微分方程
solution = solve_ivp(lambda t, y: room_temperature(t, y, R1, R2, Cin, Cwall, heat_power(t)), t_span, initial_conditions)

# 提取结果
t_values = solution.t
theta_in_values = solution.y[0]
theta_wall_values = solution.y[1]

# 绘制温度变化曲线
plt.figure(figsize=(10, 6))
plt.plot(t_values, theta_in_values, label='Indoor Temperature')
plt.plot(t_values, theta_wall_values, label='Wall Temperature')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Temperature Variation')
plt.legend()
plt.grid(True)
plt.show()