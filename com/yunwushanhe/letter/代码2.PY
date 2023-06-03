import numpy as np

from com.yunwushanhe.letter.代码1 import calculate_characteristics


def calculate_heating_period(total_days):
    temperatures = [0, -5, -10, -15, -20]
    duration = [30, 40, 40, 40, 30]
    total_energy = 0
    total_cost = 0

    for temp, days in zip(temperatures, duration):
        theta_out = temp
        theta_in0 = 20
        for _ in range(days):
            _, _, _, _, daily_energy, _, cost = calculate_characteristics(theta_in0, theta_out)
            total_energy += daily_energy
            total_cost += cost
        from com.yunwushanhe.letter.代码7 import theta_in
        theta_in0 = theta_in[-1]  # Use the final temperature from the previous day as the initial temperature for the next day

    return total_energy, total_cost

heating_period_days = 180
total_energy, total_cost = calculate_heating_period(heating_period_days)

print("供暖期总用电量：", total_energy, "kWh")
print("供暖期总成本：", total_cost, "元")