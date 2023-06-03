import numpy as np
import matplotlib.pyplot as plt

R1 = 1.2e-3
R2 = 9.2e-3
C_in = 1.1e6
C_wall = 1.86e8
Pn = 8e3
A = np.array([[-1/(R1*C_in), 1/(R1*C_in)], [1/(R1*C_wall), -1/(R1*C_wall)-1/(R2*C_wall)]])
B = np.array([[1/C_in, 0], [0, 1/(R2*C_wall)]])
day_num = 30 #30天
T = day_num * 24 * 60 * 60
dt = 60 #60s,1min
t = np.arange(0, T+dt, dt)
N = len(t) #求解点数
Ad = np.eye(2) + A * dt #离散化
Bd = B * dt
theta_in0 = 10 #室内初始温度
theta_wall = 10 #墙体初始温度
theta_out0 = 0
theta_out = theta_out0 * np.ones(N)
P_heat = np.zeros(N)
U = np.array([P_heat, theta_out])
X = np.zeros((2,N))
X[:,0] = [theta_in0, theta_wall]
for i in range(1,N):
    if X[0,i-1] > 22:
        U[0,i] = 0 #如果大于22，关闭
    elif X[0,i-1] < 18:
        U[0,i] = Pn #如果小于18，开启
    else:
        U[0,i] = U[0,i-1] #如果在区间内，保持上一次的制热功率不变

    X[:,i] = Ad @ X[:,i-1] + Bd @ U[:,i]

plt.plot(t/60,X.T)
plt.grid()
plt.legend(['室内温度', '墙体温度'])
plt.ylabel('温度')
plt.xlabel('时间/min')
plt.savefig(f'img/问题1.1室外温度为{theta_out0}时的30天室内温度和墙体温度变化.png', dpi=300)
plt.show()

plt.plot(t/60,U[0,:])
plt.grid()
plt.ylabel('制热功率')
plt.xlabel('时间/min')
plt.savefig(f'img/问题1.1室外温度为{theta_out0}时的30天制热功率.png', dpi=300)
plt.show()

# 计算稳态周期
u = U[0,:] == Pn
# [period, duty_ratio] = get_period(u) # get_period function is not defined in the given MATLAB code
# print(f'稳态周期为{period}分钟')
# print(f'稳态占空比为{duty_ratio}')

index_cut = (day_num-1) * 24 * 60 * 60 // dt + np.arange(len(np.arange(0, 24*60*60+dt, dt))) #切分出最后1天的稳态数据
X_cut = X[:,index_cut]
U_cut = U[:,index_cut]

plt.plot(t[index_cut]/60,X_cut.T)
plt.grid()
plt.legend(['室内温度', '墙体温度'])
plt.ylabel('温度')
plt.xlabel('时间/min')
plt.savefig(f'img/问题1.1室外温度为{theta_out0}时的稳态1天室内温度和墙体温度变化.png', dpi=300)
plt.show()

plt.plot(t[index_cut]/60,U_cut.T)
plt.grid()
plt.ylabel('制热功率')
plt.xlabel('时间/min')
plt.savefig(f'img/问题1.1室外温度为{theta_out0}时的稳态1天制热功率.png', dpi=300)
plt.show()