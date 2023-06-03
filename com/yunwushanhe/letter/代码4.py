import numpy as np

# 定义模型参数和温度范围
R1 = 1.2e-3  # 室内空气和墙体内侧的等效热阻（℃/W）
R2 = 9.2e-3  # 墙体外侧和室外空气的等效热阻（℃/W）
Cin = 1.1e6  # 室内空气等效热容（J/℃）
Cwall = 1.86e8  # 墙体等效热容（J/℃）
PN = 8.0  # 电采暖设备额定功率（kW）
theta_in0 = 20  # 室内初始温度（℃）

theta_out_list = [0, -5, -10, -15, -20, -25]  # 不同室外温度列表

# 计算可持续时间
t_up = np.zeros(len(theta_out_list))  # 上调可持续时间
t_down = np.zeros(len(theta_out_list))  # 下调可持续时间

for i, theta_out in enumerate(theta_out_list):
    # 计算稳态解
    theta_in_steady = (PN * R2 * theta_out + theta_in0 * (Cwall / R1 + Cwall / R2) + theta_out * Cin) / (Cin + Cwall / R1 + Cwall / R2)
    theta_wall_steady = (theta_in_steady * Cin + theta_in0 * Cwall / R1 + theta_out * Cwall / R2) / (Cin + Cwall / R1 + Cwall / R2)

    # 初始化状态
    P_heat = PN
    theta_in = theta_in0
    theta_wall = theta_wall_steady

    # 模拟计算
    t = 0
    while True:
        # 判断功率调节
        if theta_in > 22 and P_heat > 0:
            P_heat = 0  # 关闭电采暖设备
            t_down[i] += 1
        elif theta_in < 18 and P_heat == 0:
            P_heat = PN  # 开启电采暖设备
            t_up[i] += 1

        # 更新温度
        d_theta_in = (P_heat - (theta_in - theta_wall) / R1) * (1 / Cin)
        d_theta_wall = ((theta_in - theta_wall) / R1 - (theta_wall - theta_out) / R2) * (1 / Cwall)

        theta_in += d_theta_in
        theta_wall += d_theta_wall
        t += 1

        if t > 24 * 60:
            break

# 输出结果
for i in range(len(theta_out_list)):
    print("室外温度：{}°C".format(theta_out_list[i]))
    print("功率上调可持续时间：{}分钟".format(t_up[i]))
    print("功率下调可持续时间：{}分钟".format(t_down[i]))
    print("-----------------------------")