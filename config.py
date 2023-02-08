TIME_END_100 = 8000  #[s]　加熱時間(100℃一定)
TIME_END_HEAT_RESISTANCE = 50  #[s]　加熱時間(標準加熱曲線)
LENGTH = 50 / 1000  #[m]　試験体厚さ
N_CELL = 50  #[個]　セルの個数 50以上が良さげ、50→250でおしりが1℃上昇
D_t = 0.1  #[s]　単位時間

q_FU = 0.0 * 1000  #[W/m²]　輻射 TODO:一旦輻射以外で考える。てか、表面温度を入力(既知と)して、その後ろをかんがえる。
q_GEN = 0.0  #[W/m³]　内部発熱
T_0_WD = 20.0  #[℃]　木材の初期温度
T_AIR_1 = 20  #[℃]
T_AIR_2_100 = 100  #[℃]
RHO_WD_0 = 350.0  #[kg/m³] 全乾密度　引用:木材の物理p37
ALPHA_WD = 0.18 / 10**6  #[m²/s] TODO:高温域まで対応してる式かどうかTODO:一定値としていいのかな？引用:木材の物理p63、先生に確認
D_X = LENGTH / N_CELL  #[m]　セルの幅
# N_TIME = int(TIME_END / D_t)  #[個]　秒の区切りの個数、0秒を入れる場合は+1する