import numpy as np
import matplotlib.pyplot as plt

# 常数
R1 = 1.2e-3
R2 = 9.2e-3
C_in = 1.1e6
C_wall = 1.86e8
Pn = 8e3

# 系统矩阵
A = np.array([[-1/(R1*C_in), 1/(R1*C_in)],
              [1/(R1*C_wall), -1/(R1*C_wall)-1/(R2*C_wall)]])
B = np.array([[1/C_in, 0],
              [0, 1/(R2*C_wall)]])

# 模拟参数
day_num = 30
T = day_num*24*60*60
dt = 60
t = np.arange(0, T+dt, dt)
N = len(t)
Ad = np.eye(2) + A*dt
Bd = B*dt

theta_in0 = 20
theta_out0 = -15

# 预分配结果数组
P_heat = np.zeros(N)
U = np.zeros((2, N))
X = np.zeros((2, N))

# 初始化此模拟的变量
theta_wall0 = (theta_in0 + theta_out0)/2
theta_out = theta_out0*np.ones(N)
P_heat[0] = Pn
U[:,0] = np.array([P_heat[0], theta_out[0]])
X[:,0] = np.array([theta_in0, theta_wall0])

# 计算系统响应
for i in range(1, N):
    if X[0,i-1] > 22:
        U[0,i] = 0
    elif X[0,i-1] < 18:
        U[0,i] = Pn
    else:
        U[0,i] = U[0,i-1]
    X[:,i] = Ad @ X[:,i-1] + Bd @ U[:,i]

# 切片最后一天的稳态数据并绘制相应的图形
index_cut = np.arange((day_num-1)*24*60*60//dt+1, (day_num)*24*60*60//dt+1)
X_cut = X[:, index_cut]
U_cut = U[:, index_cut]

plt.figure()
plt.plot(t[index_cut]/60, X_cut[0,:])
plt.plot(t[index_cut]/60, X_cut[1,:])
plt.legend(['室内温度', '墙体温度'])
plt.xlabel('时间/分钟')
plt.ylabel('温度')
plt.grid(True)
plt.title(f'室外温度为{theta_out0}时的温度变化')
plt.savefig(f'Q2.1_temp_change_with_Tout_{theta_out0}.png', dpi=300)
plt.show()

plt.figure()
plt.plot(t[index_cut]/60, U_cut[0,:])
plt.xlabel('时间/分钟')
plt.ylabel('瓦特制热功率')
plt.grid(True)
plt.title(f'室外温度为{theta_out0}时的制热功率变化')
plt.savefig(f'Q2.1_heating_power_with_Tout_{theta_out0}.png', dpi=300)
plt.show()

# 计算加热和冷却时间
P_heat = U_cut[0,:]
u = P_heat == Pn
up_time = np.sum(u)*dt/60
down_time = np.sum(~u)*dt/60

print(f'Q2.1 加热时间: {up_time} 分钟')
print(f'Q2.1 冷却时间: {down_time} 分钟')