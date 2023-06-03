# 室外平均温度和持续天数
temperatures = [0, -5, -10, -15, -20]
duration = [30, 40, 40, 40, 30]

# 定义变量和参数
num_households = 600
max_down_adjustable_power = 5000  # 假设持续最大向下调节功率值为5000W
max_up_adjustable_power = 3000  # 假设持续最大向上调节功率值为3000W
temperature_data = np.random.uniform(18, 22, size=(num_households, 24))  # 600个住户的初始室内温度数据，假设在温控区间内均匀分布
temperature_range = (18, 22)  # 温控区间的最小温度和最大温度
compensation_price = 0.1  # 辅助服务补偿价格，假设为0.1元/W
heat_cost_per_household = 1000  # 每户的供热成本，假设为1000元

total_savings = 0  # 总节省成本
total_income = 0  # 总收益

# 循环模拟每个时间步长内的温度变化
for temp, dur in zip(temperatures, duration):
    wall_temperature = get_wall_temperature(temp)
    peak_hours, valley_hours = get_peak_valley_hours()
    for t in range(dur):
        for i in range(num_households):
            # 计算当前时刻的电采暖设备功率
            if t in peak_hours:
                power = max_down_adjustable_power
            elif t in valley_hours:
                power = -max_up_adjustable_power
            else:
                power = 0

            # 使用温变过程等值模型计算室内温度的变化
            d_theta = (power / C_in) - ((temperature_data[i, t] - wall_temperature[t]) / (R1 * C_in))
            temperature_data[i, t + 1] = temperature_data[i, t] + d_theta

    # 统计开关状态发生变化的电采暖设备数量
    num_devices_changed = np.sum(np.diff(temperature_data, axis=1) != 0, axis=0)

    # 计算每个时间点的调节功率和收益
    for t in range(24):
        if t in peak_hours:
            power = max_down_adjustable_power
        elif t in valley_hours:
            power = -max_up_adjustable_power
        else:
            power = 0

        # 计算总节省成本和总收益
        total_savings += num_devices_changed[t] * power * compensation_price
        total_income += num_devices_changed[t] * power * compensation_price

# 计算平均每户的收益和节省的供热成本百分比
avg_income_per_household = total_income / num_households
savings_percentage = (1 - total_savings / (num_households * heat_cost_per_household)) * 100

# 输出结果
print(f"平均每户的收益：{avg_income_per_household:.2f} 元")
print(f"节省的供热成本百分比：{savings_percentage:.2f}%")