import numpy as np

# 定义削峰时段和填谷时段的起始时间和结束时间
peak_periods = [(8, 10), (18, 20)]
valley_periods = [(0, 4), (12, 16)]

# 初始化电采暖负荷数据，假设为随机生成的数据
load_data = np.random.uniform(0, 10, size=(600, 24))

# 计算削峰时段可提供的持续最大向下调节功率值
down_adjustable_power = []
for period in peak_periods:
    start_time, end_time = period
    power_adjustable = load_data[:, start_time:end_time]
    total_power_adjustable = np.sum(power_adjustable, axis=1)
    down_adjustable_power.append(np.max(total_power_adjustable))

max_down_adjustable_power = np.max(down_adjustable_power)

# 计算填谷时段可提供的持续最大向上调节功率值
up_adjustable_power = []
for period in valley_periods:
    start_time, end_time = period
    power_adjustable = load_data[:, start_time:end_time]
    total_power_adjustable = np.sum(power_adjustable, axis=1)
    up_adjustable_power.append(np.max(total_power_adjustable))

max_up_adjustable_power = np.max(up_adjustable_power)

print("削峰时段可提供的持续最大向下调节功率值：", max_down_adjustable_power)
print("填谷时段可提供的持续最大向上调节功率值：", max_up_adjustable_power)