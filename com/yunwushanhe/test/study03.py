import numpy as np
import matplotlib.pyplot as plt

# 模型参数
R1 = 1.2e-3
R2 = 3.9e-3
Cin = 1.1e6
Cwall = 1.86e8
PN = 8.0

# 温控区间
T_lower = 18
T_upper = 22

# 室外温度数据
outdoor_temperatures = [0, -5, -10, -15, -20, -25]

# 统计结果
results = []

# 遍历每个室外温度
for outdoor_temp in outdoor_temperatures:
    # 初始化参数
    t = 0
    dt = 1  # 时间间隔（分钟）
    time = []
    indoor_temperatures = []
    heating_power = []
    total_energy = 0

    # 初始条件
    indoor_temp = 20
    wall_temp = 20

    # 计算一日24小时的温度变化和电采暖设备开关状态
    while t <= 24 * 60:
        # 计算制热功率
        Pheat = 0 if indoor_temp >= T_upper else PN

        # 更新室内温度和墙体温度
        dtheta_in = (Pheat - (indoor_temp - wall_temp) / R1) / Cin * dt
        dtheta_wall = ((indoor_temp - wall_temp) / R1 - (wall_temp - outdoor_temp) / R2) / Cwall * dt
        indoor_temp += dtheta_in
        wall_temp += dtheta_wall

        # 统计数据
        time.append(t)
        indoor_temperatures.append(indoor_temp)
        heating_power.append(Pheat)
        total_energy += Pheat * dt / 60

        t += dt

    # 统计特征量
    avg_warmup_time = time[np.argmax(indoor_temperatures >= T_upper)] - time[np.argmax(indoor_temperatures <= T_lower)]
    avg_cooldown_time = time[np.argmax(indoor_temperatures <= T_lower, axis=0)] - time[np.argmax(indoor_temperatures >= T_upper, axis=0)]
    cycle_duration = time[-1]
    duty_cycle = np.mean(heating_power > 0) * 100
    daily_energy = total_energy
    avg_power = total_energy / 24
    # daily_cost = daily_energy * electricity_price  # 电价根据表1中的数据进行设置

    # 将统计结果添加到列表中
    results.append([outdoor_temp, avg_warmup_time, avg_cooldown_time, cycle_duration, duty_cycle, daily_energy, avg_power, daily_cost])
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(time, indoor_temperatures)
    plt.xlabel('Time (minutes)')
    plt.ylabel('Indoor Temperature (°C)')
    plt.title(f'Indoor Temperature Variation at Outdoor Temperature {outdoor_temp}°C')

    plt.subplot(2, 1, 2)
    plt.plot(time, heating_power)
    plt.xlabel('Time (minutes)')
    plt.ylabel('Heating Power (kW)')
    plt.title(f'Heating Power Variation at Outdoor Temperature {outdoor_temp}°C')

    plt.tight_layout()
    plt.show()

# 打印统计结果
print("表1 典型住户电采暖负荷用电行为特征量统计结果（室内初始温度为20°C）")
print("室外温度  平均升温时长/min  平均降温时长/min  周期/min  平均占空比/%  日用电量/kWh  日平均用电功率/kW  日用电成本/元")
for result in results:
    print("{:<8}  {:<16}  {:<16}  {:<10}  {:<12}  {:<14}  {:<18}  {:<13}".format(*result))