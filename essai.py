import pickle
from re import X
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.fft import fftshift

from scipy.io.wavfile import read
from scipy.signal import spectrogram
from skimage.feature import peak_local_max

import os
import random
import numpy as np
import matplotlib.pyplot as plt

from scipy.io.wavfile import read

songs = [item for item in os.listdir('./samples') if item[:-4] != '.wav']
song1 = songs[3]
song2 = songs[1]
#random.choice(songs)
print('Selected song: ' + song1[:-4])
filename1 = './samples/' + song1

print('Selected song: ' + song2[:-4])
filename2 = './samples/' + song2

fs, s = read(filename1)
fs2, s2 = read(filename2)
tmin = int(50*fs) # We select an extract starting at 50s ...
duration = int(10*fs) # ... which lasts 10s
 
window = scipy.signal.get_window('triang', 128)
spec_1 = scipy.signal.spectrogram(s, fs, window, noverlap = 32)[0]
spec_2 = scipy.signal.spectrogram(s, fs, window, noverlap = 32)[1]
#print(len(spec_1))
#plt.plot(spec_1)
#plt.specgram(spec_1, noverlap = 32)
#plt.show()

#Représentation 2D
f, t, Sxx = scipy.signal.spectrogram(s, fs)
f2, t2, Sxx2 = scipy.signal.spectrogram(s2, fs2)
#return_onesided=False

#Calcul de l'énergie
def energie(f):
    E = 0
    for a in f :
        E += a ** 2
    return E

#plt.pcolormesh(t, fftshift(f), fftshift(Sxx, axes=0), shading='gouraud')
#plt.pcolormesh(t, f, Sxx, shading='gouraud')
#plt.ylabel('Frequency [Hz]')
#plt.xlabel('Time [sec]')
#plt.show()
#On trouve une figure uniforme et donc une concentration uniforme de l'énergie
#Cherchons le nombre minimal pour avoir 90% de l'énergie de la chanson : Frisk - Au.Ra
E = energie(f)
print(f"l'énergie du signal est {E}")
new_f = f
new_E = energie(new_f)
print(len(f))
while new_E >= 0.9 * E :
    new_f = new_f[:-2]
    new_E = energie(new_f)
print(f"la nouvelle énergie est {new_E}, soit {1 - (E - new_E)/E} % de la valeur initiale et le nombre de fréquences est {len(new_f)}")
#On trouve donc que l'on concentre 90% de l'énergie sur 180 fréquences

#Trouver le bons nombres de maximums
coord_maxima = peak_local_max(Sxx, min_distance = 100, exclude_border = False)
coord_maxima2 = peak_local_max(Sxx2, min_distance = 100, exclude_border = False)
#plt.pcolormesh(maxima_locaux)
#plt.show()

#Construisons la constellation du morceau:
delta_t = 0.01
def constellation(delta_t,coord_maxima):
    hash = {}
    x = coord_maxima[:,0]
    y = coord_maxima[:,1]
    for i in range(len(x)):
        for j in range(i,len(x)):
            if abs(x[i] - x[j]) < delta_t and abs(y[i] - y[j]):
                hash[f"{i}"] = [abs(i - j), y[i],y[j]]
    return hash

# Test sur une chanson:
#stars = constellation(delta_t,coord_maxima)
#print(stars)

hashes1 = constellation(delta_t, coord_maxima)
hashes2 = constellation(delta_t, coord_maxima2)
keys1 = hashes1.keys()
keys2 = hashes2.keys()
time_cloud = [[],[]]
for k1 in keys1:
    for k2 in keys2:
        if k1 == k2:
            time_cloud[0].append(int(k1) - hashes1[k1][0])
            time_cloud[1].append(int(k2) - hashes2[k2][0])
plt.scatter(time_cloud[0],time_cloud[1])
plt.xlabel('ta')
plt.ylabel('ta_tilde')
plt.show()
#Le plot est une droite pour deux morceaux identiques et on trouve une droite et une autre incomplète lorsque les deux morceaux sont différents

#Tracçon l'histogramme des différences des temps:
diff = []
for s in time_cloud:
    diff.append(s[1] - s[0])
plt.hist(diff, bins = 100)
#plt.show()