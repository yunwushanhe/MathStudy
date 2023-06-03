import numpy as np
from matplotlib import rcParams
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 参数
Cin = 1.1e6
Cwall = 1.86e8
R1 = 1.2e-3
R2 = 9.2e-3
initial_conditions = [20, 20]  # 初始室内温度和墙面温度
outdoor_temps = [0, -5, -10, -15, -20, -25]  # 室外温度列表
target_temperature = 22


def S(t, qin):
    lower_bound = target_temperature - 0.5
    upper_bound = target_temperature + 0.5
    power = P(t, qin)

    if qin < lower_bound:
        S.last_state = 1
    elif qin > upper_bound:
        S.last_state = 0
    return S.last_state, power


S.last_state = 1  # 初始状态设为开启


# 功率调整子函数
def P(t, qin):
    power_range = [8000, 15000]  # 功率范围 (W)
    temperature_range = [target_temperature, target_temperature - 15]  # 温度范围
    return np.interp(qin, temperature_range, power_range)


# 室外温度函数
def outdoor_temperature(t, temp):
    return temp


# 常微分方程
def ode_system(t, y, temp):
    qin, qwall = y
    qout = outdoor_temperature(t, temp)
    state, power = S(t, qin)

    Pheat = state * power * Cin
    dqin_dt = (qwall - qin) / R1 + Pheat / Cin
    dqwall_dt = (qin - qwall) / R1 / Cwall - (qwall - qout) / R2 / Cwall
    return [dqin_dt, dqwall_dt]


def plot_temperature_and_switch_state(sol, temp):
    plt.figure(figsize=(10, 6))
    plt.plot(sol.t, sol.y[0], label=f'室内温度 ({temp}℃)')
    switch_states = [S(t, q)[0] for t, q in zip(sol.t, sol.y[0])]
    plt.plot(sol.t, switch_states, label='电采暖设备开关状态')
    plt.xlabel('时间 (h)')
    plt.ylabel('温度 (℃) / 开关状态')
    plt.legend()
    plt.title(f'室内温度变化和电采暖设备开关状态曲线 ({temp}℃)')
    plt.grid()
    plt.show()

def analyze_results(sol):
    switch_states = [S(t, q)[0] for t, q in zip(sol.t, sol.y[0])]
    on_time = sum(switch_states) / len(switch_states) * 24
    off_time = 24 - on_time
    heating_period = on_time
    duty_cycle = on_time / 24
    power_values = [S(t, q)[1] * s for t, q, s in zip(sol.t, sol.y[0], switch_states)]
    daily_energy = np.trapz(power_values, sol.t) * 24 / 3600 / 1000
    daily_avg_power = daily_energy / 24 * 1000
    daily_cost = daily_energy * 0.56 # 假设每千瓦时耗电成本为 0.56 元
    return on_time, off_time, heating_period, duty_cycle, daily_energy, daily_avg_power, daily_cost
        # 输出表头
print('室外温度\t 平均升温时长/min\t 平均降温时长/min\t 周期/min\t 平均占空比/%\t 日用电量/kWh\t 日平均用电功率/kW\t 日用电成本/元')
t_span = (0, 24) # 时间范围 (h)
t_eval = np.linspace(t_span[0], t_span[1], 5000) # 时间评估点
# 遍历每个室外温度
for temp in outdoor_temps:
    sol = solve_ivp(ode_system, t_span, initial_conditions, args=(temp,), t_eval=t_eval, method='RK45')
    plot_temperature_and_switch_state(sol, temp)
    on_time, off_time, heating_period, duty_cycle, daily_energy, daily_avg_power,daily_cost = analyze_results(sol)
    print(f"{temp}℃\t{on_time * 60:.2f}\t\t{off_time * 60:.2f}\t\t{heating_period * 60:.2f}\t\t{duty_cycle * 100:.2f}\t\t{daily_energy:.2f}\t\t{daily_avg_power:.2f}\t\t{daily_cost:.2f}")