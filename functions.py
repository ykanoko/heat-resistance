import numpy as np


def get_T_fu(t):
    345 * np.log10(8 * t / 60 + 1) + 20
