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
day_num = 30 #30天
T = day_num * 24 * 60 * 60
dt = 60 #60s,1min
t = np.arange(0, T+dt, dt)
N = len(t) #求解点数
Ad = np.eye(2) + A * dt #离散化
Bd = B * dt
theta_in0 = 20 #室内初始温度
theta_out0 = [0,-5,-10,-15,-20,-25] #室外温度

k_length = len(theta_out0)
period = np.zeros(k_length)
duty_ratio = np.zeros(k_length)
P_heat = np.zeros((k_length,N)) #初始化P_heat
U = np.zeros((2,N,k_length)) #初始化U
X = np.zeros((2,N,k_length)) #初始化X
for k in range(k_length):
    theta_wall0 = (theta_in0 + theta_out0[k]) / 2 #假设墙体初始温度等于室内温度与室外温度的平均
    theta_out = theta_out0[k] * np.ones(N)
    P_heat[k,:] = np.zeros(N) #初始化对应的P_heat
    U[0,:,k] = P_heat[k,:]
    U[1,:,k] = theta_out
    X[:,0,k] = [theta_in0, theta_wall0]
    for i in range(1,N):
        if X[0,i-1,k] > 22:
            U[0,i,k] = 0 #如果大于22，关闭
        elif X[0,i-1,k] < 18:
            U[0,i,k] = Pn #如果小于18，开启
        else:
            U[0,i,k] = U[0,i-1,k] #如果在区间内，保持上一次的制热功率不变

        X[:,i,k] = Ad @ X[:,i-1,k] + Bd @ U[:,i,k]

    u = U[0,:,k] == Pn
    # [period[k], duty_ratio[k]] = get_period(u) # get_period function is not defined in the given MATLAB code
    # print(f'室外温度为{theta_out0[k]}的稳态周期为{period[k]}分钟')
    # print(f'室外温度为{theta_out0[k]}的稳态占空比为{duty_ratio[k]}')

    plt.plot(t/60,X[:,:,k].T)
    plt.grid()
    plt.legend(['室内温度', '墙体温度'])
    plt.ylabel('温度')
    plt.xlabel('时间/min')
    plt.savefig(f'img/问题1.2室外温度为{theta_out0[k]}时的30天室内温度和墙体温度变化.png', dpi=300)
    plt.show()

    plt.plot(t/60,U[0,:,k])
    plt.grid()
    plt.ylabel('制热功率')
    plt.xlabel('时间/min')
    plt.savefig(f'img/问题1.2室外温度为{theta_out0[k]}时的30天制热功率.png', dpi=300)
    plt.show()

index_cut = (day_num-1) * 24 * 60 * 60 // dt + np.arange(len(np.arange(0, 24*60*60+dt, dt))) #切分出最后1天的稳态数据

X_cut = X[:,index_cut,:]
U_cut = U[:,index_cut,:]
for k in range(k_length):
    plt.plot(t[index_cut]/60,X_cut[:,:,k].T)
    plt.grid()
    plt.legend(['室内温度', '墙体温度'])
    plt.ylabel('温度')
    plt.xlabel('时间/min')
    plt.savefig(f'img/问题1.2室外温度为{theta_out0[k]}时的稳态1天室内温度和墙体温度变化.png', dpi=300)
    plt.show()

    plt.plot(t[index_cut]/60,U_cut[0,:,k])
    plt.grid()
    plt.ylabel('制热功率')
    plt.xlabel('时间/min')
    plt.savefig(f'img/问题1.2室外温度为{theta_out0[k]}时的稳态1天制热功率.png', dpi=300)
    plt.show()

P_heat_cut = np.reshape(U_cut[0,:,:], (len(index_cut), k_length))
up_time = np.zeros(k_length)
down_time = np.zeros(k_length)
total_energy = np.zeros(k_length)
avg_power = np.zeros(k_length)
total_kwh = np.zeros(k_length)
avg_power_kW = np.zeros(k_length)
time_8_21_kwh = np.zeros(k_length)
time_other_kwh = np.zeros(k_length)
price = np.zeros(k_length)

for k in range(k_length):
    up_time[k] = np.sum((P_heat_cut[:,k] > 0) * dt) / 60 #升温时长（min）
    down_time[k] = np.sum((P_heat_cut[:,k] == 0) * dt) / 60 #降温时长（min）
    total_energy[k] = np.sum(P_heat_cut[:,k] * dt) #总用电量（J=W*s），1 千瓦时 = 3600000 焦耳
    avg_power[k] = total_energy[k] / (24 * 60 * 60) #平均功率（W）
    total_kwh[k] = total_energy[k] / 3600000 #总用电量（kwh）
    avg_power_kW[k] = avg_power[k] / 1000 #平均功率（kW）
    time_8_21_index = np.arange(8*60*60//dt, 21*60*60//dt+1) #8点-21点
    time_other_index = np.concatenate((np.arange(8*60*60//dt), np.arange(21*60*60//dt, len(index_cut)))) #0-8点,21-8点
    time_8_21_kwh[k] = np.sum(P_heat_cut[time_8_21_index,k] * dt) / 3600000
    time_other_kwh[k] = np.sum(P_heat_cut[time_other_index,k] * dt) / 3600000
    price[k] = time_8_21_kwh[k] * 0.56 + time_other_kwh[k] * 0.32 #用电成本

problem1_2_data = pd.DataFrame({'theta_out0': theta_out0, 'up_time': up_time, 'down_time': down_time,
                                'period': period, 'duty_ratio': duty_ratio, 'total_kwh': total_kwh,
                                'avg_power_kW': avg_power_kW, 'price': price})
problem1_2_data.to_excel('问题1.2结果.xlsx', index=False)