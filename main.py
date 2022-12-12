from math import log10
import numpy as np
import matplotlib.pyplot as plt
from functions import get_T_fu, get_h_air_wd, get_lambda_wd, get_rho_c_wd
from config import N_CELL, T_0_WD, ALPHA_WD, D_t, D_X, q_FU, q_GEN

t = 0  # time秒
T_fu = get_T_fu(t)  # 炉内温度℃

#木材の初期化
T_0_wd = np.array([T_0_WD] * N_CELL)
T_1_wd = np.array([0] * N_CELL)
T_1_wd2 = np.array([0] * N_CELL)
h_air = get_h_air_wd(T_0_wd[0])
lambda_wd = get_lambda_wd(T_0_wd[0])
rho_c_wd = get_rho_c_wd(T_0_wd[0])
T_fu = get_T_fu(0)
print(lambda_wd, h_air)
print((D_X / lambda_wd) * q_FU)
print(ALPHA_WD * D_t / D_X**2)
#T_1_wd[0] = T_0_wd[0] + (ALPHA_WD * D_t / D_X**2) * (T_0_wd[1] + D_X * h_air / lambda_wd * T_fu - (1 + (D_X * h_air / lambda_wd)) * T_0_wd[0] + ((D_X**2) / lambda_wd) * q_GEN + (D_X / lambda_wd) * q_FU)
#iPadで算出した空気から木材への流入における式 TODO:内部発熱(最後から2番目の項）を0とした場合（炭化前？）
T_1_wd2[0] = T_0_wd[0] + (ALPHA_WD * D_t / (D_X**2)) * (T_0_wd[1] - T_0_wd[0]) + (D_t * h_air / (D_X * rho_c_wd)) * (T_fu - T_0_wd[0]) + D_t * q_FU / (D_X * rho_c_wd) + D_t * q_GEN / rho_c_wd
#iPadで算出した左はじの式 TODO:内部発熱(最後の項）を考慮する（炭化について）TODO:輻射（最後から2番目の項）の考え方、おそらく違うので再考

print(T_0_wd)
print(T_1_wd)
print(T_1_wd2)
#for x in range(N_CELL):

#x = np.arange(0.0, 120.0 * 60, 1.0)
# plt.plot(x, T_fu(x), 'b:')
# plt.show()
