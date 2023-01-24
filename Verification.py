import os
import numpy as np
import matplotlib.pyplot as plt
from functions import get_T_fu, get_h_air_wd, get_lambda_wd, get_rho_c_wd, get_lambda_wd_0, get_rho_c_wd_0
from config import N_CELL, T_0_WD, ALPHA_WD, D_t, D_X, q_FU, q_GEN, N_TIME, LENGTH, RHO_WD_0

# fig_title = '標準加熱曲線'
# fig_title = '温度推移(x=0)'
fig_title = '温度推移(x=0.005)'
# fig_title = '木材内温度分布(t=50)'
# fig_title == '熱伝達率の推移'

if fig_title == '標準加熱曲線':
    fig_number = 1
    x_name = '時間 (s)'
    y_name = '温度 (℃)'
if fig_title == '温度推移(x=0)':
    fig_number = 6
    x_name = '時間 (s)'
    y_name = '温度 (℃)'
if fig_title == '温度推移(x=0.005)':
    fig_number = 7
    x_name = '時間 (s)'
    y_name = '温度 (℃)'
if fig_title == '木材内温度分布(t=50)':
    fig_number = 10
    x_name = '位置x (m)'
    y_name = '温度 (℃)'

if fig_title == '熱伝達率の推移':
    x_name = '時間 (s)'
    y_name = '熱伝達率 (W・m⁻²・K⁻¹)'
# fig_title=''

if fig_title == '木材内温度分布(t=50)':
    x_axis = np.arange(0.0, LENGTH + D_X, D_X)
if fig_title == '標準加熱曲線' or fig_title == '温度推移(x=0)' or fig_title == '温度推移(x=0.005)':
    x_axis = []
y_axis = []

for n in range(N_TIME + 1):
    t = n * D_t  #現実の経過時間
    if fig_title == '標準加熱曲線' or fig_title == '温度推移(x=0)' or fig_title == '温度推移(x=0.005)':
        x_axis.append(t)
    T_fu = get_T_fu(t)
    if fig_title == '標準加熱曲線':
        y_axis.append(T_fu)
    if n == 0:
        print('start')
        #y_axis.append(8.0)
        # y_axis.append(0.09)
        #木材温度の初期化
        T_wd = np.array([[T_0_WD] * (N_CELL + 1)] * (N_TIME + 1))
        #T_wd[t:経過時間(0秒~)][x:場所0m~]
    else:
        for x in range(N_CELL + 1):
            h_air = get_h_air_wd(T_wd[n - 1][0])
            if T_wd[n - 1][x] <= 100:
                lambda_wd = get_lambda_wd(T_wd[n][x])
                rho_c_wd = get_rho_c_wd(T_wd[n - 1][x])
            else:
                lambda_wd = get_lambda_wd_0(T_wd[n][x])
                rho_c_wd = get_rho_c_wd_0(T_wd[n - 1][x])

            if x == 0:
                #y_axis.append(h_air)
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
                #DO:試験体の厚さを十分厚くすれば、非加熱面の状態を考慮しなくていい
                #TODO:内部発熱(最後の項）を考慮する（炭化について）DO:難燃処理層最後尾の次をどう考えるか（荷重支持部表面？長田さんは炉内温度？一面加熱だから、布施さんの外温と同じ？）

            # if fig_title == '':
            #     if x == 10:
            #         y_axis.append(lambda_wd)
    if fig_title == '温度推移(x=0)':
        y_axis.append(T_wd[n][0])
    if fig_title == '温度推移(x=0.005)':
        y_axis.append(T_wd[n][5])
    # print(t, T_fu, T_wd[n])
    #print(T_wd)
# print(T_wd)
if fig_title == '木材内温度分布(t=50)':
    y_axis = T_wd[N_TIME]

##グラフ設定
plt.rcParams['font.family'] = 'MS Gothic'  #使用するフォント
plt.rcParams['font.size'] = 16  #フォントの大きさ
plt.xlabel(x_name)  #x軸
plt.ylabel(y_name)  #y軸
plt.title('図' + str(fig_number) + '　' + fig_title, y=-0.30)  #タイトル
if RHO_WD_0 != 350.0:
    plt.title('図' + str(fig_number) + '　' + fig_title + '(d₀=' + str(RHO_WD_0) + ')', y=-0.30)

plt.gca().spines['top'].set_visible(False)  #上の枠線を削除
plt.gca().spines['right'].set_visible(False)  #右の枠線を削除
plt.rcParams['xtick.direction'] = 'in'  #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'  #y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.subplots_adjust(bottom=0.22)  #図の位置(上下)を変更

plt.plot(x_axis, y_axis, '-', color="black")  #図のプロット
# plt.rcParams['xtick.major.width'] = 1.0#x軸主目盛り線の線幅
# plt.rcParams['ytick.major.width'] = 1.0#y軸主目盛り線の線幅
# plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge linewidth。囲みの太さ

folder = "ver2/体裁修正後/"
file_path = "images/" + folder + fig_title
if RHO_WD_0 != 350.0:
    file_path = "images/" + folder + fig_title + '密度' + str(RHO_WD_0)
os.makedirs("images/" + folder, exist_ok=True)
plt.savefig(file_path.replace('.', '_'), bbox_inches="tight")
plt.show()