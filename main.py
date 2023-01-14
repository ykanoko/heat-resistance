import numpy as np
import matplotlib.pyplot as plt
from functions import get_T_fu, get_h_air_wd, get_lambda_wd, get_rho_c_wd, get_lambda_wd_0, get_rho_c_wd_0
from config import N_CELL, T_0_WD, ALPHA_WD, D_t, D_X, q_FU, q_GEN, N_TIME, LENGTH, TIME_END

x_axis = np.arange(0.0, LENGTH + D_X, D_X)

# x_axis = []
y_axis = []

for n in range(N_TIME + 1):
    t = n * D_t  #現実の経過時間
    # x_axis.append(t)
    T_fu = get_T_fu(t)
    # y_axis.append(T_fu)
    if n == 0:
        print('start')
        #木材温度の初期化
        T_wd = np.array([[T_0_WD] * (N_CELL + 1)] * (N_TIME + 1))
        #T_wd[t:経過時間(0秒~)][x:場所0m~]
    else:
        for x in range(N_CELL + 1):

            h_air = get_h_air_wd(T_wd[n - 1][x])
            if T_wd[n - 1][x] <= 100:
                lambda_wd = get_lambda_wd(T_wd[n - 1][x])
                rho_c_wd = get_rho_c_wd(T_wd[n - 1][x])
            else:
                lambda_wd = get_lambda_wd_0(T_wd[n - 1][x])
                rho_c_wd = get_rho_c_wd_0(T_wd[n - 1][x])

            if x == 0:
                T_wd[n][0] = T_wd[n - 1][0] + (ALPHA_WD * D_t / (D_X**2)) * (T_wd[n - 1][1] - T_wd[
                    n - 1][0]) + (D_t * h_air / (D_X * rho_c_wd)) * (T_fu - T_wd[n - 1][0]) + (
                        D_t * q_FU) / (D_X * rho_c_wd) + (D_t * q_GEN) / rho_c_wd
                #DO:差分法の実例がある本探す　#iPadで算出した左はじの式 TODO:内部発熱(最後の項）を考慮する（炭化について）TODO:輻射（最後から2番目の項）の考え方、おそらく違うので再考
            elif 0 < x < N_CELL:
                T_wd[n][x] = T_wd[n - 1][x] + (ALPHA_WD * D_t / (D_X**2)) * (T_wd[n - 1][
                    x - 1] + T_wd[n - 1][x + 1] - 2 * T_wd[n - 1][x]) + (D_t * q_GEN) / rho_c_wd
                #TODO:内部発熱(最後の項）を考慮する（炭化について）
            elif x == N_CELL:
                T_wd[n][N_CELL] = T_wd[n - 1][N_CELL] + (ALPHA_WD * D_t / (D_X**2)) * (
                    T_wd[n - 1][N_CELL - 1] - T_wd[n - 1][N_CELL]
                ) - (D_t * h_air /
                     (D_X * rho_c_wd)) * (T_wd[n - 1][N_CELL] - T_0_WD) + (D_t * q_GEN) / rho_c_wd
                #TODO:内部発熱(最後の項）を考慮する（炭化について）DO:難燃処理層最後尾の次をどう考えるか（荷重支持部表面？長田さんは炉内温度？一面加熱だから、布施さんの外温と同じ？）
    # y_axis.append(T_wd[n][10])
    # print(t, T_fu, T_wd[n])
    #print(T_wd)
y_axis = T_wd[N_TIME]

plt.plot(x_axis, y_axis, "b:")
plt.show()
#T_1_wd[0] = T_0_wd[0] + (ALPHA_WD * D_t / D_X**2) * (T_0_wd[1] + D_X * h_air / lambda_wd * T_fu - (1 + (D_X * h_air / lambda_wd)) * T_0_wd[0] + ((D_X**2) / lambda_wd) * q_GEN + (D_X / lambda_wd) * q_FU)
#iPadで算出した空気から木材への流入における式 TODO内部発熱(最後から2番目の項）を0とした場合（炭化前？）
# T_1_wd[1] = T_0_wd[1] + (ALPHA_WD * D_t / (D_X**2)) * (T_0_wd[0] + T_0_wd[2] - 2 * T_0_wd[1]) + (D_t * q_GEN) / rho_c_wd

# print(T_1_wd)

#for x in range(N_CELL):

#x = np.arange(0.0, 120.0 * 60, 1.0)
# plt.plot(x, T_fu(x), 'b:')
# plt.show()
