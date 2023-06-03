import matplotlib.pyplot as plt
import numpy as np

q_in = [20.0]  # 初始室内温度
q_wall = [16.5]  # 初始墙体温度
q_out = -25.0 # 用于记录室外温度
delta_t = 1.0  # 时间步长（分钟）
S = [0]
N = int(24 * 60 * 60 // delta_t)  # 模拟的时间步数
X = [0]
R_1 = 0.0012
C_in = 1100000.0
R_2 = 0.0092
C_wall = 186000000.0
P_N = 8000.0

# print(N)

for t in range(N):
    X.append(t+1)

    if q_in[t] < 18:
        S.append(1)
    elif q_in[t] > 22:
        S.append(0)
    else:
        S.append(S[t])

    # 根据室外温度确定制热功率
    P_heat = S[t] * P_N  # 根据电采暖设备的开关状态和额定功率计算制热功率

    # 计算室内温度和墙体温度的变化
    q_in_new = q_in[t] + delta_t * (P_heat - (q_in[t] - q_wall[t]) / R_1) / C_in
    q_wall_new = q_wall[t] + delta_t * ((q_in[t] - q_wall[t]) / R_1 - (q_wall[t] - q_out) / R_2) / C_wall

    # 进行更新记录
    q_in.append(q_in_new)
    q_wall.append(q_wall_new)



# 创建一个新的图形并设置标题
fig = plt.figure()
fig.suptitle('q_in and s with time')

# 添加子图并设置其位置
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx() # 创建一个新的纵坐标

# 绘制第一个曲线
ax1.plot(np.array(X)/3600, q_in, color='blue', label='q_in')
ax1.set_xlabel('x')
ax1.set_ylabel('q_in')
ax1.tick_params(axis='y', labelcolor='blue')

# 绘制第二个曲线
ax2.plot(np.array(X)/3600, S, color='red', label='s')
ax2.set_xlabel('x')
ax2.set_ylabel('s')
ax2.tick_params(axis='y', labelcolor='red')

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines+lines2, labels+labels2, loc='lower left')

plt.show()