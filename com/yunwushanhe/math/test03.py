import numpy as np
import matplotlib.pyplot as plt

# 参数设置
Cin = 1100000  # 室内空气等效热容，J/℃
Cwall = 186000000  # 墙体等效热容，J/℃
R1 = 0.0012  # 室内空气和墙体内侧的等效热阻，m^2·℃/W
R2 = 0.0092  # 墙体外侧和室外空气的等效热阻，m^2·℃/W
PN = 8000  # 电采暖设备的额定功率，W
Tout = 0
# 时间设置
dt = 613  # 时间间隔，s
t = np.arange(0, 24 * 3600, dt)  # 时间数组，s

# 初始状态设置
Tin0 = 20  # 初始室内温度，℃
Twall0 = 20  # 初始墙体温度，℃Son = np.zeros_like(t)  # 初始电采暖设备关闭

# 计算室内温度和电采暖设备开关状态
Tin = np.zeros_like(t)
Tin[0] = Tin0

Twall = np.zeros_like(t)
Twall[0] = Twall0

S = np.zeros_like(t)

for i in range(len(t) - 1):
#     # 计算室外温度
#     if t[i] < 6 * 3600:
#         Tout = 0
#     elif t[i] < 18 * 3600:
#         Tout = -5
#     else:
#         Tout = -10

    # 计算电采暖设备制热功率
    # S = 1 if Tin < 18 else 0  # 当室外温度小于0度时，开启电采暖设备
    if Tin[i] == 18:
        S[i] = 1
    elif Tin[i] > 22:
        S[i] = 0
    Pheat = S[i] * PN

    # 计算室内温度和墙体温度变化
    dTin_dt = (Pheat - (Tin[i] - Twall[i]) / R1) / Cin
    dTwall_dt = ((Tin[i] - Twall[i]) / R1 - (Twall[i] - Tout) / R2) / Cwall

    Tin[i + 1] = Tin[i] + dTin_dt * dt
    Twall[i + 1] = Twall[i] + dTwall_dt * dt

# 绘制可视化图像
plt.figure(figsize=(10, 6))
plt.plot(t / 3600, Tin, label='室内温度')
plt.plot(t / 3600, Twall, label='电采暖设备制热功率')
plt.legend()
plt.xlabel('时间（h）')
plt.ylabel('温度（℃）')
plt.show()

# 计算特征量并填入表格
Tout_list = [0, -5, -10, -15, -20, -25]  # 室外温度列表，℃

# print('|室外温度（℃）|平均室内温度（℃）|最高室内温度（℃）|最低室内温度（℃）|平均电采暖设备功率（W）|电采暖设备总耗电量（kWh）|')
# print('|-|-|-|-|-|-|')