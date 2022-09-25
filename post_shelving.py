"""
This file script usually runs after the "shelving.py" file.
This file performs Fourier Transform & related analysis and plots needed graphs.
(You need your shelve file because shelve files are binary and created for a specific machine)
"""
from platform import architecture
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
plt.style.use(['seaborn'])
from scipy.fft import fftfreq
from scipy.fft import fft, ifft, fft2, ifft2
import shelve

fnames = { #example of a dictionary for analyzing multiple simulations
    "over_t_low_step":
        [
        'shelve_over_t_l_step_n_of_p=100_concE=0.15_width=1_masktype=g_num_of_patches=128.out', 
        'shelve_over_t_l_step_n_of_p=100_concE=0.15_width=1_masktype=g_num_of_patches=256.out',
        'shelve_over_t_l_step=10_n_of_p=100_concE=0.15_width=1_masktype=g_num_of_patches=128.out',
        'shelve_over_t_l_step=10_n_of_p=100_concE=0.15_width=1_masktype=g_num_of_patches=256.out',
        ],
}

mode = 'over_t_low_step' 
"""Choose a file set from dict"""
FN = fnames[mode]

"""Useful functions below"""
def i_f(array, value): 
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def symlog_shift(arr, shift=0):
    # shift array-like to symlog array with shift
    logv = np.abs(arr)*(10.**shift)
    logv[np.where(logv<1.)] = 1.
    logv = np.sign(arr)*np.log10(logv)
    return logv

def lin_profile(x, y, start, end):
    if x <= start:
        return y
    elif x > start and x <= end:
        return y * (1 - (x - start) / (end - start))
    else:
        return 0

def tr_profile(x, y, start, end, slope):
    if start >= end: 
        print("start >= end")

    if x <= start or x>= end:
        return 0
    elif x > start and x <= start + slope:
        return y * (x - start) / slope
    elif x > end - slope and x < end:
        return y * (end - x) / slope
    else:
        return y

v_lin = np.vectorize(lin_profile)
v_tr = np.vectorize(tr_profile, otypes=[np.float])

"""Useful functions above"""

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)

"""Analysis below"""
for sh in FN:
    print(sh)
    my_shelf = shelve.open(sh)
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()
    
    N = Ez.shape[1]
    print(N)
    dt = Tsim/N
    t = np.linspace(0, Tsim, N)
    
    I = Ey * Bz - Ez * By
    I = np.abs(I)

    """if you want to cut the main laser pulse START"""
    # I = np.abs(v_tr(t, I, 750, 780, 0.03))
    # Ez = v_tr(t, Ez, 750, 780, 0.03)
    """if you want to cut the main laser pulse END"""

    f = fftfreq(N, dt)
    print(f.shape)
    I_ft = np.abs(np.fft.fft(I))
    E_ft = np.abs(np.fft.fft(Ez))

    I_ft_true = np.copy(np.abs(I_ft[:, :N//2]))
    f_true = np.copy(2 * np.pi * f[:N//2])
    print(np.sum(I_ft_true[0]))

    #plotting below
    ax0.plot(f_true, I_ft[0, :N//2])
    ax0.set_yscale('symlog', linthresh = 1e-9)
    ax0.grid()
    ax0.set_xlabel("omega")
    ax0.set_ylabel("I")

    ax1.set_yscale('symlog', linthresh = 1e-9)
    ax1.grid()
    # template -- ax1.plot(f_true, np.abs(E_ft[0,:N//2]))
    ax1.plot(t, I[0])
    ax1.set_xlabel("time")
    ax1.set_ylabel("I")
    
    ax2.set_yscale('symlog', linthresh = 1e-9)
    ax2.grid()
    ax2.plot(t, Ez[0])
    ax2.set_xlabel("time")
    ax2.set_ylabel("E_z")
plt.show()