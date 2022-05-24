"""
Create a database containing the hashcodes of the songs stored 
in the specified folder (.wav files only). 
The database is saved as a pickle file as a list of dictionaries.
Each dictionary has two keys 'song' and 'hashcodes', corresponding 
to the name of the song and to the hashcodes used as signature for 
the matching algorithm.
"""

from concurrent.futures import process
import numpy as np
import matplotlib.pyplot as plt

from scipy.io.wavfile import read
from algorithm import *


# ----------------------------------------------
# Run the script
# ----------------------------------------------
if __name__ == '__main__':

    folder = './samples/'

    # 1: Load the audio files
    import os
    audiofiles = os.listdir(folder)
    audiofiles = [item for item in audiofiles if item[-4:] =='.wav']

    # 2: Set the parameters of the encoder
    # Insert your code here
    delta_t = 0.01
    table_fs_s = []
    for filename in audiofiles :
        fs, s = read(filename)
        table_fs_s.append([fs, s])
    tmin = int(50*fs) # We select an extract starting at 50s ...
    duration = int(10*fs) # ... which lasts 10s

    # 3: Construct the database
    database = []
    # Insert your code here
    for fs, s in table_fs_s:
        database.append(process(fs,s))

    # 4: Save the database
    with open('songs.pickle', 'wb') as handle:
        pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)

