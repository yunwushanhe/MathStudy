import numpy as np
import matplotlib.pyplot as plt

R1 = 1.2e-3
R2 = 9.2e-3
C_in = 1.1e6
C_wall = 1.86e8
Pn = 8e3
A = np.array([[-1 / (R1 * C_in), 1 / (R1 * C_in)],
              [1 / (R1 * C_wall), -1 / (R1 * C_wall) - 1 / (R2 * C_wall)]])
B = np.array([[1 / C_in, 0],
              [0, 1 / (R2 * C_wall)]])

day_num = 30
T = day_num * 24 * 60 * 60
dt = 60
t = np.arange(0, T, dt)
N = len(t)

Ad = np.eye(2) + A * dt
Bd = B * dt

theta_in0 = np.linspace(18, 22, 600)
theta_out = [0, -5, -10, -15, -20, -25]

for theta_out0 in theta_out:
    k_length = len(theta_in0)
    P_heat = np.zeros((k_length, N))
    U = np.zeros((2, N, k_length))
    X = np.zeros((2, N, k_length))

    for k in range(k_length):
        theta_wall0 = (theta_in0[k] + theta_out0) / 2
        theta_out = theta_out0 * np.ones(N)
        P_heat[k] = np.zeros(N)
        P_heat[k, 0] = 0
        U[:, :, k] = [P_heat[k], theta_out]
        X[:, 0, k] = [theta_in0[k], theta_wall0]

        for i in range(1, N):
            if X[0, i - 1, k] > 22:
                U[0, i, k] = 0
            elif X[0, i - 1, k] < 18:
                U[0, i, k] = Pn
            else:
                U[0, i, k] = U[0, i - 1, k]

            X[:, i, k] = Ad @ X[:, i - 1, k] + Bd @ U[:, i, k]

    index_cut = (day_num - 1) * 24 * 60 * 60 / dt + np.arange(1, 24 * 60 * 60 / dt + 1)
    X_cut = X[:, index_cut, :]
    U_cut = U[:, index_cut, :]

    P_heat_cut = np.reshape(U_cut[0, :, :], (len(index_cut), k_length))
    P_heat_sum = np.sum(P_heat_cut, axis=1)
    plt.figure()
    plt.plot(t[index_cut] / 60, P_heat_sum)
    plt.ylabel('总用电功率')
    plt.xlabel('时间/min')
    plt.savefig('img/问题4.1室外温度为{}.png'.format(theta_out0), dpi=300)
    plt.show()

    p = P_heat_cut > 0
    np.savetxt('data/问题4.1室外温度为{}.txt'.format(theta_out0), p, fmt='%i')

    p = P_heat_cut == 0
    np.savetxt('data/问题4.1室外温度为{}.txt'.format(theta_out0), p, fmt='%i')