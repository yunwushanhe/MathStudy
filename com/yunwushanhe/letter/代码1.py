import numpy as np

# 定义模型参数
R1 = 1.2e-3  # ℃/W
R2 = 9.2e-3  # ℃/W
Cin = 1.1e6  # J/℃
Cwall = 1.86e8  # J/℃
PN = 8.0  # kW

# 定义时间步长和模拟时间
dt = 1  # 分钟
T = 24 * 60  # 分钟

# 定义函数计算稳态解
def calculate_steady_state(theta_out):
    theta_in = (R2 * theta_out) / (R1 + R2)
    P_heat = (theta_in - theta_out) / R1
    return theta_in, P_heat

# 定义函数模拟温度变化和电采暖设备开关状态
def simulate_temperature(theta_in0, theta_out):
    theta_in = np.zeros(T)
    theta_wall = np.zeros(T)
    S = np.zeros(T)
    
    theta_in[0] = theta_in0
    theta_wall[0] = theta_in0
    
    for t in range(1, T):
        P_heat = calculate_steady_state(theta_out)[1]
        d_theta_in = (P_heat - (theta_in[t-1] - theta_wall[t-1]) / R1) * dt / Cin
        d_theta_wall = ((theta_in[t-1] - theta_wall[t-1]) / R1 - (theta_wall[t-1] - theta_out) / R2) * dt / Cwall
        
        theta_in[t] = theta_in[t-1] + d_theta_in
        theta_wall[t] = theta_wall[t-1] + d_theta_wall
        
        if theta_in[t] < 18:
            S[t] = 1
        elif theta_in[t] > 22:
            S[t] = 0
        else:
            S[t] = S[t-1]
    
    return theta_in, S

# 定义函数计算特征量
def calculate_characteristics(theta_in0, theta_out):
    theta_in, S = simulate_temperature(theta_in0, theta_out)
    on_periods = np.where(np.diff(S) > 0)[0]
    off_periods = np.where(np.diff(S) < 0)[0]
    cycle_length = np.mean(np.diff(on_periods))
    on_duration = np.mean(np.diff(on_periods))
    off_duration = np.mean(np.diff(off_periods))
    duty_cycle = on_duration / cycle_length * 100
    daily_energy = np.sum(S) * PN * dt / 60
    average_power = daily_energy / T * 60
    cost = daily_energy * (0.56 if 8 <= theta_out <= 21 else 0.32)
    
    return cycle_length, on_duration, off_duration, duty_cycle, daily_energy, average_power, cost

# 定义温度范围
temperatures = [0, -5, -10, -15, -20, -25]

# 计算特征量并输出结果
table1 = np.zeros((len(temperatures), 7))

for i, temp in enumerate(temperatures):
    cycle_length, on_duration, off_duration, duty_cycle, daily_energy, average_power, cost = calculate_characteristics(20, temp)
    
    table1[i, 0] = temp
    table1[i, 1] = on_duration
    table1[i, 2] = off_duration
    table1[i, 3] = cycle_length
    table1[i, 4] = duty_cycle
    table1[i, 5] = daily_energy
    table1[i, 6] = average_power * 24 * 60 * (0.56 if 8 <= temp <= 21 else 0.32)

# 输出结果
print("表1 典型住户电采暖负荷用电行为特征量统计结果（室内初始温度为20°C）")
print("室外温度\t平均升温时长/min\t平均降温时长/min\t周期/min\t平均占空比/%\t日用电量/kWh\t日平均用电功率/kW\t日用电成本/元")
for row in table1:
    print(f"{row[0]}℃\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}")