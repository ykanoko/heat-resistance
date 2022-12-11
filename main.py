from math import log10
import numpy as np
import matplotlib.pyplot as plt
from functions import get_T_fu

t = 0  # time秒
T_fu = get_T_fu(t)  # 炉内温度℃


def T_fu(t):
    return 345 * np.log10(8 * t / 60 + 1) + 20


x = np.arange(0.0, 120.0 * 60, 1.0)
plt.plot(x, T_fu(x), 'b:')
plt.show()


def T_wd2(t):
    return


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