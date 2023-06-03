import numpy as np
from matplotlib import rcParams
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# 参数定义
Cin = 1.1e6
Cwall = 1.86e8
R1 = 1.2e-3
R2 = 9.2e-3
PN = 8000

# 设置字体为微软雅黑
rcParams['font.sans-serif'] = ['Microsoft YaHei']


# 电采暖设备的开关状态函数
def S(t):
    if t % 24 < 8:  # 每天的前 8 小时关闭
        return 0
    else:  # 其他时间开启
        return 1


def ode_system(t, y):
    qin, qwall = y
    qout = 0  # 假设室外温度为 0 度
    Pheat = S(t) * PN
    dqin_dt = (qin - qwall) / R1 - Pheat / Cin
    dqwall_dt = (qin - qwall) / R1 - (qwall - qout) / R2
    return [dqin_dt, dqwall_dt]


# 初始条件
initial_conditions = [20, 20]  # 假设初始室内温度和墙体温度均为 20 度
# 求解常微分方程
t_span = [0, 24 * 7]  # 求解一周的温度变化
sol = solve_ivp(ode_system, t_span, initial_conditions, t_eval=np.linspace(t_span[0],
                                                                           t_span[1], 1000))
# 输出结果
plt.plot(sol.t, sol.y[0], label='室内温度')
plt.plot(sol.t, sol.y[1], label='墙体温度')
plt.xlabel('时间 (小时)')

plt.ylabel('温度 (摄氏度)')
plt.legend()
plt.show()
