import os
import numpy as np
import matplotlib.pyplot as plt
from functions_copy import get_T_fu, get_h_air_wd, get_lambda_wd, get_rho_c_wd, get_lambda_wd_0, get_rho_c_wd_0
from config import N_CELL, T_0_WD, T_AIR, ALPHA_WD, D_t, D_X, q_FU, q_GEN, N_TIME, LENGTH, RHO_WD_0

fig_number = 8
#フォルダ
# folder_name = '100℃一定'
folder_name = '標準加熱曲線'
#グラフタイトル
# fig_title = '標準加熱曲線'
# fig_title = '温度推移'
# fig_title = '温度分布'
#比較
comparison = '密度'
# fig_title = '加熱面の温度推移'
# fig_title = '加熱面から 5 mmの温度推移'
fig_title = '加熱終了時の温度分布'

if fig_title == '温度推移' or fig_title == '加熱面の温度推移' or fig_title == '加熱面から 5 mmの温度推移':
    x_name = '時間 (s)'
    y_name = '温度 (℃)'
    x_axis = []
if fig_title == '温度分布' or fig_title == '加熱終了時の温度分布':
    x_name = '位置$ \mathit{x} $ (m)'
    y_name = '温度 (℃)'
    x_axis = np.arange(0.0, LENGTH + D_X, D_X)
y_axis_1 = []
y_axis_2 = []
y_axis_3 = []
y_axis_4 = []

###温度算出1
RHO_WD_0 = 250
for n in range(N_TIME + 1):
    t = n * D_t  #現実の経過時間
    if folder_name == '100℃一定':
        T_fu = 100
    if folder_name == '標準加熱曲線':
        T_fu = get_T_fu(t)

    if fig_title == '温度推移' or fig_title == '加熱面の温度推移' or fig_title == '加熱面から 5 mmの温度推移':
        x_axis.append(t)

    if n == 0:
        print('start')
        #木材温度の初期化
        T_wd = np.array([[T_0_WD] * (N_CELL + 1)] * (N_TIME + 1))
        #T_wd[t:経過時間(0秒~)][x:場所0m~]
    else:
        for x in range(N_CELL + 1):
            h_air = get_h_air_wd(T_wd[n - 1][0])
            if T_wd[n - 1][x] <= 100:
                lambda_wd = get_lambda_wd(RHO_WD_0, T_wd[n][x])
                rho_c_wd = get_rho_c_wd(RHO_WD_0, T_wd[n - 1][x])
            else:
                lambda_wd = get_lambda_wd_0(RHO_WD_0, T_wd[n][x])
                rho_c_wd = get_rho_c_wd_0(RHO_WD_0, T_wd[n - 1][x])

            if x == 0:
                #y_axis.append(h_air)
                T_wd[n][0] = T_wd[n - 1][0] + (ALPHA_WD * D_t / (D_X**2)) * (T_wd[n - 1][1] - T_wd[
                    n - 1][0]) + (D_t * h_air / (D_X * rho_c_wd)) * (T_fu - T_wd[n - 1][0]) + (
                        D_t * q_FU) / (D_X * rho_c_wd) + (D_t * q_GEN) / rho_c_wd
            elif 0 < x < N_CELL:
                T_wd[n][x] = T_wd[n - 1][x] + (ALPHA_WD * D_t / (D_X**2)) * (T_wd[n - 1][
                    x - 1] + T_wd[n - 1][x + 1] - 2 * T_wd[n - 1][x]) + (D_t * q_GEN) / rho_c_wd
            elif x == N_CELL:
                T_wd[n][N_CELL] = T_wd[n - 1][N_CELL] + (ALPHA_WD * D_t / (D_X**2)) * (
                    T_wd[n - 1][N_CELL - 1] - T_wd[n - 1][N_CELL]) - (
                        D_t * h_air /
                        (D_X * rho_c_wd)) * (T_wd[n - 1][N_CELL] - T_AIR) + (D_t * q_GEN) / rho_c_wd

    if folder_name == '100℃一定':
        if fig_title == '温度推移' or fig_title == '加熱面の温度推移':
            y_axis_1.append(T_wd[n][0])
        if fig_title == '加熱面から 5 mmの温度推移':
            y_axis_1.append(T_wd[n][5])
    if folder_name == '標準加熱曲線':
        if fig_title == '温度推移' or fig_title == '加熱面の温度推移':
            y_axis_1.append(T_wd[n][0])
        if fig_title == '加熱面から 5 mmの温度推移':
            y_axis_1.append(T_wd[n][5])

if folder_name == '100℃一定':
    if fig_title == '温度分布' or fig_title == '加熱終了時の温度分布':
        y_axis_1 = T_wd[N_TIME]
if folder_name == '標準加熱曲線':
    if fig_title == '温度分布' or fig_title == '加熱終了時の温度分布':
        y_axis_1 = T_wd[N_TIME]
###温度算出1

###温度算出2
RHO_WD_0 = 350
for n in range(N_TIME + 1):
    t = n * D_t  #現実の経過時間
    if folder_name == '100℃一定':
        T_fu = 100
    if folder_name == '標準加熱曲線':
        T_fu = get_T_fu(t)

    if n == 0:
        print('start')
        #木材温度の初期化
        T_wd = np.array([[T_0_WD] * (N_CELL + 1)] * (N_TIME + 1))
        #T_wd[t:経過時間(0秒~)][x:場所0m~]
    else:
        for x in range(N_CELL + 1):
            h_air = get_h_air_wd(T_wd[n - 1][0])
            if T_wd[n - 1][x] <= 100:
                lambda_wd = get_lambda_wd(RHO_WD_0, T_wd[n][x])
                rho_c_wd = get_rho_c_wd(RHO_WD_0, T_wd[n - 1][x])
            else:
                lambda_wd = get_lambda_wd_0(RHO_WD_0, T_wd[n][x])
                rho_c_wd = get_rho_c_wd_0(RHO_WD_0, T_wd[n - 1][x])

            if x == 0:
                #y_axis.append(h_air)
                T_wd[n][0] = T_wd[n - 1][0] + (ALPHA_WD * D_t / (D_X**2)) * (T_wd[n - 1][1] - T_wd[
                    n - 1][0]) + (D_t * h_air / (D_X * rho_c_wd)) * (T_fu - T_wd[n - 1][0]) + (
                        D_t * q_FU) / (D_X * rho_c_wd) + (D_t * q_GEN) / rho_c_wd
            elif 0 < x < N_CELL:
                T_wd[n][x] = T_wd[n - 1][x] + (ALPHA_WD * D_t / (D_X**2)) * (T_wd[n - 1][
                    x - 1] + T_wd[n - 1][x + 1] - 2 * T_wd[n - 1][x]) + (D_t * q_GEN) / rho_c_wd
            elif x == N_CELL:
                T_wd[n][N_CELL] = T_wd[n - 1][N_CELL] + (ALPHA_WD * D_t / (D_X**2)) * (
                    T_wd[n - 1][N_CELL - 1] - T_wd[n - 1][N_CELL]) - (
                        D_t * h_air /
                        (D_X * rho_c_wd)) * (T_wd[n - 1][N_CELL] - T_AIR) + (D_t * q_GEN) / rho_c_wd

    if folder_name == '100℃一定':
        if fig_title == '温度推移' or fig_title == '加熱面の温度推移':
            y_axis_2.append(T_wd[n][0])
        if fig_title == '加熱面から 5 mmの温度推移':
            y_axis_2.append(T_wd[n][5])
    if folder_name == '標準加熱曲線':
        if fig_title == '温度推移' or fig_title == '加熱面の温度推移':
            y_axis_2.append(T_wd[n][0])
        if fig_title == '加熱面から 5 mmの温度推移':
            y_axis_2.append(T_wd[n][5])

if folder_name == '100℃一定':
    if fig_title == '温度分布' or fig_title == '加熱終了時の温度分布':
        y_axis_2 = T_wd[N_TIME]
if folder_name == '標準加熱曲線':
    if fig_title == '温度分布' or fig_title == '加熱終了時の温度分布':
        y_axis_2 = T_wd[N_TIME]
###温度算出2

###温度算出3
RHO_WD_0 = 450
for n in range(N_TIME + 1):
    t = n * D_t  #現実の経過時間
    if folder_name == '100℃一定':
        T_fu = 100
    if folder_name == '標準加熱曲線':
        T_fu = get_T_fu(t)

    if n == 0:
        print('start')
        #木材温度の初期化
        T_wd = np.array([[T_0_WD] * (N_CELL + 1)] * (N_TIME + 1))
        #T_wd[t:経過時間(0秒~)][x:場所0m~]
    else:
        for x in range(N_CELL + 1):
            h_air = get_h_air_wd(T_wd[n - 1][0])
            if T_wd[n - 1][x] <= 100:
                lambda_wd = get_lambda_wd(RHO_WD_0, T_wd[n][x])
                rho_c_wd = get_rho_c_wd(RHO_WD_0, T_wd[n - 1][x])
            else:
                lambda_wd = get_lambda_wd_0(RHO_WD_0, T_wd[n][x])
                rho_c_wd = get_rho_c_wd_0(RHO_WD_0, T_wd[n - 1][x])

            if x == 0:
                #y_axis.append(h_air)
                T_wd[n][0] = T_wd[n - 1][0] + (ALPHA_WD * D_t / (D_X**2)) * (T_wd[n - 1][1] - T_wd[
                    n - 1][0]) + (D_t * h_air / (D_X * rho_c_wd)) * (T_fu - T_wd[n - 1][0]) + (
                        D_t * q_FU) / (D_X * rho_c_wd) + (D_t * q_GEN) / rho_c_wd
            elif 0 < x < N_CELL:
                T_wd[n][x] = T_wd[n - 1][x] + (ALPHA_WD * D_t / (D_X**2)) * (T_wd[n - 1][
                    x - 1] + T_wd[n - 1][x + 1] - 2 * T_wd[n - 1][x]) + (D_t * q_GEN) / rho_c_wd
            elif x == N_CELL:
                T_wd[n][N_CELL] = T_wd[n - 1][N_CELL] + (ALPHA_WD * D_t / (D_X**2)) * (
                    T_wd[n - 1][N_CELL - 1] - T_wd[n - 1][N_CELL]) - (
                        D_t * h_air /
                        (D_X * rho_c_wd)) * (T_wd[n - 1][N_CELL] - T_AIR) + (D_t * q_GEN) / rho_c_wd

    if folder_name == '100℃一定':
        if fig_title == '温度推移' or fig_title == '加熱面の温度推移':
            y_axis_3.append(T_wd[n][0])
        if fig_title == '加熱面から 5 mmの温度推移':
            y_axis_3.append(T_wd[n][5])
    if folder_name == '標準加熱曲線':
        if fig_title == '温度推移' or fig_title == '加熱面の温度推移':
            y_axis_3.append(T_wd[n][0])
        if fig_title == '加熱面から 5 mmの温度推移':
            y_axis_3.append(T_wd[n][5])

if folder_name == '100℃一定':
    if fig_title == '温度分布' or fig_title == '加熱終了時の温度分布':
        y_axis_3 = T_wd[N_TIME]
if folder_name == '標準加熱曲線':
    if fig_title == '温度分布' or fig_title == '加熱終了時の温度分布':
        y_axis_3 = T_wd[N_TIME]
###温度算出3

###グラフ設定
##図の形式
#文字
plt.rcParams['font.family'] = 'MS Gothic'  #使用するフォント
plt.rcParams['font.size'] = 16  #フォントの大きさ
#目盛線
plt.rcParams['xtick.direction'] = 'in'  #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'  #y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
#枠線
plt.gca().spines['top'].set_visible(False)  #上の枠線を削除
plt.gca().spines['right'].set_visible(False)  #右の枠線を削除
#位置
plt.subplots_adjust(bottom=0.22)  #図の位置(上下)を変更
#軸ラベル
plt.xlabel(x_name)  #x軸ラベル
plt.ylabel(y_name)  #y軸ラベル
#タイトル
# plt.title('図' + str(fig_number) + '　' + fig_title, y=-0.30)
plt.title(fig_title, y=-0.30)  #図番号表記なし（発表スライド用）

if folder_name == '100℃一定':
    if fig_title == '温度推移' or fig_title == '加熱面の温度推移' or fig_title == '加熱面から 5 mmの温度推移':
        #軸範囲
        plt.xlim(0, 5400)  #x軸範囲
        plt.ylim(20, 100)  #y軸範囲
        #プロット
        plt.plot(x_axis, y_axis_1, "-.r", label='炉内')  #(x, y, fmt), fmt = '[marker][line][color]'
        plt.plot(x_axis, y_axis_2, "-c", label='左端（$ \mathit{x} $=0.000）')
        plt.plot(x_axis, y_axis_3, "--g", label='中央（$ \mathit{x} $=0.025）')
        plt.plot(x_axis, y_axis_4, ":k", label='右端（$ \mathit{x} $=0.050）')
        plt.legend(frameon=False)  #凡例（フレーム非表示）
    if fig_title == '温度分布' or fig_title == '加熱終了時の温度分布':
        #軸範囲
        plt.xlim(0.00, 0.05)  #x軸範囲
        plt.ylim(15, 100)  #y軸範囲
        #プロット
        plt.plot(x_axis, y_axis_1, "-r", label='0.0 h')  #(x, y, fmt), fmt = '[marker][line][color]'
        plt.plot(x_axis, y_axis_2, "--b", label='1.0 h')
        plt.plot(x_axis, y_axis_3, ":g", label='1.5 h')
        plt.legend(frameon=False)  #凡例（フレーム非表示）

if folder_name == '標準加熱曲線':
    if fig_title == '温度推移' or fig_title == '加熱面の温度推移':
        #軸範囲
        plt.xlim(0, 50)  #x軸範囲
        plt.ylim(20, 100)  #y軸範囲
        #プロット
        plt.plot(x_axis, y_axis_1, "-r",
                 label='全乾密度：250 kg/m³')  #(x, y, fmt), fmt = '[marker][line][color]'
        plt.plot(x_axis, y_axis_2, "--b", label='全乾密度：350 kg/m³')
        plt.plot(x_axis, y_axis_3, ":g", label='全乾密度：450 kg/m³')
        plt.legend(frameon=False)  #凡例（フレーム非表示）
    if fig_title == '加熱面から 5 mmの温度推移':
        #軸範囲
        plt.xlim(0, 50)  #x軸範囲
        plt.ylim(20, 27)  #y軸範囲
        #プロット
        plt.plot(x_axis, y_axis_1, "-r",
                 label='全乾密度：250 kg/m³')  #(x, y, fmt), fmt = '[marker][line][color]'
        plt.plot(x_axis, y_axis_2, "--b", label='全乾密度：350 kg/m³')
        plt.plot(x_axis, y_axis_3, ":g", label='全乾密度：450 kg/m³')
        plt.legend(frameon=False)  #凡例（フレーム非表示）
    if fig_title == '温度分布' or fig_title == '加熱終了時の温度分布':
        #軸範囲
        plt.xlim(0.00, 0.05)  #x軸範囲
        plt.ylim(15, 100)  #y軸範囲
        #プロット
        plt.plot(x_axis, y_axis_1, "-r",
                 label='全乾密度：250 kg/m³')  #(x, y, fmt), fmt = '[marker][line][color]'
        plt.plot(x_axis, y_axis_2, "--b", label='全乾密度：350 kg/m³')
        plt.plot(x_axis, y_axis_3, ":g", label='全乾密度：450 kg/m³')
        plt.legend(frameon=False)  #凡例（フレーム非表示）

# plt.rcParams['xtick.major.width'] = 1.0#x軸主目盛り線の線幅
# plt.rcParams['ytick.major.width'] = 1.0#y軸主目盛り線の線幅
# plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge linewidth。囲みの太さ

folder = "ver2/4_発表本番/" + folder_name + "/"
# file_path = "images/" + folder + folder_name + fig_title
file_path = "images/" + folder + folder_name + '_' + fig_title
os.makedirs("images/" + folder, exist_ok=True)
plt.savefig(file_path.replace('.', '_'), bbox_inches="tight")
plt.show()