import numpy as np
from scipy import signal

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
Ad = np.eye(2) + A*dt #离散化
Bd = B*dt
theta_in0 = 20 #室内初始温度
theta_out0 = np.array([0,-5,-10,-15,-20,-25]) #室外温度

k_length = len(theta_out0)
up_time = np.zeros(k_length)
down_time = np.zeros(k_length)
P_heat = np.zeros((k_length,N)) #初始化P_heat
U = np.zeros((2,N,k_length)) #初始化U
X = np.zeros((2,N,k_length)) #初始化X

for k in range(k_length):
    theta_wall0=(theta_in0+theta_out0[k])/2 #假设墙体初始温度等于室内温度与室外温度的平均
    theta_out=theta_out0[k]*np.ones(N)
    P_heat[k,:]=np.zeros(N) #初始化对应的P_heat
    U[:,:,k]=np.array([P_heat[k,:],theta_out])
    X[:,0,k]=np.array([theta_in0,theta_wall0])
    for i in range(1,N):
        if X[0,i-1,k] > 22:
            U[1,i,k] = 0 #如果大于22，关闭
        elif X[0,i-1,k] < 18:
            U[1,i,k] = Pn #如果小于18，开启
        else:
            U[1,i,k] = U[1,i-1,k] #如果在区间内，保持上一次的制热功率不变
        X[:,i,k] = np.dot(Ad,X[:,i-1,k]) + np.dot(Bd,U[:,i,k])

index_cut = (day_num-1)*24*60*60//dt + np.arange(len(np.arange(0,24*60*60+dt,dt))) #切分出最后1天的稳态数据

X_cut = X[:,index_cut,:]
U_cut = U[:,index_cut,:]
for k in range(k_length):
    u = U_cut[1,:,k] == Pn
    up_time[k], down_time[k] = signal.upfirdn(u, [1], up=2, down=2).nonzero()[0][[0,-1]]
    print(f'室外温度为{theta_out0[k]}的稳态后上调的持续时间为{up_time[k]}分钟')
    print(f'室外温度为{theta_out0[k]}的稳态后下调的持续时间为{down_time[k]}分钟')