import happi
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(['seaborn'])
import shelve
import os
import subprocess

folder = "" #for cd ~/folder command
os.system("cd " + folder);

S = happi.Open(results_path='.', show=True, reference_angular_frequency_SI=None, verbose=True)

"""if you want to make a movie START"""
rho = 'example1.mp4'
E = 'example2.mp4'

S.Field(0, "-Rho_electron").animate(movie=rho, fps=4, dpi=200)
S.Field(0, "Ey**2 + Ez**2").animate(movie=E, fps=4, dpi=200)

os.system('ffmpeg \
    -i ' + rho + ' -i ' + E + ' \
    -filter_complex " \
        [0:v]setpts=PTS-STARTPTS, scale=960x720[top]; \
        [1:v]setpts=PTS-STARTPTS, scale=960x720, \
             format=yuva420p,colorchannelmixer=aa=0.5[bottom]; \
        [top][bottom]overlay=shortest=1" \
    -acodec libvo_aacenc -vcodec libx264 a=20_n=50_np=128_g.mp4')

"""if you want to make a movie END"""

Ey = np.array([np.array(S.Probe(0, "Ey").getData()), np.array(S.Probe(1, "Ey").getData())])
Ez = np.array([np.array(S.Probe(0, "Ez").getData()), np.array(S.Probe(1, "Ez").getData())])

By = np.array([np.array(S.Probe(0, "By").getData()), np.array(S.Probe(1, "By").getData())])
Bz = np.array([np.array(S.Probe(0, "Bz").getData()), np.array(S.Probe(1, "Bz").getData())])

"""Data from namelist.py START"""
l0 = 2. * np.pi
t0 = l0
Lsim = [140.*l0] 
resx = 728
rest = resx
n_particles = 100
n_of_patches = 128
w = 0.1
conc = 0.2
l_step = 30
Tsim = 200*t0
A = 5.

"""Data from namelist.py END"""

filename='sh_a=20_n=50_np=128_g.txt'
my_shelf = shelve.open(filename,'n') # 'n' for new
for key in dir():
    try:
        my_shelf[key] = globals()[key]
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR shelving: {0}'.format(key))
my_shelf.close()