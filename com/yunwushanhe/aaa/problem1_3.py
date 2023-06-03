import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

R1 = 1.2e-3
R2 = 9.2e-3
C_in = 1.1e6
C_wall = 1.86e8
Pn = 8e3
A = np.array([[-1/(R1*C_in), 1/(R1*C_in)], [1/(R1*C_wall), -1/(R1*C_wall)-1/(R2*C_wall)]])
B = np.array([[1/C_in, 0], [0, 1/(R2*C_wall)]])

dt = 60 #60s,1min
Ad = np.eye(2) + A * dt #离散化
Bd = B * dt
theta_in0 = 20 #室内初始温度

theta_out0 = [0,-5,-10,-15,-20] #室外温度
T = 24 * 60 * 60 * np.array([30,40,40,40,30])
k_length = len(theta_out0)
total_energy = np.zeros(k_length)
total_kwh = np.zeros(k_length)
time_8_21_kwh = np.zeros(k_length)
time_other_kwh = np.zeros(k_length)
price = np.zeros(k_length)

for k in range(k_length):
    t = np.arange(0, T[k]+dt, dt)
    N = len(t) #求解点数
    P_heat = np.zeros(N) #初始化P_heat
    U = np.zeros((2,N)) #初始化U
    X = np.zeros((2,N)) #初始化X

    theta_wall0 = (theta_in0 + theta_out0[k]) / 2 #假设墙体初始温度等于室内温度与室外温度的平均
    theta_out = theta_out0[k] * np.ones(N)
    U[0,:] = P_heat
    U[1,:] = theta_out
    X[:,0] = [theta_in0, theta_wall0]
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
    plt.savefig(f'img/问题1.3室外温度为{theta_out0[k]}时的30天室内温度和墙体温度变化.png', dpi=300)
    plt.show()

    plt.plot(t/60,U[0,:])
    plt.grid()
    plt.ylabel('制热功率')
    plt.xlabel('时间/min')
    plt.savefig(f'img/问题1.3室外温度为{theta_out0[k]}时的30天制热功率.png', dpi=300)
    plt.show()

    P_heat = U[0,:]
    total_energy[k] = np.sum(P_heat * dt)
    total_kwh[k] = total_energy[k] / 3600000 #用电量（kwh）
    time_8_21_index = np.arange(8*60*60//dt, 21*60*60//dt+1)
    time_other_index = np.concatenate((np.arange(8*60*60//dt), np.arange(21*60*60//dt, 24*60*60//dt+1)))
    for j in range(1, T[k]//(24*60*60)+1):
        time_8_21_index = np.concatenate((time_8_21_index, (j-1)*24*60 + np.arange(8*60*60//dt, 21*60*60//dt+1))) #8点-21点
        time_other_index = np.concatenate((time_other_index, (j-1)*24*60 + np.concatenate((np.arange(8*60*60//dt), np.arange(21*60*60//dt, 24*60*60//dt+1))))) #0-8点,21-8点

    time_8_21_kwh[k] = np.sum(P_heat[time_8_21_index] * dt) / 3600000
    time_other_kwh[k] = np.sum(P_heat[time_other_index] * dt) / 3600000
    price[k] = time_8_21_kwh[k] * 0.56 + time_other_kwh[k] * 0.32 #用电成本

problem1_3_data = pd.DataFrame({'theta_out0': theta_out0, 'T': T // (24*60*60), 'total_kwh': total_kwh, 'price': price})
problem1_3_data.to_excel('问题1.3结果.xlsx', index=False)