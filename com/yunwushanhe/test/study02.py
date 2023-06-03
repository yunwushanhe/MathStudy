import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 室内温度、墙体温度、室外温度、时间步长、时间步数
q_in = [20.0]
q_wall = [16.5]
q_out = 0.0
delta_t = 1.0  # 分钟
N = int(24 * 60 * 60 // delta_t)

# 热容能、热传导阻力、额定功率
R_1 = 0.0012
C_in = 1100000.0
R_2 = 0.0092
C_wall = 186000000.0
P_N = 8000.0

# 制热状态、时间步
S = [0]
timestep = [i for i in range(N)]

# 获取当前制热功率
def get_p_heat(q_in, s):
    if q_in < 18:
        return P_N if s == 1 else 0
    elif q_in > 22:
        return 0 if s == 1 else P_N
    else:
        return P_N * s

# 计算室内温度和墙体温度的变化
def get_new_temp(q_in, q_wall, q_out, p_heat):
    q_in_new = q_in + delta_t * (p_heat - (q_in - q_wall) / R_1) / C_in
    q_wall_new = q_wall + delta_t * ((q_in - q_wall) / R_1 - (q_wall - q_out) / R_2) / C_wall
    return q_in_new, q_wall_new

# 更新温度和制热状态记录
for i in range(N-1):
    p_heat = get_p_heat(q_in[-1], S[-1])
    q_in_new, q_wall_new = get_new_temp(q_in[-1], q_wall[-1], q_out, p_heat)
    S.append(S[-1] if q_in_new > 18 and q_in_new < 22 else 1 if q_in_new < 18 else 0)
    q_in.append(round(q_in_new, 1))
    q_wall.append(round(q_wall_new, 1))

# 创建绘图窗口
fig, ax = plt.subplots()

# 室内温度折线图
temp_line, = ax.plot([], [], lw=2, color='blue', label='q_in')
ax.set_ylabel('室内温度 (℃)', color='blue')
ax.tick_params(axis='y', labelcolor='blue')
ax.set_xlim(0, N / 3600)
ax.set_ylim(0, 30)
ax.set_xlabel(r'Time (h)')

# 制热状态散点图
s_scatter = ax.scatter([], [], s=15, color='red', label='制热状态')

# 标题和图例
plt.title(r'q_in and s with time')
lines, labels = ax.get_legend_handles_labels()
ax.legend(lines, labels, loc='upper left')


# # 初始化函数
# def init():
#     temp_line.set_data([], [])
#     s_scatter.set_offsets([])
#     return temp_line, s_scatter
#
# # 更新函数
# def update(i):
#     temp_line.set_data(np.array(timestep[:i])/3600, q_in[:i])
#     s_scatter.set_offsets(np.c_[timestep[:i]/3600, S[:i]])
#     return temp_line, s_scatter

# ani = FuncAnimation(fig, update, frames=N-1, init_func=init, blit=True)

plt.show()