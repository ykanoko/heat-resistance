import os
import numpy as np
import matplotlib.pyplot as plt
from functions import get_T_fu, get_h_air_wd, get_lambda_wd, get_rho_c_wd, get_lambda_wd_0, get_rho_c_wd_0
from config import N_CELL, T_0_WD, T_AIR, ALPHA_WD, D_t, D_X, q_FU, q_GEN, N_TIME, LENGTH, RHO_WD_0, TIME_END

fig_number = 6
#フォルダ
# folder_name = '100℃一定片面'
# folder_name = '100℃一定両面'
folder_name = '標準加熱曲線'
if folder_name == '100℃一定両面':
    T_AIR = 100  #[℃]
if folder_name == '標準加熱曲線':
    TIME_END = 50  #[s]
    N_TIME = int(TIME_END / D_t)  #[個]　秒の区切りの個数、0秒を入れる場合は+1する

#グラフタイトル
# fig_title = '標準加熱曲線'
# fig_title = '温度推移'
fig_title = '温度分布'
#比較
# comparison = '密度'
# fig_title = '加熱面の温度推移'
# fig_title = '加熱終了時の温度分布'

if fig_title == '温度推移' or fig_title == '加熱面の温度推移':
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

#個々のグラフ作成
# fig_title = '温度推移(x=0)'
# fig_title = '温度推移(x=0.005)'
# fig_title = '温度分布(t=50)'
# fig_title == '熱伝達率の推移'
if fig_title == '標準加熱曲線' or fig_title == '温度推移(x=0)' or fig_title == '温度推移(x=0.005)':
    x_name = '時間 (s)'
    y_name = '温度 (℃)'
    x_axis = []
if fig_title == '温度分布(t=50)':
    x_name = '位置x (m)'
    y_name = '温度 (℃)'
    x_axis = np.arange(0.0, LENGTH + D_X, D_X)
if fig_title == '熱伝達率の推移':
    x_name = '時間 (s)'
    y_name = '熱伝達率 (W・m⁻²・K⁻¹)'
y_axis = []

###温度算出
for n in range(N_TIME + 1):
    t = n * D_t  #現実の経過時間
    if folder_name == '100℃一定片面' or folder_name == '100℃一定両面':
        T_fu = 100
    if folder_name == '標準加熱曲線':
        T_fu = get_T_fu(t)

    if fig_title == '温度推移':
        x_axis.append(t)
        y_axis_1.append(T_fu)

    if fig_title == '標準加熱曲線' or fig_title == '温度推移(x=0)' or fig_title == '温度推移(x=0.005)':
        x_axis.append(t)
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
                    T_wd[n - 1][N_CELL - 1] - T_wd[n - 1][N_CELL]) - (
                        D_t * h_air /
                        (D_X * rho_c_wd)) * (T_wd[n - 1][N_CELL] - T_AIR) + (D_t * q_GEN) / rho_c_wd
                #DO:試験体の厚さを十分厚くすれば、非加熱面の状態を考慮しなくていい
                #TODO:内部発熱(最後の項）を考慮する（炭化について）DO:難燃処理層最後尾の次をどう考えるか（荷重支持部表面？長田さんは炉内温度？一面加熱だから、布施さんの外温と同じ？）

            # if fig_title == '':
            #     if x == 10:
            #         y_axis.append(lambda_wd)

    if folder_name == '100℃一定片面' or folder_name == '100℃一定両面':
        if fig_title == '温度推移':
            y_axis_2.append(T_wd[n][0])
            y_axis_3.append(T_wd[n][int(N_CELL / 2)])
            y_axis_4.append(T_wd[n][N_CELL])
    if folder_name == '標準加熱曲線':
        if fig_title == '温度推移':
            y_axis_2.append(T_wd[n][0])
            y_axis_3.append(T_wd[n][5])

    if fig_title == '温度推移(x=0)':
        y_axis.append(T_wd[n][0])
    if fig_title == '温度推移(x=0.005)':
        y_axis.append(T_wd[n][5])
    # print(t, T_fu, T_wd[n])
    #print(T_wd)
# print(T_wd)
if folder_name == '100℃一定片面' or folder_name == '100℃一定両面':
    if fig_title == '温度分布':
        y_axis_1 = T_wd[0]
        y_axis_2 = T_wd[int(N_TIME / 2)]
        y_axis_3 = T_wd[N_TIME]
if folder_name == '標準加熱曲線':
    if fig_title == '温度分布':
        y_axis_1 = T_wd[0]
        y_axis_2 = T_wd[int(N_TIME / 2)]
        y_axis_3 = T_wd[N_TIME]

if fig_title == '温度分布(t=50)':
    y_axis = T_wd[N_TIME]

###グラフ設定
##図の形式
#文字
plt.rcParams['font.family'] = 'MS Gothic'  #使用するフォント
plt.rcParams['font.size'] = 16  #フォントの大きさ
#目盛線
plt.rcParams['xtick.direction'] = 'in'  #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'  #y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.minorticks_on()
# plt.rcParams['axes.autolimit_mode'] = 'round_numbers'
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

if folder_name == '100℃一定片面' or folder_name == '100℃一定両面':
    if fig_title == '温度推移':
        #軸範囲
        plt.xlim(0, TIME_END)  #x軸範囲
        plt.ylim(20, 100)  #y軸範囲
        #プロット
        plt.plot(x_axis, y_axis_1, "-.r", label='炉内')  #(x, y, fmt), fmt = '[marker][line][color]'
        plt.plot(x_axis, y_axis_2, "-c", label='左端')
        plt.plot(x_axis, y_axis_3, "--g", label='中央')
        plt.plot(x_axis, y_axis_4, ":k", label='右端')
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1), ncol=4)  #凡例

    if fig_title == '温度分布':
        #軸範囲
        plt.xlim(0.00, LENGTH)  #x軸範囲
        plt.ylim(15, 100)  #y軸範囲
        #プロット
        plt.plot(x_axis, y_axis_1, "-r", label='0 s')  #(x, y, fmt), fmt = '[marker][line][color]'
        plt.plot(x_axis, y_axis_2, "--b", label=str(int(TIME_END / 2)) + ' s')
        plt.plot(x_axis, y_axis_3, ":g", label=str(TIME_END) + ' s')
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1), ncol=3)  #凡例

if folder_name == '標準加熱曲線':
    if fig_title == '標準加熱曲線':
        #軸範囲
        plt.xlim(0, TIME_END)  #x軸範囲
        plt.ylim(0, 350)  #y軸範囲
        plt.plot(x_axis, y_axis, '-', color="black")  #プロット
    if fig_title == '温度推移':
        #軸範囲
        plt.xlim(0, TIME_END)  #x軸範囲
        plt.ylim(20, 100)  #y軸範囲
        #プロット
        # plt.plot(x_axis, y_axis_1, "-r")  #(x, y, fmt), fmt = '[marker][line][color]'
        plt.plot(x_axis, y_axis_2, "-b", label='加熱面')
        plt.plot(x_axis, y_axis_3, "--g", label='加熱面から 5 mm')
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1), ncol=2)  #凡例

    if fig_title == '温度分布':
        #軸範囲
        plt.xlim(0.00, LENGTH)  #x軸範囲
        plt.ylim(15, 100)  #y軸範囲
        #プロット
        plt.plot(x_axis, y_axis_1, "-r", label='0 s')  #(x, y, fmt), fmt = '[marker][line][color]'
        plt.plot(x_axis, y_axis_2, "--b", label=str(int(TIME_END / 2)) + ' s')
        plt.plot(x_axis, y_axis_3, ":g", label=str(TIME_END) + ' s')
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1), ncol=3)  #凡例

#タイトル
if fig_title == '温度推移(x=0)' or fig_title == '温度推移(x=0.005)' or fig_title == '温度分布(t=50)':
    if RHO_WD_0 != 350.0:
        plt.title('図' + str(fig_number) + '　' + fig_title + '(d₀=' + str(RHO_WD_0) + ')', y=-0.30)

if fig_title == '温度推移(x=0)' or fig_title == '温度推移(x=0.005)' or fig_title == '温度分布(t=50)':
    plt.plot(x_axis, y_axis, '-', color="black")

# plt.rcParams['xtick.major.width'] = 1.0#x軸主目盛り線の線幅
# plt.rcParams['ytick.major.width'] = 1.0#y軸主目盛り線の線幅
# plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge linewidth。囲みの太さ

folder = "ver2/4_発表本番/" + folder_name + "/"
file_path = "images/" + folder + folder_name + fig_title
# file_path = "images/" + folder + folder_name + '_' + fig_title
if fig_title == '温度推移(x=0)' or fig_title == '温度推移(x=0.005)' or fig_title == '温度分布(t=50)':
    if RHO_WD_0 != 350.0:
        file_path = "images/" + folder + fig_title + '密度' + str(RHO_WD_0)
os.makedirs("images/" + folder, exist_ok=True)
plt.savefig(file_path.replace('.', '_'), bbox_inches="tight")
plt.show()