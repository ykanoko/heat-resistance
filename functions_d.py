import numpy as np
from config import RHO_WD_0, ALPHA_WD


def get_T_fu(t):
    """標準加熱曲線により炉内空気温度を求める関数

    Args:
        t (s): 経過時間

    Returns:
        ℃:炉内空気温度
    """
    return 345 * np.log10(8 * t / 60 + 1) + 20


def get_h_air_wd(T_wd):
    """
    空気から木材への熱伝達率を求める関数
    Args:
        T_wd (℃):木材の温度 

    Returns:
        W/m²*K: 熱伝達率
    """
    return 0.168 * T_wd + 4.64
    #考察:引用:由田、式9,10、加熱面,非加熱面同じ式のため、非加熱面ではあるが空気と木材の式10を採用、式中の温度は低温度側の物質の温度を採用してそう？もしくは着目する物体？


def get_lambda_wd(rho_wd_0, T_wd, T1_wd=20, lambda1=0.09):
    """木材の温度から熱伝導率を求める関数

    Args:
        T_wd (℃): 熱伝導率を求める時の木材の温度
        T1_wd (℃, optional): 熱伝導率の参考値の時の木材の温度. Defaults to 20.
        lambda1 (W/m*K, optional): 熱伝導率の参考値. Defaults to 0.09.
        rho_wd_0 (kg/m³, optional): 木材の全乾密度. Defaults to RHO_WD_0.

    Returns:
        W/m*K:求めたい木材の熱伝導率 
    """
    return lambda1 * (1 - (1.1 - 0.00098 * rho_wd_0) * (T1_wd - T_wd) / 100)
    #TODO:高温域まで対応してる式かどうか#考察:引用の式がおそらく違うため、改編版引用:木材の物理p63(4-12)


def get_lambda_wd_0(rho_wd_0, T_wd, T1_wd=20):
    """全乾状態の木材の温度から熱伝導率を求める関数

    Args:
        T_wd (℃): 熱伝導率を求める時の木材の温度
        T1_wd (℃, optional): 熱伝導率の参考値の時の木材の温度. Defaults to 20.
        rho_wd_0 (kg/m³, optional): 木材の全乾密度. Defaults to RHO_WD_0.

    Returns:
        W/m*K:求めたい木材の熱伝導率
    """
    lambda20 = 1.163 * (0.022 + 0.724 * (rho_wd_0 / 1000) + 0.0931 * ((rho_wd_0 / 1000)**2))
    return lambda20 * (1 - (1.1 - 0.00098 * rho_wd_0) * (T1_wd - T_wd) / 100)
    #考察:値がでかすぎる。式4-09を使ってるけど、繊維方向の可能性もある？#引用:木材の物理（緑）p67


def get_rho_c_wd(rho_wd_0, T_wd):
    """木材の温度から密度ρ*比熱cを求める式

    Args:
        T_wd (℃): 木材の温度

    Returns:
        J/m³*K: 密度ρ*比熱c
    """
    lambda_wd = get_lambda_wd(rho_wd_0, T_wd)
    return lambda_wd / ALPHA_WD


def get_rho_c_wd_0(rho_wd_0, T_wd):
    """全乾状態の木材の温度から密度ρ*比熱cを求める式

    Args:
        T_wd (℃): 木材の温度

    Returns:
        J/m³*K: 密度ρ*比熱c
    """
    lambda_wd = get_lambda_wd_0(rho_wd_0, T_wd)
    return lambda_wd / ALPHA_WD


# print(get_h_air_wd(20))
# print(get_lambda_wd(20))
# print(get_lambda_wd_0(200))
# print(0.0029 * 150 + 0.01954)
# print(0.00275 * 21 + 0.09319)
# print(get_lambda_wd(21, 20, 0.14, 0.38))
"""
参考値
T=20

c = 1133 + 4.853*(T-373.15)

c_u =  (u/100 + c_0)/(u/100 + 1)

λ=0.09
λ=1.163*(0.022 + 0.724*d_0/1000 + 0.0931*(d_0/1000)^2)
λ_2 = λ_1*(1-k*(u_1-u_2))

λ_2 = λ_1*(1-(1.1-0.00098*d_0))*(T_1-T_2)/100
"""